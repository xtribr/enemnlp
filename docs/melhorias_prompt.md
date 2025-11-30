# 🎯 Melhorias no Prompt para Aumentar Acurácia

## 📊 Análise dos Erros

### Problemas Identificados:

1. **Matemática tem acurácia muito baixa (33.52%)**
   - 363 erros de 546 questões
   - Área com maior dificuldade para a IA

2. **Padrões de erro comuns:**
   - C→B: 71 vezes (9.8% dos erros)
   - A→B: 71 vezes (9.8% dos erros)
   - C→D: 65 vezes (8.9% dos erros)
   - **A IA tende a escolher B com muita frequência**

3. **Áreas com boa acurácia:**
   - Linguagens: 91.98%
   - Humanas: 91.15%
   - Natureza: 71.48%

---

## ✅ Melhorias Implementadas no Prompt

### 1. Instruções Específicas por Área

Adicionadas instruções específicas para cada área de conhecimento:

- **Matemática**: Enfatiza raciocínio lógico, cálculos precisos, verificação de unidades
- **Ciências da Natureza**: Foco em conceitos científicos corretos, relações causa-efeito
- **Linguagens**: Análise de interpretação, tema central, intenção do autor
- **Humanas**: Contextualização histórica/social, relações causa-consequência

### 2. Metodologia de Resolução (Chain-of-Thought)

Adicionado processo passo a passo:
1. Ler contexto completo
2. Identificar o que a pergunta pede
3. Analisar cada alternativa individualmente
4. Eliminar alternativas incorretas
5. Comparar alternativas restantes
6. Escolher a melhor resposta

### 3. Avisos Específicos

- **NÃO escolher alternativa apenas por parecer plausível**
- **Verificar se está realmente correta**
- **Evitar escolher B por padrão** (problema identificado)
- **Para matemática**: verificar cálculos e unidades
- **Para ciências**: verificar conceitos científicos

### 4. Enfatizar Análise Igual de Todas as Alternativas

Instrução explícita para não dar preferência a nenhuma alternativa específica.

---

## 🎯 Resultados Esperados

Com essas melhorias, esperamos:

1. **Aumentar acurácia de Matemática** de 33.52% para pelo menos 60-70%
2. **Reduzir erros do tipo C→B e A→B** (escolha de B por padrão)
3. **Melhorar acurácia geral** de 73.79% para 80-85%
4. **Aproximar do objetivo de 90%** com ajustes adicionais

---

## 📝 Próximos Passos

1. **Testar prompt melhorado** em amostra de questões
2. **Avaliar melhoria** na acurácia
3. **Ajustar conforme necessário**
4. **Executar avaliação completa** com prompt otimizado

---

## 🔄 Como Usar o Prompt Melhorado

O prompt melhorado já está implementado em `21_avaliacao_acuracia_maritaca.py`.

Para testar:
```bash
export CURSORMINIMAC='sua-chave-aqui'
python scripts/analise_enem/21_avaliacao_acuracia_maritaca.py
```

---

**Status**: ✅ **PROMPT MELHORADO IMPLEMENTADO**


