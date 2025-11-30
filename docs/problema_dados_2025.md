# ⚠️ Problema com Dados ENEM 2025

## 📊 Situação Atual

### Questões Processadas
- **Total processado**: 118 questões
- **Esperado**: 180 questões (45 por área)
- **Faltam**: 62 questões

### Distribuição por Área
- **Linguagens**: 38 questões (faltam 7)
- **Humanas**: 32 questões (faltam 13)
- **Natureza**: 27 questões (faltam 18)
- **Matemática**: 21 questões (faltam 24)

## 🔍 Análise do Problema

### Arquivos Originais
- `enem_2025_linguagens_humanas.json`: **89 questões** (esperado: 90)
- `enem_2025_natureza_matematica.json`: **77 questões** (esperado: 90)
- **Total nos arquivos**: 166 questões
- **Faltam nos arquivos originais**: 14 questões

### Questões Rejeitadas

#### 1. Questões Completamente Vazias: 26
- Sem `question`
- Sem `alternatives`
- Sem `texts_of_support`
- **Não podem ser recuperadas**

#### 2. Questões com Conteúdo mas Sem Alternativas: 8
- Têm `question` ou `texts_of_support`
- Mas não têm `alternatives` ou têm menos de 5
- **Podem ser parcialmente recuperadas** (preenchendo alternativas vazias)

#### 3. Questões com Contexto mas Sem Question: ~20
- Têm `texts_of_support` mas `question` vazio
- **Podem ser recuperadas** usando o contexto como pergunta

## ✅ Melhorias Implementadas

1. **Uso de `texts_of_support` como `question`** quando `question` está vazio
2. **Aceitação de questões com menos de 5 alternativas** (preenchendo com vazias)
3. **Aceitação de questões apenas com contexto** (usando contexto como pergunta)

## 🎯 Próximos Passos

### Opção 1: Obter Arquivos Completos
- Verificar se há versão completa dos arquivos JSON com todas as 180 questões
- Solicitar ao fornecedor dos dados os arquivos completos

### Opção 2: Preencher Manualmente
- Identificar quais questões faltam (por número/ID)
- Preencher manualmente as questões faltantes

### Opção 3: Aceitar Dados Parciais
- Trabalhar com as 118 questões disponíveis
- Documentar que 2025 tem dados incompletos
- Ajustar análises para considerar apenas questões válidas

## 📝 Recomendação

**Recomendo a Opção 1**: Verificar se há uma versão completa dos arquivos JSON ou se os dados foram extraídos incorretamente. Os arquivos atuais parecem estar incompletos ou corrompidos.

---

*Documento gerado em: 29/11/2025*

