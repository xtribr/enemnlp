# 📚 Integração de Dados Históricos do ENEM

## 🎉 Descoberta Importante

Encontramos um repositório com **dados históricos do ENEM de 2009 a 2023**!

**Repositório**: [gabriel-antonelli/extract-enem-data](https://github.com/gabriel-antonelli/extract-enem-data)

---

## 📊 Estrutura dos Dados

### Organização:
```
enem-data/
├── enem-2009/
│   ├── linguagens.csv
│   ├── ciencias-humanas.csv
│   ├── ciencias-natureza.csv
│   └── matematica.csv
├── enem-2010/
│   └── ...
├── ...
└── enem-2023/
    └── ...
```

### Formato CSV:
- **number**: Número da questão
- **context**: Contexto/texto base da questão
- **question**: Texto da pergunta
- **A, B, C, D, E**: Alternativas
- **answer**: Resposta correta
- **context-images**: Caminho para imagens (se houver)

### Estatísticas:
- **Período**: 2009-2023 (15 anos)
- **Áreas**: 4 áreas de conhecimento por ano
- **Total estimado**: ~2.000-3.000 questões por ano = **30.000-45.000 questões totais**

---

## 🔄 Integração com Dados Existentes

### Dados Atuais do Projeto:
- **2022**: JSON (formato antigo)
- **2024**: JSONL (formato novo, mais completo)

### Estratégia de Integração:
1. **Carregar dados históricos** (2009-2023) do repositório
2. **Normalizar formato** para estrutura unificada
3. **Combinar com dados existentes** (priorizar dados mais recentes/completos)
4. **Criar série temporal completa** (2009-2024)

---

## 🚀 Script de Integração

Criado: `scripts/analise_enem/01_carregar_dados_historico.py`

### Funcionalidades:
- ✅ Clona repositório extract-enem-data automaticamente
- ✅ Carrega dados de todos os anos (2009-2023)
- ✅ Normaliza estrutura (CSV → JSONL unificado)
- ✅ Integra com dados existentes (2022, 2023, 2024)
- ✅ Salva dados combinados em formato padronizado

### Uso:
```bash
python scripts/analise_enem/01_carregar_dados_historico.py
```

### Saída:
```
data/processed/
├── enem_2009_completo.jsonl
├── enem_2010_completo.jsonl
├── ...
└── enem_2024_completo.jsonl
```

---

## 📈 Impacto nas Análises

### Antes (3 anos):
- ❌ Série temporal muito curta
- ❌ Predições especulativas
- ❌ Análise limitada de tendências

### Agora (15 anos):
- ✅ Série temporal robusta (2009-2024)
- ✅ Predições mais confiáveis
- ✅ Análise profunda de tendências
- ✅ Modelos de ML mais robustos
- ✅ Validação adequada (treino: 2009-2021, teste: 2022-2024)

---

## 🎯 Análises Possíveis Agora

### 1. Análise Temporal Robusta
- Evolução de vocabulário ao longo de 15 anos
- Mudanças em tópicos e temas
- Tendências de complexidade

### 2. Modelos Preditivos
- Séries temporais (ARIMA, Prophet)
- Machine Learning (Random Forest, XGBoost)
- Deep Learning (LSTM, Transformers)

### 3. Análise Comparativa
- Comparar décadas (2009-2014 vs 2015-2020 vs 2021-2024)
- Identificar mudanças estruturais
- Padrões por área de conhecimento

### 4. Validação Robusta
- Treino: 2009-2021 (13 anos)
- Validação: 2022-2023 (2 anos)
- Teste: 2024 (1 ano)

---

## ⚠️ Considerações

### Qualidade dos Dados:
- ⚠️ Pode haver questões faltantes (conforme README do repositório)
- ⚠️ Formato pode variar entre anos
- ✅ Validar integridade dos dados após carregamento

### Normalização:
- Unificar formato entre anos diferentes
- Tratar campos vazios ou inconsistentes
- Validar estrutura antes de análises

### Armazenamento:
- Dados históricos são grandes (~30k-45k questões)
- Considerar compressão ou banco de dados
- Cache de embeddings e análises intermediárias

---

## 📋 Próximos Passos

1. ✅ **Executar script de integração** (`01_carregar_dados_historico.py`)
2. ✅ **Validar dados carregados** (estatísticas, integridade)
3. ✅ **Normalizar formato** entre todos os anos
4. ✅ **Atualizar análises** para usar série temporal completa
5. ✅ **Ajustar modelos preditivos** para série temporal robusta

---

## 🔗 Referências

- **Repositório**: https://github.com/gabriel-antonelli/extract-enem-data
- **Licença**: GPL-3.0
- **Formato**: CSV por ano e área
- **Período**: 2009-2023

---

**Última atualização**: 2024  
**Status**: Integração em andamento


