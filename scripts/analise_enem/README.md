# 📊 Análise Preditiva e Semântica do ENEM

Este diretório contém scripts para análise semântica, lexical e preditiva das provas do ENEM.

## ⚠️ Avisos Importantes

1. **Dados Reais Apenas**: Nunca criar dados fictícios
2. **Precisão Crítica**: Validar todas as análises com especialistas
3. **Limitações**: Apenas 3 anos de dados (2022, 2023, 2024)
4. **Predições**: Focar em tendências qualitativas, não predições precisas

## 📁 Estrutura

```
scripts/analise_enem/
├── README.md
├── 01_carregar_dados.py
├── 02_preprocessar_texto.py
├── 03_validar_dados.py
├── 04_gerar_embeddings.py
├── 05_analise_lexical.py
├── 06_modelagem_topicos.py
├── 07_complexidade_texto.py
├── 08_heuristica_dificuldade.py
├── 09_similaridade_provas.py
├── 10_validar_dificuldade.py
├── 11_serie_temporal.py
├── 12_identificar_padroes.py
├── 13_analise_por_area.py
├── 14_modelo_tendencias.py
├── 15_validar_predicoes.py
├── 16_intervalos_confianca.py
├── 17_visualizacoes.py
├── 18_gerar_relatorio.py
└── 19_dashboard_interativo.py
```

## 🚀 Como Usar

### Instalação de Dependências

```bash
pip install transformers sentence-transformers
pip install scikit-learn nltk spacy
pip install pandas numpy matplotlib seaborn
pip install plotly streamlit  # Para dashboards
```

### Execução Sequencial

```bash
# Fase 1: Preparação
python scripts/analise_enem/01_carregar_dados.py
python scripts/analise_enem/02_preprocessar_texto.py
python scripts/analise_enem/03_validar_dados.py

# Fase 2: Análise Semântica
python scripts/analise_enem/04_gerar_embeddings.py
# ... etc
```

## 📊 Saídas Esperadas

- `data/processed/`: Dados processados
- `data/embeddings/`: Embeddings gerados
- `data/analises/`: Resultados das análises
- `reports/`: Relatórios e visualizações

## 🔍 Validação

Sempre valide resultados com:
- Especialistas em ENEM
- Dados reais de desempenho (se disponíveis)
- Métricas estatísticas apropriadas


