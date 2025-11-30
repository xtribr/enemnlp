# 📊 Gráficos Gerados - Análise ENEM

## 📈 Gráfico 1: Evolução da Acurácia do Projeto

**Arquivo**: `reports/visualizacoes/evolucao_acuracia_projeto.png`

### Descrição
Visualização da evolução da acurácia do projeto em Matemática do ENEM 2024, mostrando a progressão de **24% → 82.22%**.

### Dados Visualizados
- **Scripts Customizados**: 24% (baseline inicial)
- **Sistema Oficial (v1)**: 71.11% (+47.11 pontos percentuais)
- **Sistema Oficial (v2)**: 82.22% (+11.11 pontos percentuais)
- **Meta 90%**: Linha de referência

### Melhoria Total
**+58 pontos percentuais** (de 24% para 82.22%)

### Características do Gráfico
- Barras coloridas representando cada etapa
- Linha de evolução conectando as etapas
- Linha de benchmark (82.22%) destacada
- Anotações mostrando ganhos incrementais

---

## 📊 Gráfico 2: Dificuldade por Área (2009-2025)

**Arquivo**: `reports/visualizacoes/dificuldade_por_area_2009_2025.png`

### Descrição
Evolução cronológica da dificuldade média das questões do ENEM por área de conhecimento, de 2009 a 2025.

### Áreas Analisadas
1. **Linguagens** (azul)
2. **Humanas** (vermelho)
3. **Natureza** (verde)
4. **Matemática** (laranja)

### Estatísticas por Área (2009-2024)

| Área | Média | Mínimo | Máximo |
|------|-------|--------|--------|
| Humanas | 32.25 | 11.43 | 36.56 |
| Linguagens | 32.75 | 16.47 | 37.90 |
| Matemática | 36.51 | 12.63 | 41.81 |
| Natureza | 37.72 | 34.50 | 40.53 |

### Insights
- **Natureza** é a área com maior dificuldade média (37.72)
- **Humanas** é a área com menor dificuldade média (32.25)
- **Matemática** tem a maior variação (12.63 - 41.81)
- **Natureza** tem a menor variação (34.50 - 40.53), indicando consistência

### Características do Gráfico
- Linhas temporais para cada área
- Área preenchida sob cada linha (fill_between)
- Destaque para 2025 (linha vertical tracejada)
- Grid para facilitar leitura
- Legenda clara com cores distintas

---

## 🔧 Como Reproduzir

### Gráfico de Evolução
```bash
python scripts/analise_enem/41_grafico_evolucao_projeto.py
```

### Gráfico de Dificuldade por Área
```bash
python scripts/analise_enem/42_grafico_dificuldade_por_area.py
```

### Pré-requisitos
- Dados de dificuldade processados (`data/analises/dificuldade_completo.json`)
- Biblioteca matplotlib instalada: `pip install matplotlib`

---

## 📁 Localização dos Arquivos

Todos os gráficos são salvos em:
```
reports/visualizacoes/
├── evolucao_acuracia_projeto.png
└── dificuldade_por_area_2009_2025.png
```

---

*Documento gerado em: 29/11/2025*

