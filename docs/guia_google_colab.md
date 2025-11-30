# 🚀 Guia: Usar GPT-4-ENEM no Google Colab com GPU

Este guia explica como configurar e usar o projeto GPT-4-ENEM no Google Colab para aproveitar GPUs como A100, T4, V100, etc.

---

## 📋 Índice

1. [Por que usar Google Colab?](#por-que-usar-google-colab)
2. [Configuração Inicial](#configuração-inicial)
3. [Usando o Notebook](#usando-o-notebook)
4. [Alternativas: Upload Manual](#alternativas-upload-manual)
5. [Dicas e Troubleshooting](#dicas-e-troubleshooting)

---

## 🎯 Por que usar Google Colab?

### Vantagens:
- ✅ **GPU gratuita** (T4) ou A100 com Colab Pro
- ✅ **Ambiente pré-configurado** (Python, CUDA, etc.)
- ✅ **Sem instalação local** necessária
- ✅ **Fácil compartilhamento** de notebooks
- ✅ **Armazenamento temporário** para dados e resultados

### Limitações:
- ⚠️ Sessões têm tempo limite (12h gratuito, 24h Pro)
- ⚠️ GPU pode não estar sempre disponível (gratuito)
- ⚠️ Dados são temporários (faça backup!)

---

## 🚀 Configuração Inicial

### Passo 1: Acessar Google Colab

1. Acesse: https://colab.research.google.com/
2. Faça login com sua conta Google
3. Crie um novo notebook ou abra um existente

### Passo 2: Configurar GPU

1. Vá em **Runtime → Change runtime type**
2. Em **Hardware accelerator**, selecione **GPU**
3. Para A100, você precisa de **Colab Pro** ou **Colab Pro+**
4. Clique em **Save**

### Passo 3: Abrir Notebook

**Opção A: Usar notebook pré-configurado**
- Abra `notebooks/gpt4_enem_colab_setup.ipynb` no Colab
- Ou faça upload do arquivo `.ipynb`

**Opção B: Criar do zero**
- Siga as instruções abaixo

---

## 📓 Usando o Notebook

### Estrutura do Notebook

O notebook `gpt4_enem_colab_setup.ipynb` contém:

1. **Verificação de GPU** - Confirma se GPU está ativa
2. **Instalação de Dependências** - Instala todos os pacotes necessários
3. **Clone do Repositório** - Baixa o código do GitHub
4. **Configuração de API** - Configura chaves da Maritaca/OpenAI
5. **Teste de Conexão** - Verifica se API está funcionando
6. **Execução de Avaliações** - Roda avaliações do ENEM
7. **Análise de Resultados** - Visualiza e analisa resultados

### Executando Células

1. Execute cada célula na ordem (Shift+Enter)
2. Aguarde instalações completarem
3. Configure sua chave API antes de testar conexão

---

## 🔧 Alternativas: Upload Manual

Se preferir não clonar do GitHub:

### Passo 1: Preparar Arquivos

No seu computador local:

```bash
# Criar arquivo ZIP do projeto (sem dados grandes)
zip -r gpt4-enem-colab.zip . \
    -x "*.git*" \
    -x "data/figures/*" \
    -x "lm_cache/*" \
    -x "*.pyc" \
    -x "__pycache__/*"
```

### Passo 2: Upload no Colab

1. No Colab, vá em **Files → Upload**
2. Selecione o arquivo ZIP
3. Descompacte:
   ```python
   !unzip gpt4-enem-colab.zip
   ```

### Passo 3: Instalar Dependências

Siga as células do notebook para instalar tudo.

---

## ⚙️ Configuração Detalhada

### 1. Verificar GPU

```python
import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"Memória: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

### 2. Instalar Dependências

```python
# Instalar PyTorch com CUDA
!pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Instalar dependências do projeto
!pip install -q transformers datasets scikit-learn
!pip install -q sqlitedict pytablewriter sacrebleu rouge-score
!pip install -q openai fschat

# Instalar projeto
!git clone https://github.com/piresramon/gpt-4-enem.git
%cd gpt-4-enem
!pip install -e .
```

### 3. Configurar API

```python
import os

# Sua chave API da Maritaca
os.environ['CURSORMINIMAC'] = 'sua-chave-aqui'

# Ou
os.environ['MARITALK_API_SECRET_KEY'] = 'sua-chave-aqui'
```

### 4. Testar Conexão

```python
import openai

api_key = os.environ.get('CURSORMINIMAC')
openai.api_base = "https://chat.maritaca.ai/api"

# Para openai >= 1.0
client = openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")
response = client.chat.completions.create(
    model="sabia-3",
    messages=[{"role": "user", "content": "OK"}],
    max_tokens=5
)
print(response.choices[0].message.content)
```

### 5. Executar Avaliação

```python
!python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt \
    --limit 10 \
    --output_path results/teste.json
```

---

## 💡 Dicas e Troubleshooting

### GPU não disponível?

**Problema**: "GPU não detectada"

**Soluções**:
1. Verifique se ativou GPU em Runtime → Change runtime type
2. Para A100, você precisa de Colab Pro
3. Tente desconectar e reconectar (Runtime → Disconnect and delete runtime)

### Erro de memória?

**Problema**: "Out of memory"

**Soluções**:
1. Use `--limit` para testar com menos questões
2. Feche outras abas do Colab
3. Reinicie o runtime (Runtime → Restart runtime)

### API não funciona?

**Problema**: "Authentication error"

**Soluções**:
1. Verifique se a chave está correta
2. Confirme que configurou a variável de ambiente
3. Teste a chave localmente primeiro

### Dados não encontrados?

**Problema**: "File not found: data/enem/2024.jsonl"

**Soluções**:
1. Os dados são baixados automaticamente na primeira execução
2. Ou faça upload manual dos arquivos `.jsonl`
3. Verifique o caminho do diretório

### Sessão expirada?

**Problema**: "Runtime disconnected"

**Soluções**:
1. Faça download dos resultados regularmente
2. Use `--output_path` para salvar resultados
3. Colab Pro tem sessões mais longas (24h)

---

## 📊 Exemplo Completo

```python
# 1. Setup
import os
os.environ['CURSORMINIMAC'] = 'sua-chave'

# 2. Executar avaliação
!python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt \
    --limit 5 \
    --output_path results/teste.json

# 3. Analisar resultados
import json
with open('results/teste.json') as f:
    results = json.load(f)
print(json.dumps(results, indent=2, ensure_ascii=False))
```

---

## 🔄 Workflow Recomendado

1. **Abrir Colab** → Criar novo notebook
2. **Configurar GPU** → Runtime → Change runtime type → GPU
3. **Executar setup** → Rodar células de instalação
4. **Configurar API** → Adicionar sua chave
5. **Testar** → Rodar avaliação com `--limit 5`
6. **Avaliar completo** → Remover `--limit` para avaliação completa
7. **Download** → Baixar resultados antes de desconectar

---

## 📦 Estrutura de Arquivos no Colab

```
/content/
├── gpt-4-enem/          # Projeto clonado
│   ├── data/
│   │   └── enem/        # Dados ENEM
│   ├── lm_eval/         # Código de avaliação
│   ├── main.py          # Script principal
│   └── ...
├── results/              # Resultados (criar manualmente)
│   └── *.json           # Arquivos de resultados
└── ...
```

---

## 🎓 Casos de Uso

### 1. Teste Rápido
```bash
--limit 5  # Apenas 5 questões
```

### 2. Avaliação Completa
```bash
# Sem --limit, todas as questões
```

### 3. Múltiplas Tarefas
```bash
--tasks enem_cot_2024_blind,enem_cot_2024_captions
```

### 4. Comparação de Modelos
```bash
# Executar com diferentes --model_args
```

---

## ⚠️ Importante

1. **Dados são temporários** - Faça download regularmente
2. **Custos de API** - Monitore uso da API Maritaca
3. **Tempo de sessão** - Sessões expiram (12h/24h)
4. **GPU não é necessária** - API Maritaca é remota, mas Colab oferece ambiente estável

---

## 📞 Suporte

- **Documentação**: `docs/`
- **Notebook**: `notebooks/gpt4_enem_colab_setup.ipynb`
- **Issues**: GitHub do projeto

---

**Última atualização**: 2024


