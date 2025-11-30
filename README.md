# 🎓 ENEM NLP - Análise e Avaliação de Modelos de Linguagem no ENEM

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Sistema completo para análise semântica, preditiva e avaliação de modelos de linguagem nas provas do **Exame Nacional do Ensino Médio (ENEM)**.

> **\*\*\* Most of the code in this repository has been adapted from [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness). \*\*\***

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Dados](#-dados)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Análises Avançadas](#-análises-avançadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Resultados](#-resultados)
- [Citação](#-citação)

---

## 🎯 Sobre o Projeto

Este repositório contém código e dados utilizados nos seguintes artigos:

- [Evaluating GPT-4's Vision Capabilities on Brazilian University Admission Exams](https://arxiv.org/abs/2311.14169)
- [Evaluating GPT-3.5 and GPT-4 Models on Brazilian University Admission Exams](https://arxiv.org/abs/2303.17003)

Além da avaliação de modelos, o projeto oferece:

- ✅ **Análise Semântica**: Embeddings, similaridade, correlação entre áreas
- ✅ **Análise Preditiva**: Tendências temporais, modelos de dificuldade
- ✅ **Avaliação de Modelos**: Framework completo para avaliar LLMs no ENEM
- ✅ **Integração com Maritaca Sabiá-3**: Sistema completo de avaliação e análise
- ✅ **Visualizações**: Gráficos interativos e dashboards

---

## 🚀 Funcionalidades

### 1. Avaliação de Modelos de Linguagem

Avalie modelos como GPT-4, GPT-4o, Sabiá-3 e outros em questões do ENEM:

- **22 tarefas diferentes** (blind, images, captions, com/sem CoT)
- **ENEM 2022, 2023, 2024** completos
- **Few-shot learning** configurável
- **Chain-of-Thought (CoT)** para raciocínio passo-a-passo

### 2. Análise Semântica e Preditiva

- **Embeddings semânticos** para todas as questões (2009-2025)
- **Correlação semântica** entre áreas e anos
- **Similaridade intra e inter-área**
- **Análise de dificuldade** heurística e baseada em TRI
- **Modelagem de tópicos** (LDA, NMF)
- **Série temporal** e predições

### 3. Integração com Maritaca Sabiá-3

- Sistema completo de avaliação
- Análise de erros automatizada
- Sugestões de melhorias de prompt
- Testes com amostras balanceadas

### 4. Visualizações e Relatórios

- Gráficos de evolução temporal
- Matrizes de correlação semântica
- Dashboards HTML interativos
- Relatórios detalhados em JSON/CSV

---

## 📊 Dados

### Datasets Disponíveis

- **ENEM 2022, 2023, 2024**: Formatos JSONL com imagens e captions
- **ENEM 2009-2023**: Dados históricos integrados
- **ENEM 2025**: Dados parciais (em processamento)
- **Alvorada-bench**: Dataset externo para treinamento

### Acesso aos Dados

Os datasets também estão disponíveis via 🤗 Datasets:
```
https://huggingface.co/datasets/maritaca-ai/enem
```

### Estrutura dos Dados

```json
{
  "id": "enem_2024_languages_1",
  "exam": 2024,
  "area": "languages",
  "question": "Texto da pergunta...",
  "context": "Texto de apoio...",
  "alternatives": ["A) ...", "B) ...", "C) ...", "D) ...", "E) ..."],
  "label": "C",
  "description": "Descrição textual de imagens",
  "figures": ["path/to/image.png"]
}
```

---

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/xtribr/enemnlp.git
cd enemnlp
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
```

### 4. Configure as chaves de API

```bash
# OpenAI
export OPENAI_API_SECRET_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Maritaca
export CURSORMINIMAC=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# ou
export MARITALK_API_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ⚡ Uso Rápido

### Avaliar Modelos no ENEM

#### Sabiá-3 (Maritaca)

```bash
python main.py \
    --model maritalk \
    --model_args engine=sabia-3 \
    --tasks enem_cot_2024_blind,enem_cot_2024_captions \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt
```

#### GPT-4o

```bash
python main.py \
    --model chatgpt \
    --model_args engine=gpt-4o \
    --tasks enem_cot_2024_blind,enem_cot_2024_images,enem_cot_2024_captions \
    --description_dict_path description.json \
    --num_fewshot 3 \
    --conversation_template chatgpt
```

### Teste Rápido com 100 Questões por Área

```bash
python scripts/analise_enem/63_teste_100_questoes_por_area.py
```

### Análises Semânticas

```bash
# Gerar embeddings
python scripts/analise_enem/04_gerar_embeddings.py

# Matriz de correlação semântica
python scripts/analise_enem/60_matriz_correlacao_semantica.py

# Análise de similaridade detalhada
python scripts/analise_enem/61_analise_similaridade_semantica_detalhada.py

# Exemplos de similaridade
python scripts/analise_enem/62_exemplos_similaridade_semantica.py
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

### Scripts de Execução Automática

```bash
# Executar todas as análises
bash scripts/analise_enem/executar_todas_analises.sh

# Monitorar progresso
python scripts/analise_enem/monitorar_treinamento.py
```

---

## 📁 Estrutura do Projeto

```
enemnlp/
├── data/
│   ├── enem/              # Datasets ENEM (2022, 2023, 2024, 2025)
│   ├── processed/         # Dados processados e normalizados
│   ├── embeddings/        # Embeddings semânticos gerados
│   └── treino/            # Dados de treinamento
│
├── scripts/
│   └── analise_enem/      # Scripts de análise
│       ├── 01_carregar_dados_historico.py
│       ├── 04_gerar_embeddings.py
│       ├── 60_matriz_correlacao_semantica.py
│       ├── 63_teste_100_questoes_por_area.py
│       └── ...
│
├── docs/                  # Documentação completa
│   ├── guia_google_colab.md
│   ├── possibilidades_maritaca_enem.md
│   └── ...
│
├── notebooks/             # Notebooks para Google Colab
│   └── gpt4_enem_colab_setup.ipynb
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

### Performance dos Modelos no ENEM 2024

| Área | GPT-4o (blind) | GPT-4o (CoT+captions) | Sabiá-3 (blind) | Sabiá-3 (CoT+captions) |
|------|----------------|------------------------|-----------------|------------------------|
| Linguagens | 88.89 | 91.11 | 86.67 | **93.33** |
| Humanas | 100.00 | 100.00 | 100.00 | 100.00 |
| Natureza | 68.18 | 93.18 | 72.73 | 86.36 |
| Matemática | 60.00 | 91.11 | 60.00 | 82.22 |
| **Total** | **79.33** | **93.85** | **79.89** | **90.50** |

*Resultados usando 3-shot prompts com Chain-of-Thought*

### Análises Semânticas

- **Similaridade Intra-Área**: 0.890 (muito alta consistência temporal)
- **Similaridade Inter-Área Correlatas**: 0.566 (moderada)
- **Correlação Linguagens ↔ Humanas**: 0.789 (alta)
- **Correlação Natureza ↔ Matemática**: 0.649 (média-alta)

---

## 🎓 Tarefas Disponíveis

O projeto implementa **22 tarefas** diferentes para avaliação:

| Tarefa | Edição | Imagens | CoT | Descrição |
|--------|--------|---------|-----|-----------|
| `enem_cot_2024_blind` | 2024 | ❌ | ✅ | Sem imagens, com CoT |
| `enem_cot_2024_captions` | 2024 | 📝 | ✅ | Com captions, com CoT |
| `enem_cot_2024_images` | 2024 | 🖼️ | ✅ | Com imagens, com CoT |
| `enem_2024_blind` | 2024 | ❌ | ❌ | Sem imagens, sem CoT |
| ... | ... | ... | ... | ... |

*Consulte a documentação completa para todas as 22 tarefas disponíveis.*

---

## 📚 Documentação

Documentação completa disponível em `docs/`:

- [Guia Google Colab](docs/guia_google_colab.md)
- [Possibilidades Maritaca ENEM](docs/possibilidades_maritaca_enem.md)
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
@misc{pires2023evaluating,
      title={Evaluating GPT-4's Vision Capabilities on Brazilian University Admission Exams}, 
      author={Ramon Pires and Thales Sales Almeida and Hugo Abonizio and Rodrigo Nogueira},
      year={2023},
      eprint={2311.14169},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

```bibtex
@misc{nunes2023evaluating,
      title={Evaluating GPT-3.5 and GPT-4 Models on Brazilian University Admission Exams}, 
      author={Desnes Nunes and Ricardo Primi and Ramon Pires and Roberto Lotufo and Rodrigo Nogueira},
      year={2023},
      eprint={2303.17003},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autores

- **Ramon Pires** - *Trabalho original*
- **Equipe XTRI** - *Análises avançadas e integração com Maritaca*

---

## 🙏 Agradecimentos

- [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) pelo framework base
- [Maritaca AI](https://maritaca.ai) pela API Sabiá-3
- Comunidade open source brasileira

---

## 📞 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/xtribr/enemnlp/issues) no GitHub.

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**
