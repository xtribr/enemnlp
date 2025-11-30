# 📊 Plano de Análise Preditiva e Semântica do ENEM

## 🎯 Revisão do Plano Proposto

Este documento revisa e aprimora o plano de análise preditiva do ENEM, considerando:
- Estrutura real dos dados disponíveis
- Regras de precisão educacional (impacto crítico)
- Integração com API Maritaca
- Contexto de uso (EdTech XTRI)

---

## ✅ Pontos Fortes do Plano Original

1. **Abordagem Multidisciplinar**: Combina análise semântica, lexical e preditiva
2. **Série Temporal**: Identifica padrões históricos
3. **Visualização**: Facilita compreensão dos resultados
4. **Aplicação Prática**: Útil para orientação educacional

---

## 🔧 Ajustes e Melhorias Sugeridas

### 1. **Carregamento e Pré-processamento de Dados**

#### ✅ Mantido:
- Carregar provas do ENEM (2022, 2023, 2024)
- Extrair questões, alternativas, respostas corretas

#### 🔄 Ajustes Necessários:
- **Formato dos dados**: 
  - 2024: JSONL (uma questão por linha)
  - 2022: JSON (array de questões)
  - 2023: Verificar formato disponível
- **Campos disponíveis**:
  - `question`: Texto da questão
  - `alternatives`: Lista de alternativas
  - `label`: Resposta correta (A, B, C, D, E)
  - `exam`: Ano da prova
  - `description`: Descrições textuais de imagens
  - `figures`: Caminhos para imagens
  - `id`: Identificador único

#### ⚠️ Considerações:
- **NÃO remover stopwords** para questões de língua portuguesa (podem ser importantes)
- **Tokenização cuidadosa** para preservar contexto
- **Tratar campos vazios** (`description`, `figures`)
- **Normalizar formato** entre diferentes anos

### 2. **Análise Semântica e Lexical**

#### ✅ Mantido:
- Embeddings de palavras/sentenças
- Análise de frequência de vocabulário
- Modelagem de tópicos (LDA, NMF)
- Análise de complexidade

#### 🔄 Ajustes:
- **Usar modelos em português**:
  - `neuralmind/bert-base-portuguese-cased`
  - `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
  - Ou usar API Maritaca para embeddings
- **Análise por área de conhecimento**:
  - Linguagens e Códigos
  - Ciências Humanas
  - Ciências da Natureza
  - Matemática
- **Considerar contexto completo**:
  - Questão + alternativas + descrições de imagens

#### 💡 Integração com API Maritaca:
- Usar Sabiá-3 para:
  - Extração de tópicos principais
  - Análise de complexidade semântica
  - Geração de resumos temáticos

### 3. **Análise de Dificuldade e Similaridade**

#### ✅ Mantido:
- Métodos para inferir dificuldade
- Similaridade entre provas

#### 🔄 Ajustes Críticos:
- **Dificuldade**:
  - **NÃO usar dados fictícios** de desempenho
  - Se houver dados reais (190k+ registros mencionados), usar
  - Heurísticas baseadas em:
    - Complexidade sintática (árvores de dependência)
    - Raridade lexical (frequência de palavras)
    - Comprimento do texto
    - Número de conceitos envolvidos
  - **Validar com especialistas** antes de usar em produção
- **Similaridade**:
  - Similaridade de cosseno entre embeddings médios
  - Jaccard similarity para vocabulário
  - Similaridade de tópicos (distribuição LDA)

#### ⚠️ Precisão Educacional:
- **Sempre validar** resultados com professores/especialistas
- **Documentar** todas as métricas e métodos
- **Não fazer afirmações** sem evidências sólidas

### 4. **Preparação para Predição**

#### ✅ Mantido:
- Série temporal
- Identificação de padrões

#### ✅ Ajustes (ATUALIZADO):
- **Dados históricos disponíveis**:
  - **15 anos de dados** (2009-2023) do repositório extract-enem-data
  - **Série temporal robusta** para predições mais confiáveis
  - Dados organizados por área de conhecimento
  - Integração com dados existentes (2022, 2023, 2024)
- **Estrutura dos dados históricos**:
  - Formato CSV por ano e área
  - Campos: number, context, question, A-E, answer, context-images
  - Imagens em pastas separadas
- **Agregação por área**:
  - Análise separada por área de conhecimento
  - Padrões específicos de cada área
- **Features temporais**:
  - Evolução de vocabulário
  - Mudança em tópicos
  - Tendência de complexidade

### 5. **Modelo Preditivo**

#### ✅ Mantido:
- Modelos de ML para predição

#### ✅ Ajustes (ATUALIZADO):
- **Dados robustos disponíveis**:
  - **15 anos de dados** (2009-2023) permitem predições mais confiáveis
  - Série temporal adequada para modelos de ML e séries temporais
  - Possibilidade de validação com dados recentes (2022-2024)
- **Modelos apropriados**:
  - **Análise de tendências**: Regressão linear simples, médias móveis
  - **Extrapolação cuidadosa**: Não extrapolar muito além dos dados
  - **Intervalos de confiança**: Sempre incluir incerteza
- **Validação**:
  - Usar 2022-2023 para treino, 2024 para validação
  - Métricas de erro claras
  - **Não confiar cegamente** nas predições

#### 💡 Abordagem Alternativa:
- **Análise comparativa** ao invés de predição:
  - Comparar 2022 vs 2023 vs 2024
  - Identificar mudanças e tendências
  - Projeções qualitativas (não quantitativas precisas)

### 6. **Avaliação e Visualização**

#### ✅ Mantido:
- Métricas de avaliação
- Visualizações

#### 🔄 Ajustes:
- **Métricas apropriadas**:
  - Para predições: MAE, RMSE, R²
  - Para análise: Estatísticas descritivas
  - **Sempre incluir incerteza**
- **Visualizações educacionais**:
  - Gráficos claros e acessíveis
  - Legendas em português
  - Cores acessíveis (WCAG)
  - Explicações contextuais

---

## 📋 Estrutura de Implementação Proposta

### Fase 1: Preparação de Dados (Semana 1)
```
scripts/analise_enem/
├── 01_carregar_dados.py      # Carregar e normalizar dados
├── 02_preprocessar_texto.py  # Limpeza e tokenização
└── 03_validar_dados.py        # Validação de qualidade
```

### Fase 2: Análise Semântica (Semana 2)
```
scripts/analise_enem/
├── 04_gerar_embeddings.py     # Embeddings com modelos PT
├── 05_analise_lexical.py      # Frequência, vocabulário
├── 06_modelagem_topicos.py   # LDA, NMF
└── 07_complexidade_texto.py   # Métricas de complexidade
```

### Fase 3: Análise de Dificuldade (Semana 3)
```
scripts/analise_enem/
├── 08_heuristica_dificuldade.py  # Métricas heurísticas
├── 09_similaridade_provas.py      # Similaridade entre anos
└── 10_validar_dificuldade.py      # Validação com especialistas
```

### Fase 4: Análise Temporal (Semana 4)
```
scripts/analise_enem/
├── 11_serie_temporal.py       # Preparar série temporal
├── 12_identificar_padroes.py   # Padrões e tendências
└── 13_analise_por_area.py     # Análise por área de conhecimento
```

### Fase 5: Modelagem Preditiva (Semana 5)
```
scripts/analise_enem/
├── 14_modelo_tendencias.py    # Modelos de tendências
├── 15_validar_predicoes.py    # Validação cruzada
└── 16_intervalos_confianca.py # Incerteza e intervalos
```

### Fase 6: Visualização e Relatórios (Semana 6)
```
scripts/analise_enem/
├── 17_visualizacoes.py        # Gráficos e dashboards
├── 18_gerar_relatorio.py      # Relatório final
└── 19_dashboard_interativo.py # Dashboard web (opcional)
```

---

## ⚠️ Avisos Importantes

### 1. ✅ Dados Históricos Disponíveis
- **15 anos de dados** (2009-2023) do repositório [extract-enem-data](https://github.com/gabriel-antonelli/extract-enem-data)
- **Série temporal robusta** para análises e predições
- **Dados organizados por área** (Linguagens, Humanas, Natureza, Matemática)
- **Formato CSV** com questões, alternativas, respostas e imagens
- **Integração** com dados existentes (2022, 2023, 2024) para série completa

### 2. Precisão Educacional
- **Impacto crítico**: Resultados afetam estudantes
- **Validar sempre** com especialistas
- **Documentar** todas as metodologias
- **Não fazer afirmações** sem evidências

### 3. Dados Reais Apenas
- **NUNCA criar dados fictícios**
- **Usar apenas** dados fornecidos
- **Se não houver dados**, informar claramente

### 4. Integração com Dados Reais
- Se você tem **190k+ registros** de desempenho real:
  - **Usar para validar** dificuldade
  - **Treinar modelos** com dados reais
  - **Correlacionar** com análises semânticas

---

## 🎯 Objetivos Realistas

### Objetivos Primários:
1. ✅ **Análise comparativa** entre 2022, 2023, 2024
2. ✅ **Identificação de tendências** qualitativas
3. ✅ **Análise semântica e lexical** robusta
4. ✅ **Similaridade entre provas** por área

### Objetivos Secundários:
1. ⚠️ **Predições quantitativas** (com ressalvas de incerteza)
2. ⚠️ **Projeções futuras** (qualitativas, não precisas)
3. ✅ **Insights educacionais** baseados em evidências

---

## 📊 Métricas de Sucesso

### Técnicas:
- [ ] Embeddings gerados para todas as questões
- [ ] Tópicos identificados por área e ano
- [ ] Similaridade calculada entre provas
- [ ] Tendências identificadas (com incerteza)

### Educacionais:
- [ ] Validação com especialistas em ENEM
- [ ] Relatório compreensível para educadores
- [ ] Visualizações acessíveis e claras
- [ ] Insights acionáveis para orientação estudantil

---

## 🚀 Próximos Passos

1. **Revisar e aprovar** este plano ajustado
2. **Definir prioridades** (quais fases implementar primeiro)
3. **Validar disponibilidade** de dados adicionais (190k+ registros)
4. **Iniciar Fase 1**: Carregamento e pré-processamento

---

## 💡 Sugestões Adicionais

### Integração com API Maritaca:
- Usar para análise de complexidade semântica
- Geração de resumos temáticos
- Classificação de questões por tipo

### Dashboard Interativo:
- Visualizações interativas (Plotly, Streamlit)
- Filtros por área, ano, tipo de questão
- Exportação de relatórios

### Validação Contínua:
- Comparar predições com ENEM 2025 (quando disponível)
- Ajustar modelos com novos dados
- Melhorar precisão ao longo do tempo

---

**Última atualização**: 2024  
**Status**: Aguardando aprovação e ajustes

