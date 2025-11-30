# 📊 Gráficos de Dificuldade ENEM 2009-2025

## ✅ Gráficos Gerados

### 1. Gráfico de Dificuldade por Área (2009-2025)
**Arquivo:** `reports/visualizacoes/dificuldade_por_area_2009_2025.png`

**Descrição:**
- Mostra a evolução cronológica da dificuldade média por área de conhecimento
- 4 áreas: Linguagens, Humanas, Natureza, Matemática
- Período: 2009-2025 (17 anos)
- Destaque especial para 2025 (linha vertical vermelha)

**Estatísticas por Área:**
- **Humanas**: Média 33.52 | Min 30.41 | Max 36.56
- **Linguagens**: Média 34.19 | Min 30.87 | Max 38.19
- **Natureza**: Média 37.57 | Min 34.50 | Max 40.53
- **Matemática**: Média 37.83 | Min 32.42 | Max 41.81

### 2. Gráfico Temporal de Dificuldade (2009-2025)
**Arquivo:** `reports/visualizacoes/dificuldade_temporal_2009_2025.png`

**Descrição:**
- **Painel Superior**: Evolução da dificuldade média geral (todas as áreas combinadas)
  - Inclui linha de tendência
  - Destaque para 2025
- **Painel Inferior**: Evolução da dificuldade por área (4 linhas)
  - Comparação visual entre áreas
  - Destaque para 2025

**Estatísticas Temporais:**
- **Média Geral**: 36.09
- **Mínimo**: 33.61 (2025)
- **Máximo**: 41.87 (2024)
- **Primeiro ano (2009)**: 38.08
- **Último ano (2025)**: 33.61

## 📈 Observações Importantes

### Tendência Geral
- **2009**: 38.08 (início do período analisado)
- **2024**: 41.87 (pico de dificuldade)
- **2025**: 33.61 (redução significativa)

### Por Área (2025)
- **Linguagens**: 33.61 (abaixo da média histórica)
- **Humanas**: 33.61 (próximo da média histórica)
- **Natureza**: 33.61 (abaixo da média histórica)
- **Matemática**: 33.61 (abaixo da média histórica)

### Análise
1. **2025 mostra redução na dificuldade** em relação a 2024
2. **Matemática e Natureza** são tradicionalmente as áreas mais difíceis
3. **Humanas** é a área com menor dificuldade média
4. **Tendência geral**: Flutuação entre 33-42 pontos ao longo dos anos

## 🔧 Scripts Utilizados

1. **`42_grafico_dificuldade_por_area.py`**
   - Gera gráfico de evolução por área
   - Cores distintas para cada área
   - Preenchimento sob as linhas

2. **`57_grafico_temporal_dificuldade.py`**
   - Gera gráfico temporal com 2 painéis
   - Painel superior: evolução geral
   - Painel inferior: evolução por área
   - Linha de tendência no painel superior

## 📊 Dados Base

- **Fonte**: `data/analises/dificuldade_completo.json`
- **Método**: Heurísticas baseadas em:
  - Complexidade sintática
  - Raridade lexical
  - Comprimento do texto
- **Anos incluídos**: 2009-2025 (17 anos)
- **Total de questões analisadas**: ~2,779 questões

## 💡 Como Regenerar os Gráficos

```bash
# Gráfico por área
python scripts/analise_enem/42_grafico_dificuldade_por_area.py

# Gráfico temporal
python scripts/analise_enem/57_grafico_temporal_dificuldade.py
```

## ⚠️ Notas Importantes

1. **Dificuldade calculada por heurísticas**: Valide com dados reais de desempenho quando disponíveis
2. **2025 tem dados parciais**: 160 questões (faltam 20 de Linguagens)
3. **Metodologia**: Baseada em análise textual, não em desempenho real dos estudantes

