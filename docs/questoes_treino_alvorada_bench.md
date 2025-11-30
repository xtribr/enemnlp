# 📚 Questões de Treino - Alvorada-bench

## ✅ Integração Concluída

Foram integradas **2.886 questões de treino** de exames brasileiros do dataset [Alvorada-bench](https://huggingface.co/datasets/HenriqueGodoy/Alvorada-bench).

## 📊 Distribuição por Exame

| Exame | Questões | Descrição |
|-------|----------|-----------|
| **FUVEST** | 1.303 | Vestibular da USP |
| **ITA** | 720 | Instituto Tecnológico de Aeronáutica |
| **IME** | 147 | Instituto Militar de Engenharia |
| **UNICAMP** | 716 | Vestibular da UNICAMP |
| **Total** | **2.886** | - |

## 📊 Distribuição por Área

### FUVEST (1.303 questões)
- **Natural-sciences**: 502 questões
- **Human-sciences**: 422 questões
- **Languages**: 256 questões
- **Mathematics**: 102 questões
- **Unknown**: 21 questões

### ITA (720 questões)
- **Natural-sciences**: 366 questões
- **Mathematics**: 200 questões
- **Languages**: 144 questões
- **Human-sciences**: 4 questões
- **Unknown**: 6 questões

### IME (147 questões)
- **Mathematics**: 77 questões
- **Natural-sciences**: 70 questões

### UNICAMP (716 questões)
- **Human-sciences**: 250 questões
- **Natural-sciences**: 241 questões
- **Languages**: 117 questões
- **Mathematics**: 100 questões
- **Unknown**: 8 questões

## 📁 Estrutura dos Arquivos

### Arquivos Individuais
- `data/treino/treino_fuvest.jsonl` - 1.303 questões
- `data/treino/treino_ita.jsonl` - 720 questões
- `data/treino/treino_ime.jsonl` - 147 questões
- `data/treino/treino_unicamp.jsonl` - 716 questões

### Arquivo Consolidado
- `data/treino/treino_alvorada_bench_completo.jsonl` - 2.886 questões (todas)

## 📋 Formato das Questões

Cada questão contém:

```json
{
  "id": "question_id_original",
  "exam": "2024",
  "exam_type": "fuvest",  // ou "ita", "ime", "unicamp"
  "exam_name": "exams_pt-br_fuvest_2024",
  "area": "mathematics",  // languages, human-sciences, natural-sciences, mathematics
  "subject": "Matemática",  // Subject original do dataset
  "number": "1",
  "context": "",
  "question": "Texto da questão...",
  "alternatives": ["A. ...", "B. ...", "C. ...", "D. ...", "E. ..."],
  "label": "C",  // Resposta correta
  "has_images": false,
  "source": "alvorada-bench"  // Marca de origem
}
```

### Campos Importantes

- **`exam_type`**: Identifica o exame (fuvest, ita, ime, unicamp)
- **`exam_name`**: Nome completo do exame (inclui ano)
- **`source`**: Sempre "alvorada-bench" para identificar origem
- **`area`**: Área mapeada para formato padrão (compatível com ENEM)
- **`subject`**: Subject original do dataset (preservado)

## 🎯 Uso para Treino

### Vantagens

1. **Diversidade de exames**: Questões de diferentes vestibulares brasileiros
2. **Alto nível**: ITA e IME são exames muito difíceis, excelentes para treino
3. **Cobertura temporal**: Questões de vários anos
4. **Respostas corretas**: Todas as questões têm gabarito
5. **Formato padronizado**: Compatível com o sistema existente

### Recomendações de Uso

1. **Treino balanceado**: Usar questões de todos os exames
2. **Foco em dificuldade**: ITA e IME são mais difíceis, bons para desafio
3. **Áreas específicas**: Filtrar por área para treino focado
4. **Validação**: Usar apenas ENEM para validação final

## 🔧 Como Usar

### Carregar questões de um exame específico

```python
import json
from pathlib import Path

treino_dir = Path("data/treino")

# Carregar questões FUVEST
questoes_fuvest = []
with open(treino_dir / "treino_fuvest.jsonl", 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            questoes_fuvest.append(json.loads(line))

print(f"Total: {len(questoes_fuvest)} questões FUVEST")
```

### Filtrar por área

```python
# Filtrar apenas matemática
matematica = [q for q in questoes_fuvest if q['area'] == 'mathematics']
print(f"Matemática: {len(matematica)} questões")
```

### Carregar todas as questões

```python
# Carregar arquivo consolidado
questoes_treino = []
with open(treino_dir / "treino_alvorada_bench_completo.jsonl", 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            questoes_treino.append(json.loads(line))

print(f"Total: {len(questoes_treino)} questões de treino")
```

## 📈 Estatísticas Gerais

- **Total de questões**: 2.886
- **Exames**: 4 (FUVEST, ITA, IME, UNICAMP)
- **Anos cobertos**: Vários (depende do exame)
- **Áreas cobertas**: Todas (Linguagens, Humanas, Natureza, Matemática)
- **Taxa de respostas corretas**: 100% (todas têm gabarito)

## 🔄 Atualização

Para atualizar os dados de treino:

```bash
python scripts/analise_enem/44_integrar_alvorada_bench.py
```

---

*Documentação gerada em: 29/11/2025*  
*Dataset fonte: [Alvorada-bench](https://huggingface.co/datasets/HenriqueGodoy/Alvorada-bench)*

