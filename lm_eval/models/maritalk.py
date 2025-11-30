import json
import openai
import os
import time
from lm_eval.base import BaseLM
from lm_eval import utils
from tqdm import tqdm


def get_result(response, ctxlen):
    """Process results from OpenAI API response.

    :param response: dict
        OpenAI API Response
    :param ctxlen: int
        Length of context (so we can slice them away and only keep the predictions)
    :return:
        continuation_logprobs: np.array
            Log probabilities of continuation tokens
        is_greedy: bool
            whether argmax matches given continuation exactly
    """
    is_greedy = True
    logprobs = response["logprobs"]["token_logprobs"]
    continuation_logprobs = sum(logprobs[ctxlen:])

    for i in range(ctxlen, len(response["logprobs"]["tokens"])):
        token = response["logprobs"]["tokens"][i]
        top_tokens = response["logprobs"]["top_logprobs"][i]
        top_token = max(top_tokens.keys(), key=lambda x: top_tokens[x])
        if top_token != token:
            is_greedy = False
            break

    return continuation_logprobs, is_greedy


def oa_completion(client=None, **kwargs):
    """Query OpenAI API for completion.

    Retry with back-off until they respond
    Compatível com openai v0.x e v1.x+
    """
    backoff_time = 3
    while True:
        try:
            if client is not None:
                # API v1.x+ - usa client
                return client.chat.completions.create(**kwargs)
            else:
                # API v0.x - usa módulo direto
                return openai.ChatCompletion.create(**kwargs)
        except (openai.error.OpenAIError, openai.OpenAIError, openai.APIError) as e:
            import traceback
            traceback.print_exc()
            time.sleep(backoff_time)
            backoff_time *= 1.5


class MARITALKLM(BaseLM):
    REQ_CHUNK_SIZE = 1

    def __init__(self, engine, truncate=False):
        """

        :param engine: str
            OpenAI API engine (e.g. sabia-3)
        :param truncate: bool
            Truncate input if too long (if False and input is too long, throw error)
        """
        super().__init__()

        self.engine = engine
        
        # Detecta versão do openai e configura apropriadamente
        openai_version = openai.__version__
        major_version = int(openai_version.split('.')[0])
        
        # Read from environment variable (tenta múltiplas opções)
        api_key = (
            os.environ.get("MARITALK_API_SECRET_KEY") or
            os.environ.get("CURSORMINIMAC") or
            os.environ.get("MARITACA_API_KEY")
        )
        if not api_key:
            raise ValueError(
                "Chave API da Maritaca não encontrada! "
                "Configure uma das variáveis: MARITALK_API_SECRET_KEY, CURSORMINIMAC ou MARITACA_API_KEY"
            )
        
        if major_version >= 1:
            # API v1.x+ - usa client
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url="https://chat.maritaca.ai/api"
            )
            self.use_client = True
        else:
            # API v0.x - usa módulo direto
            openai.api_base = "https://chat.maritaca.ai/api"
            openai.api_key = api_key
            self.client = None
            self.use_client = False

    @property
    def eot_token_id(self):
        return self.tokenizer.eos_token_id

    @property
    def max_length(self):
        # Note: the OpenAI API supports up to 2049 tokens, with the first token being the first input token
        return 4000

    @property
    def max_gen_toks(self):
        return 512

    @property
    def batch_size(self):
        # Isn't used because we override _loglikelihood_tokens
        raise NotImplementedError()

    @property
    def device(self):
        # Isn't used because we override _loglikelihood_tokens
        raise NotImplementedError()

    def tok_encode(self, string: str):
        return self.tokenizer.encode(string, add_special_tokens=False)

    def tok_decode(self, tokens):
        return self.tokenizer.decode(tokens)

    def _loglikelihood_tokens(self, requests, disable_tqdm=False):
        # ChatGPT does not suppport max_tokens=0 and does not return logprobs
        raise NotImplementedError()

    def greedy_until(self, requests):
        if not requests:
            return []
        res = []

        def _collate(x):
            return len(x[0]), x[0]

        re_ord = utils.Reorderer(requests, _collate)

        def sameuntil_chunks(xs, size):
            ret = []
            lastuntil = xs[0][1]
            for x in xs:
                if len(ret) >= size or x[1] != lastuntil:
                    yield ret, lastuntil
                    ret = []
                    lastuntil = x[1]
                ret.append(x)

            if ret:
                yield ret, lastuntil

        # todo: more intelligent batching for heterogeneous `until`
        for chunk, until in tqdm(
            list(sameuntil_chunks(re_ord.get_reordered(), self.REQ_CHUNK_SIZE))
        ):
            inps = []
            for context, _ in chunk:
                try:
                    messages = json.loads(context)
                except json.decoder.JSONDecodeError:
                    # If context is not a valid JSON string, pass it as is
                    messages = [{"role": "user", "content": context}]
                inps.append(messages)

            response = oa_completion(
                client=self.client if self.use_client else None,
                model=self.engine,
                messages=inps[0],
                max_tokens=self.max_gen_toks, 
                temperature=0.,
                # stop=until,  # not working
                ## The server had an error processing your request. Sorry about 
                ## that! You can retry your request, or contact us through our 
                ## help center at help.openai.com if you keep seeing this error.  
            )

            # Extrai choices da resposta (compatível com ambas versões)
            if self.use_client:
                # API v1.x+
                choices = response.choices
            else:
                # API v0.x
                if hasattr(response, 'choices'):
                    choices = response.choices
                elif isinstance(response, dict) and 'choices' in response:
                    choices = response['choices']
                else:
                    choices = [response]
            
            for resp, (context, until_) in zip(choices, chunk):
                # Extrai conteúdo da mensagem (compatível com ambas versões)
                if self.use_client:
                    # API v1.x+
                    s = resp.message.content
                else:
                    # API v0.x
                    if hasattr(resp, 'message'):
                        s = resp.message['content'] if isinstance(resp.message, dict) else resp.message.content
                    elif isinstance(resp, dict):
                        s = resp.get('message', {}).get('content', str(resp))
                    else:
                        s = str(resp)

                for term in until_:
                    s = s.split(term)[0]

                # partial caching
                self.cache_hook.add_partial("greedy_until", (context, until_), s)

                res.append(s)

        return re_ord.get_original(res)

    def _model_call(self, inps):
        # Isn't used because we override _loglikelihood_tokens
        raise NotImplementedError()

    def _model_generate(self, context, max_length, eos_token_id):
        # Isn't used because we override greedy_until
        raise NotImplementedError()
