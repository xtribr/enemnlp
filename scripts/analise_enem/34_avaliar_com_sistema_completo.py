#!/usr/bin/env python3
"""
Avaliação usando Sistema Completo 100% Maritaca (Otimizado)

Inclui:
- Cache de análises semânticas
- Busca eficiente de questões similares
- Comparação com sistema anterior
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time
import hashlib
import random

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def configurar_api_maritaca():
    """Configura conexão com API Maritaca"""
    import openai
    
    api_key = (
        os.environ.get("CURSORMINIMAC") or
        os.environ.get("MARITALK_API_SECRET_KEY") or
        os.environ.get("MARITACA_API_KEY")
    )
    
    if not api_key:
        return None, None
    
    openai.api_base = "https://chat.maritaca.ai/api"
    openai_version = openai.__version__
    major_version = int(openai_version.split('.')[0])
    
    if major_version >= 1:
        client = openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")
        return client, 'v1'
    else:
        openai.api_key = api_key
        return openai, 'v0'

class CacheAnalises:
    """Cache para análises semânticas"""
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self.cache = self._carregar_cache()
    
    def _carregar_cache(self) -> Dict:
        """Carrega cache do arquivo"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _salvar_cache(self):
        """Salva cache no arquivo"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def _hash_questao(self, questao: Dict) -> str:
        """Gera hash único da questão"""
        texto = f"{questao.get('context', '')}{questao.get('question', '')}"
        return hashlib.md5(texto.encode()).hexdigest()
    
    def obter_analise(self, questao: Dict) -> Optional[Dict]:
        """Obtém análise do cache"""
        hash_q = self._hash_questao(questao)
        return self.cache.get(hash_q)
    
    def salvar_analise(self, questao: Dict, analise: Dict):
        """Salva análise no cache"""
        hash_q = self._hash_questao(questao)
        self.cache[hash_q] = analise
        self._salvar_cache()

def analise_semantica_profunda_maritaca(client, versao: str, questao: Dict, 
                                        cache: Optional[CacheAnalises] = None) -> Optional[Dict]:
    """Análise semântica profunda da questão usando Maritaca (com cache)"""
    
    # Verificar cache primeiro
    if cache:
        analise_cached = cache.obter_analise(questao)
        if analise_cached:
            return analise_cached
    
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    area = questao.get('area', 'desconhecida')
    
    prompt = f"""Você é a Maritaca Sabiá 3, especialista em ENEM.

Realize uma ANÁLISE SEMÂNTICA PROFUNDA da seguinte questão do ENEM:

ÁREA: {area}

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)
        prompt += f"{letra}. {alt}\n"
    
    prompt += """
ANÁLISE REQUERIDA (formate como JSON):
{{
  "conceitos_chave": ["lista de conceitos principais"],
  "tipo_problema": "tipo identificado",
  "armadilhas_comuns": ["lista de armadilhas"],
  "nivel_dificuldade": "fácil/médio/difícil",
  "conhecimentos_previos": ["lista de conhecimentos"],
  "estrategia_resolucao": "passo a passo resumido"
}}"""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.2
            )
            resposta = response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.2
            )
            resposta = response.choices[0].message.content
        
        # Extrair JSON (tentar múltiplas estratégias)
        import re
        analise = None
        
        # Estratégia 1: Buscar JSON completo
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', resposta, re.DOTALL)
        if json_match:
            try:
                analise = json.loads(json_match.group())
            except:
                pass
        
        # Estratégia 2: Se falhou, tentar extrair campos manualmente
        if not analise:
            analise = {}
            # Extrair conceitos-chave
            conceitos_match = re.search(r'conceitos[_\s]*chave["\']?\s*[:=]\s*\[(.*?)\]', resposta, re.IGNORECASE | re.DOTALL)
            if conceitos_match:
                conceitos_texto = conceitos_match.group(1)
                conceitos = [c.strip().strip('"\'') for c in conceitos_texto.split(',')]
                analise['conceitos_chave'] = conceitos
            
            # Extrair tipo de problema
            tipo_match = re.search(r'tipo[_\s]*problema["\']?\s*[:=]\s*["\']?([^"\']+)["\']?', resposta, re.IGNORECASE)
            if tipo_match:
                analise['tipo_problema'] = tipo_match.group(1).strip()
            
            # Se não conseguiu extrair nada, usar texto completo
            if not analise:
                analise = {'analise_texto': resposta[:500]}  # Limitar tamanho
        
        # Salvar no cache
        if cache:
            cache.salvar_analise(questao, analise)
        return analise
    except Exception as e:
        print(f"    ⚠️  Erro na análise: {e}")
        return None

def encontrar_questoes_similares_otimizado(questao_atual: Dict, analise_atual: Dict,
                                           banco_questoes: List[Dict], 
                                           questoes_resolvidas: Dict[str, str],
                                           num_similares: int = 3) -> List[Dict]:
    """Encontra questões similares de forma otimizada"""
    
    if not analise_atual:
        return []
    
    # Extrair conceitos-chave
    conceitos = analise_atual.get('conceitos_chave', [])
    if isinstance(conceitos, str):
        conceitos = [conceitos]
    
    tipo_problema = analise_atual.get('tipo_problema', '')
    area = questao_atual.get('area', '')
    
    # Busca otimizada: apenas questões da mesma área
    questoes_filtradas = [q for q in banco_questoes 
                          if q.get('area') == area and q.get('id') != questao_atual.get('id')]
    
    # Calcular similaridade simples (baseado em conceitos-chave)
    questoes_com_similaridade = []
    
    for questao in questoes_filtradas[:100]:  # Limitar busca
        contexto_outra = questao.get('context', '').lower()
        pergunta_outra = questao.get('question', '').lower()
        texto_outra = f"{contexto_outra} {pergunta_outra}"
        
        # Contar conceitos em comum
        palavras_comuns = sum(1 for conceito in conceitos 
                            if conceito.lower() in texto_outra)
        
        # Bonus se tipo de problema similar
        bonus_tipo = 2 if tipo_problema.lower() in texto_outra else 0
        
        similaridade = palavras_comuns + bonus_tipo
        
        if similaridade > 0:
            questoes_com_similaridade.append({
                'questao': questao,
                'similaridade': similaridade,
                'resposta_correta': questoes_resolvidas.get(questao.get('id'), questao.get('label', ''))
            })
    
    # Ordenar e retornar top N
    questoes_com_similaridade.sort(key=lambda x: x['similaridade'], reverse=True)
    
    return [item['questao'] for item in questoes_com_similaridade[:num_similares]]

def criar_prompt_few_shot_otimizado(questao: Dict, analise: Dict,
                                    questoes_similares: List[Dict],
                                    questoes_resolvidas: Dict[str, str]) -> str:
    """Cria prompt com few-shot learning otimizado"""
    
    prompt = """Você é a Maritaca Sabiá 3, especialista em ENEM.

Vou apresentar questões similares já resolvidas corretamente, e depois a questão que você deve resolver.

"""
    
    # Adicionar exemplos similares
    for i, questao_similar in enumerate(questoes_similares, 1):
        contexto_sim = questao_similar.get('context', '').strip()
        pergunta_sim = questao_similar.get('question', '').strip()
        alternativas_sim = questao_similar.get('alternatives', [])
        resposta_sim = questoes_resolvidas.get(questao_similar.get('id'), 
                                               questao_similar.get('label', '')).upper()
        
        prompt += f"""EXEMPLO {i} (Questão Similar - Resposta Correta: {resposta_sim}):

CONTEXTO:
{contexto_sim[:300]}...

PERGUNTA:
{pergunta_sim}

ALTERNATIVAS:
"""
        for j, alt in enumerate(alternativas_sim, 1):
            letra = chr(64 + j)
            prompt += f"{letra}. {alt}\n"
        
        prompt += f"\nRESPOSTA CORRETA: {resposta_sim}\n\n"
    
    # Adicionar análise semântica
    if analise:
        prompt += f"""ANÁLISE SEMÂNTICA DA QUESTÃO ATUAL:
- Conceitos-chave: {', '.join(analise.get('conceitos_chave', [])[:5])}
- Tipo de problema: {analise.get('tipo_problema', 'N/A')}
- Estratégia: {analise.get('estrategia_resolucao', 'N/A')[:200]}

"""
    
    # Adicionar questão atual
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    
    prompt += f"""QUESTÃO A RESOLVER:

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)
        prompt += f"{letra}. {alt}\n"
    
    prompt += """
INSTRUÇÕES:
1. Use os exemplos similares como referência
2. Aplique a análise semântica fornecida
3. Siga a mesma metodologia dos exemplos
4. Resolva passo a passo
5. Responda APENAS com a letra (A, B, C, D ou E)"""
    
    return prompt

def avaliar_questao_completo(client, versao: str, questao: Dict, 
                             banco_questoes: List[Dict],
                             questoes_resolvidas: Dict[str, str],
                             cache: Optional[CacheAnalises] = None) -> Dict:
    """Avalia questão usando sistema completo otimizado"""
    
    # 1. Análise semântica (com cache)
    analise = analise_semantica_profunda_maritaca(client, versao, questao, cache)
    
    # 2. Encontrar questões similares (otimizado)
    questoes_similares = encontrar_questoes_similares_otimizado(
        questao, analise, banco_questoes, questoes_resolvidas, num_similares=3
    )
    
    # 3. Criar prompt com few-shot
    if questoes_similares:
        prompt = criar_prompt_few_shot_otimizado(questao, analise, questoes_similares, questoes_resolvidas)
    else:
        # Fallback: prompt sem exemplos
        contexto = questao.get('context', '').strip()
        pergunta = questao.get('question', '').strip()
        alternativas = questao.get('alternatives', [])
        
        prompt = f"""Você é a Maritaca Sabiá 3, especialista em ENEM.

ANÁLISE SEMÂNTICA:
{json.dumps(analise, indent=2, ensure_ascii=False) if analise else 'N/A'}

QUESTÃO:

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
        for i, alt in enumerate(alternativas, 1):
            letra = chr(64 + i)
            prompt += f"{letra}. {alt}\n"
        
        prompt += "\nResolva passo a passo e responda APENAS com a letra (A, B, C, D ou E)."
    
    # 4. Avaliar questão
    resposta_correta = questao.get('label', '').upper().strip()
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        
        # Extrair letra
        import re
        match = re.search(r'\b([A-E])\b', resposta_ia)
        resposta_ia = match.group(1) if match else None
        
        acerto = resposta_ia == resposta_correta if resposta_ia else False
        
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': resposta_ia,
            'acerto': acerto,
            'usou_few_shot': len(questoes_similares) > 0,
            'num_exemplos': len(questoes_similares),
            'tem_analise': analise is not None
        }
    except Exception as e:
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': None,
            'acerto': False,
            'erro': str(e)
        }

def carregar_resultados_anteriores() -> Dict:
    """Carrega resultados anteriores para comparação"""
    project_root = Path(__file__).parent.parent.parent
    analises_dir = project_root / "data" / "analises"
    
    resultados = {}
    
    # Carregar último resultado de 50 questões
    arquivo_50 = analises_dir / "avaliacao_matematica_50_maritaca.json"
    if arquivo_50.exists():
        with open(arquivo_50, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            resultados['sistema_anterior_50'] = {
                'acuracia': dados.get('acuracia', 0),
                'total': dados.get('total', 0),
                'acertos': dados.get('acertos', 0)
            }
    
    # Carregar último resultado de 100 questões
    arquivo_100 = analises_dir / "avaliacao_matematica_100_maritaca.json"
    if arquivo_100.exists():
        with open(arquivo_100, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            resultados['sistema_anterior_100'] = {
                'acuracia': dados.get('acuracia', 0),
                'total': dados.get('total', 0),
                'acertos': dados.get('acertos', 0)
            }
    
    return resultados

def main():
    """Função principal"""
    import sys
    
    # Número de questões (padrão: 50)
    num_questoes = 50
    if len(sys.argv) > 1:
        try:
            num_questoes = int(sys.argv[1])
        except ValueError:
            pass
    
    print("=" * 70)
    print("🚀 SISTEMA COMPLETO 100% MARITACA (OTIMIZADO)")
    print(f"📊 Avaliando {num_questoes} questões de matemática")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    client, versao = configurar_api_maritaca()
    if not client:
        print("❌ API não configurada")
        return
    
    print("✅ API configurada")
    print()
    
    # Carregar questões
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    print("📥 Carregando questões...")
    banco_questoes = []
    questoes_resolvidas = {}  # ID -> resposta correta
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if questao.get('area') == 'mathematics':
                        banco_questoes.append(questao)
                        questoes_resolvidas[questao.get('id', '')] = questao.get('label', '').upper()
    
    print(f"✅ {len(banco_questoes)} questões de matemática carregadas")
    print()
    
    # Configurar cache
    cache_dir = project_root / "data" / "cache"
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / "analises_semanticas.json"
    cache = CacheAnalises(cache_file)
    print(f"💾 Cache configurado: {cache_file}")
    print()
    
    # Carregar resultados anteriores
    resultados_anteriores = carregar_resultados_anteriores()
    if resultados_anteriores:
        print("📊 Resultados anteriores para comparação:")
        for key, val in resultados_anteriores.items():
            print(f"   {key}: {val['acuracia']:.2f}% ({val['acertos']}/{val['total']})")
        print()
    
    # Selecionar questões para teste (filtrar ANULADAS)
    questoes_validas = [q for q in banco_questoes 
                        if q.get('label', '').upper() not in ['ANULADO', '']]
    questoes_teste = random.sample(questoes_validas, min(num_questoes, len(questoes_validas)))
    
    print("🚀 Iniciando avaliação...")
    print(f"   ⏱️  Estimativa: ~{num_questoes * 3} segundos (com cache)")
    print()
    
    resultados = []
    inicio = time.time()
    
    for i, questao in enumerate(questoes_teste, 1):
        print(f"  [{i}/{len(questoes_teste)}] {questao.get('id', '')[:40]}...", end=' ', flush=True)
        
        resultado = avaliar_questao_completo(
            client, versao, questao, banco_questoes, questoes_resolvidas, cache
        )
        resultados.append(resultado)
        
        if resultado.get('acerto'):
            print("✅")
        else:
            print(f"❌ (IA: {resultado.get('resposta_ia', 'N/A')}, Correta: {resultado.get('resposta_correta', 'N/A')})")
        
        time.sleep(0.5)  # Rate limiting
    
    tempo_total = time.time() - inicio
    
    # Resultados
    acertos = sum(1 for r in resultados if r.get('acerto'))
    acuracia = (acertos / len(resultados) * 100) if resultados else 0
    
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print(f"Total de questões: {len(resultados)}")
    print(f"Acertos: {acertos}")
    print(f"Erros: {len(resultados) - acertos}")
    print(f"Acurácia: {acuracia:.2f}%")
    print(f"Tempo total: {tempo_total:.1f}s ({tempo_total/len(resultados):.1f}s por questão)")
    print()
    
    # Estatísticas do sistema
    com_few_shot = sum(1 for r in resultados if r.get('usou_few_shot'))
    com_analise = sum(1 for r in resultados if r.get('tem_analise'))
    
    print("📈 Estatísticas do Sistema:")
    print(f"   Questões com few-shot learning: {com_few_shot}/{len(resultados)} ({com_few_shot/len(resultados)*100:.1f}%)")
    print(f"   Questões com análise semântica: {com_analise}/{len(resultados)} ({com_analise/len(resultados)*100:.1f}%)")
    print()
    
    # Comparação
    if resultados_anteriores.get('sistema_anterior_50'):
        anterior = resultados_anteriores['sistema_anterior_50']
        print("📊 Comparação com Sistema Anterior (50 questões):")
        print(f"   Sistema anterior: {anterior['acuracia']:.2f}%")
        print(f"   Sistema completo: {acuracia:.2f}%")
        diferenca = acuracia - anterior['acuracia']
        if diferenca > 0:
            print(f"   ✅ Melhoria: +{diferenca:.2f}%")
        else:
            print(f"   ⚠️  Redução: {diferenca:.2f}%")
        print()
    
    # Padrões de erro
    erros = [r for r in resultados if not r.get('acerto')]
    if erros:
        print("📊 Padrões de erro:")
        padroes = {}
        for erro in erros:
            correta = erro.get('resposta_correta', '')
            ia = erro.get('resposta_ia', '')
            if correta and ia:
                padrao = f"{correta}→{ia}"
                padroes[padrao] = padroes.get(padrao, 0) + 1
        
        for padrao, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {padrao:10s}: {count:2d} vezes")
        print()
    
    # Salvar resultados
    arquivo = project_root / "data" / "analises" / f"avaliacao_completa_{num_questoes}_maritaca.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump({
            'resultados': resultados,
            'total': len(resultados),
            'acertos': acertos,
            'erros': len(resultados) - acertos,
            'acuracia': acuracia,
            'tempo_total': tempo_total,
            'tempo_medio': tempo_total / len(resultados) if resultados else 0,
            'sistema': 'completo_100_maritaca_otimizado',
            'com_few_shot': com_few_shot,
            'com_analise': com_analise,
            'comparacao_anterior': resultados_anteriores
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {arquivo}")
    print()
    
    if acuracia >= 90:
        print("🎉 OBJETIVO ALCANÇADO! Acurácia >= 90%")
    elif acuracia >= 70:
        print(f"✅ Boa melhoria! Acurácia: {acuracia:.2f}%")
        print(f"   Faltam {90 - acuracia:.2f}% para 90%")
    else:
        print(f"📈 Acurácia: {acuracia:.2f}%")
        print(f"   Faltam {90 - acuracia:.2f}% para 90%")
        print("   Continue otimizando com ajuda da Maritaca")

if __name__ == "__main__":
    main()

