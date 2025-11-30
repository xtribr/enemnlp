# 🎓 BrainX - Sistema de Análise e Avaliação de Modelos de Linguagem no ENEM

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Sistema completo para análise semântica, preditiva e avaliação de modelos de linguagem nas provas do **Exame Nacional do Ensino Médio (ENEM)**, desenvolvido pela **XTRI EdTech**.

> **BrainX** é um sistema avançado de avaliação e análise educacional que utiliza modelos de linguagem para resolver questões do ENEM com acurácia superior a 82%, integrando técnicas de **prompts adaptativos por TRI**, **few-shots customizados por tema** e **detecção inteligente de figuras simples**.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Sistema Adaptativo BrainX](#-sistema-adaptativo-brainx)
- [Dados](#-dados)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Análises Avançadas](#-análises-avançadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Resultados](#-resultados)
- [Citação](#-citação)

---

## 🎯 Sobre o Projeto

**BrainX** é um sistema desenvolvido pela **XTRI EdTech** para análise e avaliação de modelos de linguagem no contexto do ENEM. O projeto integra:

- ✅ **Avaliação de Modelos**: Framework completo para avaliar LLMs no ENEM usando Maritaca Sabiá-3
- ✅ **Sistema Adaptativo**: Prompts que se ajustam automaticamente à dificuldade da questão (TRI)
- ✅ **Few-Shots Inteligentes**: Exemplos customizados por tema (Álgebra, Geometria, Estatística, etc.)
- ✅ **Detecção de Figuras**: Identificação automática de figuras simples (tabelas, gráficos básicos)
- ✅ **Análise Semântica**: Embeddings, similaridade, correlação entre áreas
- ✅ **Análise Preditiva**: Tendências temporais, modelos de dificuldade
- ✅ **Análise Comparativa**: Comparação de dificuldade entre ENEM, FUVEST, ITA e IME
- ✅ **Visualizações**: Gráficos interativos e dashboards

### 🎓 Contexto Educacional

Este projeto foi desenvolvido por **Alexandre Emerson Melo de Araújo**, Professor de Ensino Médio e CEO da **XTRI EdTech** em Natal/RN, trabalhando com dados educacionais críticos (190k+ registros) para desenvolver dashboards e análises preditivas para orientação estudantil.

---

## 🚀 Funcionalidades

### 1. Sistema Adaptativo BrainX

O **BrainX** utiliza três camadas de inteligência adaptativa:

#### 🎯 Prompts Adaptativos por TRI
- **Questões Fáceis (TRI < 650)**: Prompts diretos e objetivos
- **Questões Médias (TRI 650-750)**: Prompts com metodologia passo-a-passo
- **Questões Difíceis (TRI > 750)**: Prompts detalhados com análise profunda

#### 📚 Few-Shots Customizados por Tema
- **6 temas principais**: Álgebra, Geometria, Estatística, Grandezas, Números, Trigonometria
- **Exemplos específicos** para cada tema
- **Integração automática** com prompts adaptativos

#### 🖼️ Detecção de Figuras Simples
- **Identificação automática** de tabelas e gráficos básicos
- **Prompts específicos** para evitar "overthinking" em questões fáceis com figuras
- **Impacto esperado**: +5-8% em questões fáceis com figuras

### 2. Avaliação de Modelos de Linguagem

Avalie modelos como **Maritaca Sabiá-3** e outros em questões do ENEM:

- **ENEM 2022, 2023, 2024, 2025** completos
- **Few-shot learning** configurável (3 ou 5 exemplos)
- **Chain-of-Thought (CoT)** para raciocínio passo-a-passo
- **Análise detalhada** por nível de dificuldade, tema e presença de figuras

### 3. Análise Semântica e Preditiva

- **Embeddings semânticos** para todas as questões (2009-2025)
- **Correlação semântica** entre áreas e anos
- **Similaridade intra e inter-área**
- **Análise de dificuldade** heurística e baseada em TRI
- **Modelagem de tópicos** (LDA, NMF)
- **Série temporal** e predições

### 4. Análise Comparativa de Dificuldade

- **Comparação ENEM vs FUVEST, ITA, IME**
- **Amostras balanceadas** (147 questões por exame)
- **Métricas avançadas**: Q1, Q3, Mínimo, Máximo
- **Gráficos comparativos**: Box plots, radar charts, barras

### 5. Visualizações e Relatórios

- Gráficos de evolução temporal
- Matrizes de correlação semântica
- Dashboards HTML interativos
- Relatórios detalhados em JSON/CSV

---

## 🧠 Sistema Adaptativo BrainX

### Arquitetura

```
┌─────────────────────────────────────────┐
│         QUESTÃO DO ENEM                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   1. CLASSIFICAÇÃO POR TRI              │
│   (Fácil / Médio / Difícil)             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   2. SELEÇÃO DE PROMPT ADAPTATIVO       │
│   (Baseado no nível de dificuldade)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   3. DETECÇÃO DE FIGURAS SIMPLES       │
│   (Tabelas, gráficos básicos)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   4. FEW-SHOTS POR TEMA                 │
│   (Álgebra, Geometria, etc.)           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   5. PROMPT FINAL OTIMIZADO             │
│   (Enviado para o modelo)              │
└─────────────────────────────────────────┘
```

### Scripts Principais

- `70_prompts_adaptativos_por_tri.py` - Sistema de prompts adaptativos
- `73_fewshots_customizados_por_tema.py` - Few-shots por tema
- `75_deteccao_figuras_simples.py` - Detecção de figuras
- `77_avaliar_sistema_completo_adaptativo.py` - Avaliação completa integrada

---

## 📊 Dados

### Datasets Disponíveis

- **ENEM 2022, 2023, 2024**: Formatos JSONL com imagens e captions
- **ENEM 2009-2023**: Dados históricos integrados
- **ENEM 2025**: Dados parciais (em processamento)
- **Dados TRI**: Classificação de dificuldade por questão

### Estrutura dos Dados

```json
{
  "id": "enem_2024_mathematics_136",
  "exam": 2024,
  "area": "mathematics",
  "number": 136,
  "question": "Texto da pergunta...",
  "context": "Texto de apoio...",
  "alternatives": ["A) ...", "B) ...", "C) ...", "D) ...", "E) ..."],
  "label": "C",
  "description": "Descrição textual de imagens",
  "figures": ["path/to/image.png"],
  "tri": 701.9,
  "tema": "Geometria"
}
```

---

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/xtribr/gpt-4-enem.git
cd gpt-4-enem
```

### 2. Instale as dependências

```bash
pip install -e .
```

### 3. Dependências adicionais para análises

```bash
pip install transformers sentence-transformers
pip install scikit-learn nltk pandas numpy
pip install matplotlib seaborn plotly
pip install openai
```

### 4. Configure as chaves de API

```bash
# Maritaca (Sabiá-3)
export CURSORMINIMAC=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# ou
export MARITALK_API_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ⚡ Uso Rápido

### Avaliar com Sistema Adaptativo BrainX

```bash
# Avaliação completa (45 questões de matemática)
python scripts/analise_enem/77_avaliar_sistema_completo_adaptativo.py

# Teste rápido (10 questões)
python scripts/analise_enem/77_avaliar_sistema_completo_adaptativo.py --limit 10
```

### Avaliar Modelos no ENEM (Sistema Base)

```bash
# Sabiá-3 (Maritaca)
python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind,enem_cot_2024_captions \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt
```

### Análises Semânticas

```bash
# Gerar embeddings
python scripts/analise_enem/04_gerar_embeddings.py

# Matriz de correlação semântica
python scripts/analise_enem/60_matriz_correlacao_semantica.py

# Análise de similaridade detalhada
python scripts/analise_enem/61_analise_similaridade_semantica_detalhada.py
```

### Análise Comparativa de Dificuldade

```bash
# Comparar ENEM vs FUVEST, ITA, IME
python scripts/analise_enem/60_grafico_comparativo_dificuldade_exames.py
```

---

## 📈 Análises Avançadas

### Pipeline Completo de Análise

```bash
# 1. Carregar dados históricos
python scripts/analise_enem/01_carregar_dados_historico.py

# 2. Normalizar dados
python scripts/analise_enem/02_normalizar_dados.py

# 3. Validar dados
python scripts/analise_enem/03_validar_dados.py

# 4. Gerar embeddings
python scripts/analise_enem/04_gerar_embeddings.py

# 5. Análise de dificuldade
python scripts/analise_enem/08_heuristica_dificuldade.py

# 6. Similaridade entre provas
python scripts/analise_enem/09_similaridade_provas.py

# 7. Série temporal
python scripts/analise_enem/11_serie_temporal.py

# 8. Visualizações
python scripts/analise_enem/17_visualizacoes.py
```

---

## 📁 Estrutura do Projeto

```
gpt-4-enem/
├── data/
│   ├── enem/              # Datasets ENEM (2022, 2023, 2024, 2025)
│   ├── processed/         # Dados processados e normalizados
│   ├── embeddings/        # Embeddings semânticos gerados
│   ├── analises/          # Análises e resultados
│   └── treino/            # Dados de treinamento
│
├── scripts/
│   └── analise_enem/      # Scripts de análise
│       ├── 70_prompts_adaptativos_por_tri.py
│       ├── 73_fewshots_customizados_por_tema.py
│       ├── 75_deteccao_figuras_simples.py
│       ├── 77_avaliar_sistema_completo_adaptativo.py
│       ├── 60_grafico_comparativo_dificuldade_exames.py
│       └── ...
│
├── docs/                  # Documentação completa
│   ├── resultado_final_avaliacao_enem_2024.md
│   ├── proximos_passos_modelo.md
│   ├── correcoes_graficos_dificuldade.md
│   └── ...
│
├── reports/               # Relatórios e visualizações
│   ├── visualizacoes/     # Gráficos e heatmaps
│   └── avaliacoes/        # Resultados de avaliações
│
├── lm_eval/               # Framework de avaliação (adaptado)
│   └── models/
│       └── maritalk.py    # Integração com Maritaca
│
└── main.py                # Script principal de avaliação
```

---

## 📊 Resultados

### Performance do BrainX no ENEM 2024

#### Resultados por Área (Sistema Base - Sabiá-3)

| Área | Acurácia | Status |
|------|----------|--------|
| **Matemática** | **82.22%** | ✅ Benchmark atingido |
| Humanas | 97.78% | ✅ Excelente |
| Linguagens | 93.33% | ✅ Excelente |
| Natureza | 84.09% | ✅ Muito bom |
| **Geral** | **86.59%** | ✅ Excelente |

*Resultados usando 3-shot prompts com Chain-of-Thought e captions*

#### Resultados por Nível de Dificuldade (Matemática)

| Nível | Acurácia | Acertos | Status |
|-------|----------|---------|--------|
| Fácil | 71.4% | 10/14 | ⚠️ Melhorável |
| Intermediário | 87.5% | 14/16 | ✅ Ótimo |
| **Difícil** | **100%** | **5/5** | 🌟 Perfeito |
| Muito Difícil | 80.0% | 8/10 | ✅ Ótimo |

#### Resultados por Tema (Matemática)

| Tema | Acurácia | Acertos | Status |
|------|----------|---------|--------|
| 🌟 **Geometria** | **100%** | **7/7** | Perfeito |
| 🌟 **Análise Combinatória** | **100%** | **1/1** | Perfeito |
| ✅ Grandezas e Medidas | 90.0% | 9/10 | Excelente |
| ✅ Números e Operações | 88.9% | 8/9 | Ótimo |
| ⚠️ Estatística e Probabilidade | 70.0% | 7/10 | Regular |
| ❌ Álgebra e Funções | 62.5% | 5/8 | Precisa atenção |

### Impacto Esperado do Sistema Adaptativo BrainX

| Melhoria | Impacto Esperado | Status |
|----------|------------------|--------|
| Prompts Adaptativos por TRI | +5-8% acurácia | ✅ Implementado |
| Few-Shots Customizados | +3-5% em temas específicos | ✅ Implementado |
| Detecção de Figuras Simples | +5-8% em questões fáceis | ✅ Implementado |
| **Total Esperado** | **+8-15%** | 🚀 Em teste |

### Análises Semânticas

- **Similaridade Intra-Área**: 0.890 (muito alta consistência temporal)
- **Similaridade Inter-Área Correlatas**: 0.566 (moderada)
- **Correlação Linguagens ↔ Humanas**: 0.789 (alta)
- **Correlação Natureza ↔ Matemática**: 0.649 (média-alta)

### Análise Comparativa de Dificuldade

Comparação balanceada (147 questões por exame):

| Exame | Média | Q3 (75%) | Mínimo | Status |
|-------|-------|----------|--------|--------|
| ENEM | 36.09 | 42.5 | 18.2 | Baseline |
| FUVEST | 36.66 | 43.1 | 19.8 | Similar |
| ITA | 36.29 | 45.2 | **28.5** | Piso mais alto |
| IME | 37.13 | 44.8 | **27.1** | Piso mais alto |

*Dados históricos (2009-2025) com amostras balanceadas*

---

## 📚 Documentação

Documentação completa disponível em `docs/`:

- [Resultado Final Avaliação ENEM 2024](docs/resultado_final_avaliacao_enem_2024.md)
- [Próximos Passos do Modelo](docs/proximos_passos_modelo.md)
- [Correções Gráficos Dificuldade](docs/correcoes_graficos_dificuldade.md)
- [Sistema de Análises](README_ANALISES.md)
- [Plano de Análise Preditiva](docs/plano_analise_preditiva_enem.md)

---

## 🔬 Uso no Google Colab

Para usar com GPU no Google Colab, consulte:

- [Notebook de Setup](notebooks/gpt4_enem_colab_setup.ipynb)
- [Guia Completo](docs/guia_google_colab.md)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Citação

Se você usar este código ou dados em sua pesquisa, por favor cite:

```bibtex
@misc{brainx2024enem,
      title={BrainX: Sistema Adaptativo de Avaliação de Modelos de Linguagem no ENEM}, 
      author={Alexandre Emerson Melo de Araújo},
      year={2024},
      organization={XTRI EdTech},
      note={Sistema de prompts adaptativos, few-shots customizados e detecção de figuras para avaliação educacional}
}
```

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autor

**Alexandre Emerson Melo de Araújo**

- Professor de Ensino Médio
- CEO da **XTRI EdTech** (Natal/RN)
- Especialista em ENEM e TRI
- Trabalhando com dados educacionais críticos (190k+ registros)

---

## 🙏 Agradecimentos

- [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) pelo framework base
- [Maritaca AI](https://maritaca.ai) pela API Sabiá-3
- Comunidade open source brasileira
- Estudantes e educadores que tornam este projeto possível

---

## 📞 Contato

Para dúvidas ou sugestões:

- Abra uma [issue](https://github.com/xtribr/gpt-4-enem/issues) no GitHub
- **XTRI EdTech**: [Website](https://xtri.com.br) | [Email](mailto:contato@xtri.com.br)

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**

---

*Desenvolvido com ❤️ para a educação brasileira*
