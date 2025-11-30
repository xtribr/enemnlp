# ✅ Checklist: Ambiente Colab Configurado

## 🎉 Parabéns! Seu ambiente está configurado

Agora você pode executar avaliações do ENEM com a API Maritaca. Siga este checklist:

---

## 📋 Próximos Passos

### 1. ✅ Verificar Configuração

Execute estas células para confirmar que tudo está funcionando:

```python
# Verificar GPU
import torch
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Não disponível'}")

# Verificar API
import os
api_key = os.environ.get('CURSORMINIMAC') or os.environ.get('MARITALK_API_SECRET_KEY')
print(f"API configurada: {'✅' if api_key else '❌'}")
```

### 2. 🧪 Teste Rápido (Recomendado)

Antes de executar uma avaliação completa, faça um teste com poucas questões:

```python
!python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt \
    --limit 5 \
    --output_path results/teste_rapido.json
```

**Tempo estimado**: 2-5 minutos  
**Custo estimado**: Muito baixo (apenas 5 questões)

### 3. 📊 Analisar Resultados do Teste

Após o teste, analise os resultados:

```python
import json
from pathlib import Path

with open('results/teste_rapido.json', 'r') as f:
    results = json.load(f)

print("📊 Resultados:")
if 'results' in results:
    for task_name, task_results in results['results'].items():
        print(f"\n{task_name}:")
        print(f"  Acurácia: {task_results.get('acc', 0):.2%}")
```

### 4. 🚀 Avaliação Completa (Opcional)

Se o teste funcionou, você pode executar a avaliação completa:

```python
!python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt \
    --output_path results/sabia3_enem2024_completo.json
```

**⚠️ ATENÇÃO**:
- **Tempo estimado**: 30-60 minutos (dependendo da API)
- **Custo**: Pode ser significativo (180 questões)
- **Recomendação**: Execute apenas se necessário

---

## 🎯 Tarefas Disponíveis

Você pode avaliar diferentes configurações:

### Por Edição:
- `enem_cot_2024_blind` - ENEM 2024 sem imagens
- `enem_cot_2023_blind` - ENEM 2023 sem imagens
- `enem_cot_2022_blind` - ENEM 2022 sem imagens

### Por Modalidade:
- `*_blind` - Sem imagens (apenas texto)
- `*_captions` - Com descrições textuais das imagens
- `*_images` - Com imagens (não suportado por modelos de texto)

### Com ou Sem CoT:
- `enem_cot_*` - Com Chain-of-Thought (raciocínio passo-a-passo)
- `enem_*` - Sem Chain-of-Thought (resposta direta)

### Exemplo: Múltiplas Tarefas

```python
!python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind,enem_cot_2024_captions \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt \
    --output_path results/comparacao.json
```

---

## 📈 Análise de Resultados

### Visualização Simples

```python
import json
import matplotlib.pyplot as plt

with open('results/teste_rapido.json', 'r') as f:
    results = json.load(f)

if 'results' in results:
    for task_name, task_results in results['results'].items():
        areas = {
            'languages': 'Linguagens',
            'human-sciences': 'Humanas',
            'natural-sciences': 'Natureza',
            'mathematics': 'Matemática'
        }
        
        area_names = []
        acuracias = []
        
        for area_key, area_name in areas.items():
            if area_key in task_results:
                area_names.append(area_name)
                acuracias.append(task_results[area_key])
        
        if area_names:
            plt.figure(figsize=(10, 6))
            plt.bar(area_names, acuracias)
            plt.title(f'Acurácia por Área - {task_name}')
            plt.ylabel('Acurácia')
            plt.ylim(0, 1)
            plt.show()
```

### Exportar para Análise

```python
import json
import pandas as pd

# Carregar resultados
with open('results/teste_rapido.json', 'r') as f:
    results = json.load(f)

# Converter para DataFrame (se necessário)
# Processar e exportar conforme sua necessidade
```

---

## 💾 Backup dos Resultados

**IMPORTANTE**: Faça download dos resultados antes de desconectar!

### Método 1: Download Manual
1. Vá em **Files** (ícone de pasta à esquerda)
2. Navegue até `results/`
3. Clique com botão direito no arquivo → **Download**

### Método 2: Download Automático

```python
from google.colab import files
files.download('results/teste_rapido.json')
```

### Método 3: Salvar no Google Drive

```python
# Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Copiar resultados
!cp results/*.json /content/drive/MyDrive/enem_results/
```

---

## 🔧 Troubleshooting

### Erro: "Module not found"
```python
# Reinstalar dependências
!pip install -e .
```

### Erro: "API authentication failed"
```python
# Verificar chave
import os
print(f"Chave configurada: {bool(os.environ.get('CURSORMINIMAC'))}")
```

### Erro: "File not found: data/enem/2024.jsonl"
```python
# Os dados são baixados automaticamente na primeira execução
# Ou faça upload manual dos arquivos .jsonl
```

### Sessão expirou
- Faça download dos resultados regularmente
- Use `--output_path` para salvar automaticamente
- Considere usar Google Drive para persistência

---

## 📊 Exemplo Completo de Workflow

```python
# 1. Setup (já feito)
import os
os.environ['CURSORMINIMAC'] = 'sua-chave'

# 2. Teste rápido
!python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt \
    --limit 5 \
    --output_path results/teste.json

# 3. Analisar
import json
with open('results/teste.json') as f:
    results = json.load(f)
print(json.dumps(results, indent=2, ensure_ascii=False))

# 4. Se tudo OK, executar completo
# !python main.py ... (sem --limit)

# 5. Download
from google.colab import files
files.download('results/teste.json')
```

---

## 🎓 Dicas Finais

1. **Sempre teste primeiro** com `--limit 5`
2. **Monitore custos** da API Maritaca
3. **Faça backup** regularmente dos resultados
4. **Use cache** (não use `--no_cache` a menos que necessário)
5. **Compare resultados** entre diferentes configurações

---

**Boa sorte com suas avaliações! 🚀**


