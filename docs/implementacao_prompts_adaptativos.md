# 🎯 Implementação: Sistema de Prompts Adaptativos por TRI

## ✅ Status: IMPLEMENTADO

### Arquivos Criados

1. **`scripts/analise_enem/70_prompts_adaptativos_por_tri.py`**
   - Sistema completo de prompts adaptativos
   - Classificação por TRI (fácil/médio/difícil)
   - 3 níveis de prompts diferentes

2. **`scripts/analise_enem/71_avaliar_com_prompts_adaptativos.py`**
   - Script de avaliação que integra prompts adaptativos
   - Estatísticas por nível de dificuldade
   - Logging detalhado

---

## 📊 Estrutura do Sistema

### Classificação por TRI

```python
TRI < 650  → Fácil    (Prompt simplificado)
TRI 650-750 → Médio   (Prompt padrão)
TRI > 750   → Difícil (Prompt detalhado com CoT extenso)
```

### Características dos Prompts

#### 1. Prompt Fácil (TRI < 650)
- **Tamanho**: ~634 caracteres
- **Estratégia**: Simplificado, direto, sem overthinking
- **Foco**: Evitar complicar questões simples
- **Instruções**: Leia → Identifique → Resolva → Verifique → Escolha

#### 2. Prompt Médio (TRI 650-750)
- **Tamanho**: ~690 caracteres
- **Estratégia**: Prompt padrão com CoT moderado
- **Foco**: Raciocínio passo-a-passo balanceado
- **Instruções**: Identificação → Planejamento → Resolução → Validação → Escolha

#### 3. Prompt Difícil (TRI > 750)
- **Tamanho**: ~4146 caracteres
- **Estratégia**: CoT extenso e detalhado, múltiplas validações
- **Foco**: Cuidado extra e validação rigorosa
- **Instruções**: 7 passos detalhados com validações múltiplas

---

## 🚀 Como Usar

### Teste Rápido (5 questões)
```bash
python scripts/analise_enem/71_avaliar_com_prompts_adaptativos.py --limit 5
```

### Avaliação Completa (Matemática)
```bash
python scripts/analise_enem/71_avaliar_com_prompts_adaptativos.py --area matematica
```

### Todas as Áreas
```bash
python scripts/analise_enem/71_avaliar_com_prompts_adaptativos.py --area todas
```

---

## 📈 Resultados Esperados

### Impacto Esperado
- **Questões Fáceis**: +5-8% acurácia (resolver paradoxo)
- **Questões Difíceis**: +2-4% acurácia (validação extra)
- **Geral**: +3-5% acurácia total

### Métricas de Sucesso
- [ ] Questões fáceis (TRI < 650): 85%+ acurácia
- [ ] Questões médias (TRI 650-750): 80%+ acurácia
- [ ] Questões difíceis (TRI > 750): 70%+ acurácia
- [ ] Acurácia geral: 85%+ (vs 82.22% atual)

---

## 🔧 Próximos Passos

1. **Testar sistema** com amostra pequena (10-20 questões)
2. **Comparar resultados** com sistema atual (82.22%)
3. **Ajustar prompts** se necessário
4. **Implementar few-shots customizados** (próximo item)
5. **Implementar detecção de figuras simples** (terceiro item)

---

## 📝 Notas Técnicas

### Dependências
- `datasets`: Para carregar questões ENEM
- `openai`: Para API Maritaca
- Dados TRI: Já incluídos no script (ENEM 2024 Matemática)

### Configuração
```bash
export CURSORMINIMAC=sua_chave_aqui
# ou
export MARITALK_API_SECRET_KEY=sua_chave_aqui
```

---

*Documento criado em: 30/11/2025*  
*Status: Sistema implementado, aguardando testes*

