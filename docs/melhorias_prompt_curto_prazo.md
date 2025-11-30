# Melhorias de Curto Prazo - Prompt e Few-Shots

## 📋 Resumo

Implementação das recomendações de curto prazo baseadas na análise de correlação TRI/Habilidade:

1. ✅ **Few-shots específicos para questões com figuras/tabelas**
2. ✅ **Instruções melhoradas para leitura cuidadosa de enunciados**

## 🎯 Problemas Identificados

### Análise de Correlação (Script 45)

- **Impacto das Figuras**: 72.2% de acerto com figuras vs 88.9% sem figuras (-16.7pp)
- **Erros em Questões Fáceis**: 37.5% dos erros são em questões TRI < 600
- **Temas Problemáticos**: Álgebra (62.5%) e Estatística (70.0%)

## 🔧 Melhorias Implementadas

### 1. Prompt Melhorado (`PROMPT_COT_MELHORADO`)

#### Instruções de Leitura Detalhadas:
- ✅ Leia o enunciado COMPLETO antes de calcular
- ✅ Identifique TODAS as informações fornecidas
- ✅ Preste atenção a palavras-chave: "máximo", "mínimo", "exatamente", etc.
- ✅ Analise figuras, gráficos ou tabelas com atenção
- ✅ Verifique unidades de medida
- ✅ Identifique o que está sendo pedido

#### Metodologia de Resolução:
1. Identificar o tipo de problema
2. Listar informações conhecidas
3. Determinar fórmula/método
4. Executar cálculos passo a passo
5. Verificar se a resposta faz sentido
6. Comparar com alternativas

### 2. Few-Shots Específicos

#### Few-Shots Básicos (3 exemplos):
- Multiplicação simples
- Equação do primeiro grau
- Cálculo de área de retângulo

**Características:**
- Estrutura passo a passo clara
- Verificação de resposta
- Formato padronizado

#### Few-Shots com Figuras/Tabelas (3 exemplos):
- **Tabela**: Identificar maior valor em tabela
- **Gráfico**: Analisar gráfico de barras
- **Figura Geométrica**: Teorema de Pitágoras com figura

**Características:**
- Análise explícita da figura/tabela
- Uso das informações visuais na resolução
- Demonstração de como interpretar dados visuais

### 3. Seleção Inteligente de Few-Shots

O script detecta automaticamente se a questão tem figuras:
- **Com figura**: 2 exemplos básicos + 2 exemplos com figuras
- **Sem figura**: Apenas 3 exemplos básicos

Isso garante que o modelo tenha exemplos relevantes para cada tipo de questão.

## 📊 Estrutura do Script

### Arquivo: `scripts/analise_enem/46_avaliar_com_prompt_melhorado.py`

**Funcionalidades:**
- ✅ Detecção automática de figuras/tabelas
- ✅ Seleção adaptativa de few-shots
- ✅ Prompt com instruções detalhadas
- ✅ Logging completo de resultados
- ✅ Análise por nível, tema e habilidade

**Uso:**
```bash
# Avaliar todas as questões de matemática
python scripts/analise_enem/46_avaliar_com_prompt_melhorado.py --area matematica

# Teste rápido com 10 questões
python scripts/analise_enem/46_avaliar_com_prompt_melhorado.py --area matematica --limit 10
```

## 📈 Resultados Esperados

### Melhorias Esperadas:
1. **Questões com Figuras**: Aumento de 72.2% → 85%+ de acurácia
2. **Questões Fáceis**: Redução de erros em questões TRI < 600
3. **Álgebra e Estatística**: Melhoria na interpretação de enunciados

### Métricas a Monitorar:
- Acurácia geral
- Acurácia com vs sem figuras
- Taxa de erro em questões fáceis (TRI < 600)
- Desempenho por tema (especialmente Álgebra e Estatística)

## 🔄 Próximos Passos

Após testar o script melhorado:

1. **Comparar resultados** com a versão anterior
2. **Analisar erros restantes** para identificar novos padrões
3. **Ajustar few-shots** se necessário
4. **Implementar melhorias de médio prazo**:
   - Prompts específicos por área
   - Temperatura mais baixa (0.05)

## 📝 Notas Técnicas

### Diferenças do Script Original:
- **Prompt**: Mais detalhado e estruturado
- **Few-shots**: Separados em básicos e com figuras
- **Seleção**: Adaptativa baseada na presença de figuras
- **Temperatura**: 0.0 (vs 0.1) para maior consistência
- **Max tokens**: 2000 (vs 1500) para respostas mais detalhadas

### Compatibilidade:
- ✅ Compatível com openai v0.x e v1.x+
- ✅ Usa API Maritaca (Sabiá-3)
- ✅ Suporta captions de imagens
- ✅ Formato de saída compatível com análise de correlação

## 🎓 Exemplos de Few-Shots

### Exemplo com Tabela:
```
PASSO 1 - Leitura cuidadosa: Identificar qual turma tem mais alunos
PASSO 2 - Análise da tabela: Extrair valores de cada turma
PASSO 3 - Comparação: Comparar valores numéricos
PASSO 4 - Verificação: Confirmar resposta
```

### Exemplo com Gráfico:
```
PASSO 1 - Leitura cuidadosa: Identificar mês com maior venda
PASSO 2 - Análise do gráfico: Ler valores de cada barra
PASSO 3 - Comparação: Encontrar maior valor
PASSO 4 - Verificação: Confirmar resposta
```

Esses exemplos demonstram explicitamente como usar informações visuais na resolução.

