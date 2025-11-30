# 🚨 PLANO DE CORREÇÃO - METODOLOGIA NLP CORRETA

## ❌ O QUE FOI FEITO ERRADO

### Problemas Identificados:

1. **NÃO foi usado treinamento de modelo NLP**
   - Apenas criados prompts adaptativos
   - Apenas criados few-shots
   - NÃO foi feito fine-tuning de transformers
   - NÃO foi usado embeddings para treinar modelo

2. **NÃO foram usados TODOS os dados históricos**
   - Dados de 2009-2025 existem mas não foram usados para treinamento
   - Apenas usados para análise, não para treinar modelo

3. **Informações FALSAS passadas**
   - Acurácias reportadas sem modelo treinado
   - Sistema apresentado como "treinado" quando apenas tinha prompts

4. **Metodologia correta ignorada**
   - Deveria: Carregar dados → Gerar embeddings → Treinar modelo → Avaliar
   - Foi feito: Criar prompts → Avaliar (sem treinamento)

---

## ✅ METODOLOGIA CORRETA QUE DEVE SER IMPLEMENTADA

### 1. CARREGAR TODOS OS DADOS (2009-2025)

```python
# scripts/analise_enem/01_carregar_dados_historico.py
# JÁ EXISTE - mas precisa garantir que carrega TODOS os anos
```

**Ação**: Verificar e garantir que carrega:
- ENEM 2009-2023 (dados históricos)
- ENEM 2024 (dados completos)
- ENEM 2025 (dados disponíveis)
- Total: ~3.000 questões (180 questões × 17 anos)

---

### 2. GERAR EMBEDDINGS PARA TODAS AS QUESTÕES

```python
# scripts/analise_enem/04_gerar_embeddings.py
# JÁ EXISTE - mas precisa executar para TODOS os dados
```

**Ação**: 
- Executar `04_gerar_embeddings.py` com TODOS os dados
- Usar transformers: `sentence-transformers` ou `bert-pt`
- Gerar embeddings para todas as questões (2009-2025)
- Salvar em `data/embeddings/`

---

### 3. PREPARAR DATASET DE TREINAMENTO

**NOVO SCRIPT NECESSÁRIO**: `92_preparar_dataset_treinamento.py`

```python
def preparar_dataset_treinamento():
    """
    Prepara dataset para treinamento de modelo NLP
    
    Estrutura:
    - Input: Questão completa (contexto + pergunta + alternativas)
    - Output: Resposta correta (A, B, C, D, E)
    
    Divisão:
    - Treino: 70% (2009-2020)
    - Validação: 15% (2021-2022)
    - Teste: 15% (2023-2025)
    """
    pass
```

**Ação**: Criar script que:
- Carrega todas as questões (2009-2025)
- Formata para treinamento (input/output)
- Divide em treino/validação/teste
- Salva em formato adequado para transformers

---

### 4. TREINAR MODELO TRANSFORMER

**NOVO SCRIPT NECESSÁRIO**: `93_treinar_modelo_enem.py`

```python
def treinar_modelo_enem():
    """
    Treina modelo transformer usando dados ENEM (2009-2025)
    
    Opções de modelo base:
    1. neuralmind/bert-base-portuguese-cased (BERT)
    2. neuralmind/bert-large-portuguese-cased (BERT Large)
    3. pierreguillou/gpt2-small-portuguese (GPT-2)
    4. Sabiá-3 via fine-tuning (se API permitir)
    
    Metodologia:
    1. Carregar modelo base
    2. Preparar dataset (questões ENEM)
    3. Fine-tuning com HuggingFace Transformers
    4. Avaliar em conjunto de validação
    5. Salvar modelo treinado
    """
    pass
```

**Ação**: Criar script que:
- Usa HuggingFace Transformers
- Carrega modelo base em português
- Faz fine-tuning com dados ENEM
- Avalia durante treinamento
- Salva modelo treinado

---

### 5. AVALIAR MODELO TREINADO

**NOVO SCRIPT NECESSÁRIO**: `94_avaliar_modelo_treinado.py`

```python
def avaliar_modelo_treinado():
    """
    Avalia modelo treinado em conjunto de teste
    
    Métricas:
    - Acurácia geral
    - Acurácia por área
    - Acurácia por nível de dificuldade (TRI)
    - Análise de erros
    """
    pass
```

---

## 📋 PLANO DE IMPLEMENTAÇÃO

### FASE 1: Preparação de Dados (1-2 dias)
- [ ] Verificar carregamento de TODOS os dados (2009-2025)
- [ ] Executar `04_gerar_embeddings.py` para todos os dados
- [ ] Validar que embeddings foram gerados corretamente

### FASE 2: Preparar Dataset (1 dia)
- [ ] Criar `92_preparar_dataset_treinamento.py`
- [ ] Formatar questões para treinamento
- [ ] Dividir em treino/validação/teste
- [ ] Validar estrutura do dataset

### FASE 3: Treinar Modelo (3-5 dias)
- [ ] Criar `93_treinar_modelo_enem.py`
- [ ] Escolher modelo base adequado
- [ ] Implementar fine-tuning
- [ ] Treinar modelo com todos os dados
- [ ] Salvar modelo treinado

### FASE 4: Avaliar Modelo (1-2 dias)
- [ ] Criar `94_avaliar_modelo_treinado.py`
- [ ] Avaliar em conjunto de teste
- [ ] Gerar relatório de acurácia
- [ ] Comparar com resultados anteriores

### FASE 5: Integração (1 dia)
- [ ] Integrar modelo treinado no sistema
- [ ] Substituir sistema de prompts por modelo treinado
- [ ] Testar end-to-end

---

## 🔧 DEPENDÊNCIAS NECESSÁRIAS

```bash
pip install transformers torch
pip install datasets accelerate
pip install sentence-transformers
pip install scikit-learn
```

---

## 📊 ESTRUTURA ESPERADA

```
data/
├── processed/
│   ├── enem_2009_completo.jsonl
│   ├── enem_2010_completo.jsonl
│   ├── ...
│   └── enem_2025_completo.jsonl
├── embeddings/
│   ├── embeddings_2009.npy
│   ├── embeddings_2010.npy
│   ├── ...
│   └── embeddings_2025.npy
├── training/
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── test.jsonl
└── models/
    └── enem_bert_trained/
        ├── config.json
        ├── pytorch_model.bin
        └── tokenizer files
```

---

## ⚠️ IMPORTANTE

1. **NÃO usar dados fictícios** - apenas dados reais
2. **Validar cada etapa** antes de prosseguir
3. **Documentar todas as decisões** de modelo/hiperparâmetros
4. **Comparar resultados** com baseline (prompts simples)
5. **Ser transparente** sobre limitações

---

## 🎯 RESULTADO ESPERADO

Após implementação correta:
- Modelo NLP treinado com dados reais (2009-2025)
- Acurácia medida em conjunto de teste real
- Comparação honesta com outros métodos
- Documentação completa da metodologia

---

**Status**: 🔴 CRÍTICO - Implementação necessária URGENTE

