# 🔴 CORREÇÕES CRÍTICAS - Sistema TRI

## Problemas Identificados

### 1. ❌ Dados TRI Incompletos
- **Problema**: Sistema só tinha TRI de Matemática (questões 136-180)
- **Realidade**: Existem dados TRI para TODAS as áreas:
  - Linguagens (questões 1-45)
  - Humanas (questões 46-90)
  - Natureza (questões 91-135)
  - Matemática (questões 136-180)

### 2. ❌ Classificação TRI Incorreta
- **Problema Atual**:
  - Fácil: < 650
  - Médio: 650-750
  - Difícil: > 750

- **Régua CORRETA do ENEM**:
  - **Fácil**: 200 - 590
  - **Médio**: 590 - 690
  - **Difícil**: 700+

### 3. ❌ Prompts Genéricos para Áreas sem TRI
- **Problema**: Quando não havia TRI, usava prompts genéricos fracos
- **Solução**: Usar dados TRI completos de todas as áreas

## Ações Imediatas

1. ✅ Localizar dados TRI completos de todas as áreas
2. ✅ Corrigir função `classificar_por_tri()` com régua correta
3. ✅ Carregar TRI_DATA completo (180 questões)
4. ✅ Revisar prompts adaptativos
5. ✅ Testar sistema corrigido

## Impacto Esperado

Com essas correções, esperamos:
- Melhor classificação de dificuldade
- Prompts mais adequados por nível
- Acurácia significativamente melhor

