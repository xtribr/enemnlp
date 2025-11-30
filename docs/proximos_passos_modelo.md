# 🚀 Próximos Passos para o Modelo ENEM

## 📊 Situação Atual

### ✅ Conquistas
- **Benchmark atingido**: 82.22% em Matemática (igual ao paper Sabiá-3)
- **Sistema estável**: Framework completo de avaliação funcionando
- **Dados completos**: 16 anos de dados históricos (2009-2025, ~2.900 questões)
- **Análises implementadas**: Semântica, dificuldade, similaridade, comparações
- **Integração Maritaca**: Funcionando perfeitamente

### ⚠️ Pontos de Atenção
- **Questões fáceis com figuras**: 71.4% acerto (paradoxo - erra mais que difíceis)
- **Álgebra e funções**: 62.5% (pior tema)
- **Estatística**: 70% (segundo pior)
- **Overthinking**: Modelo complica questões simples

---

## 🎯 Plano de Próximos Passos (Priorizado)

### 🔥 PRIORIDADE MUITO ALTA (Impacto Imediato)

#### 1. **Sistema de Prompts Adaptativos por Dificuldade**
**Objetivo**: Resolver o paradoxo "fácil vs difícil"

**O que fazer**:
- Criar 3 níveis de prompt baseados em TRI:
  - **TRI < 650 (Fácil)**: Prompt simplificado, direto, sem overthinking
  - **TRI 650-750 (Médio)**: Prompt padrão atual
  - **TRI > 750 (Difícil)**: Prompt detalhado com CoT extenso

**Impacto esperado**: +5-8% acurácia geral
**Esforço**: Médio (2-3 dias)
**Prioridade**: ⭐⭐⭐⭐⭐

**Implementação**:
```python
def selecionar_prompt_por_tri(tri_score):
    if tri_score < 650:
        return prompt_simples_direto  # Sem CoT complexo
    elif tri_score < 750:
        return prompt_padrao_atual
    else:
        return prompt_detalhado_cot_extenso
```

---

#### 2. **Few-Shots Customizados por Tema**
**Objetivo**: Melhorar Álgebra (62.5%) e Estatística (70%)

**O que fazer**:
- Criar bancos de few-shots específicos:
  - **Álgebra**: 5-7 exemplos de questões de álgebra resolvidas
  - **Estatística**: 5-7 exemplos de estatística/probabilidade
  - **Geometria**: Manter exemplos atuais (já está 100%)
  - **Grandezas**: Manter exemplos atuais (já está 90%)

**Impacto esperado**: +3-5% em Álgebra e Estatística
**Esforço**: Baixo-Médio (1-2 dias)
**Prioridade**: ⭐⭐⭐⭐

**Implementação**:
```python
def selecionar_fewshots_por_tema(tema):
    bancos = {
        'algebra': fewshots_algebra,
        'estatistica': fewshots_estatistica,
        'geometria': fewshots_geometria,
        'grandezas': fewshots_grandezas
    }
    return bancos.get(tema, fewshots_padrao)
```

---

#### 3. **Sistema de Detecção de Figuras Simples**
**Objetivo**: Resolver problema de interpretação de tabelas/diagramas básicos

**O que fazer**:
- Detectar quando figura é simples (tabela, gráfico básico)
- Aplicar prompt específico: "Esta é uma questão simples. Leia a tabela diretamente."
- Evitar análise complexa em questões com figuras simples

**Impacto esperado**: +3-5% em questões fáceis com figuras
**Esforço**: Médio (2 dias)
**Prioridade**: ⭐⭐⭐⭐

---

### 📈 PRIORIDADE ALTA (Médio Prazo)

#### 4. **Análise de Erros Sistemática**
**Objetivo**: Entender padrões de erro para melhorias direcionadas

**O que fazer**:
- Sistema automático de análise de erros após cada avaliação
- Classificação de erros por:
  - Tipo (cálculo, interpretação, conceito)
  - Tema
  - Nível TRI
  - Presença de figura
- Dashboard de erros em tempo real

**Impacto esperado**: Base para todas as melhorias futuras
**Esforço**: Médio (3-4 dias)
**Prioridade**: ⭐⭐⭐⭐

---

#### 5. **Ensemble de Modelos para Casos Borderline**
**Objetivo**: Aumentar confiança em questões difíceis

**O que fazer**:
- Para questões com TRI > 750, usar múltiplas abordagens:
  - Prompt padrão
  - Prompt com CoT extenso
  - Prompt com few-shots específicos
- Votação majoritária ou confiança ponderada

**Impacto esperado**: +2-4% em questões muito difíceis
**Esforço**: Alto (5-7 dias)
**Prioridade**: ⭐⭐⭐

---

#### 6. **Validação com Dados Reais de Desempenho**
**Objetivo**: Correlacionar predições com dados reais (190k+ registros)

**O que fazer**:
- Integrar com dados reais de desempenho do Baserow
- Validar se dificuldade heurística correlaciona com dados TRI reais
- Ajustar modelo baseado em dados reais

**Impacto esperado**: Validação científica e ajustes precisos
**Esforço**: Alto (depende de acesso aos dados)
**Prioridade**: ⭐⭐⭐

---

### 🔬 PRIORIDADE MÉDIA (Longo Prazo)

#### 7. **Fine-tuning Específico para ENEM**
**Objetivo**: Modelo especializado em questões ENEM

**O que fazer**:
- Dataset de treino: ~2.000 questões ENEM (2009-2024)
- Fine-tuning do Sabiá-3 ou modelo base
- Foco em questões difíceis (TRI > 750)

**Impacto esperado**: +5-10% acurácia geral
**Esforço**: Muito Alto (2-4 semanas)
**Prioridade**: ⭐⭐

---

#### 8. **Sistema de Aprendizado Adaptativo**
**Objetivo**: Modelo que aprende com erros

**O que fazer**:
- Sistema que identifica padrões de erro
- Ajusta estratégia automaticamente
- Aprende com questões similares já resolvidas

**Impacto esperado**: Melhoria contínua ao longo do tempo
**Esforço**: Muito Alto (4-6 semanas)
**Prioridade**: ⭐⭐

---

#### 9. **Expansão para Outras Áreas**
**Objetivo**: Aplicar melhorias em todas as áreas

**O que fazer**:
- Aplicar sistema de prompts adaptativos em:
  - Linguagens (atual: 93.33%)
  - Humanas (atual: 97.78%)
  - Natureza (atual: 84.09%)
- Few-shots customizados por área

**Impacto esperado**: Consistência em todas as áreas
**Esforço**: Médio (1 semana por área)
**Prioridade**: ⭐⭐

---

## 📋 Roadmap Sugerido (3 Meses)

### Mês 1: Melhorias Imediatas
- ✅ Semana 1-2: Sistema de prompts adaptativos por TRI
- ✅ Semana 2-3: Few-shots customizados por tema
- ✅ Semana 3-4: Sistema de detecção de figuras simples

**Meta**: 85-87% acurácia em Matemática

### Mês 2: Análise e Validação
- ✅ Semana 1-2: Sistema de análise de erros
- ✅ Semana 2-3: Validação com dados reais
- ✅ Semana 3-4: Ajustes baseados em dados

**Meta**: 87-89% acurácia em Matemática

### Mês 3: Otimização Avançada
- ✅ Semana 1-2: Ensemble de modelos
- ✅ Semana 2-3: Expansão para outras áreas
- ✅ Semana 3-4: Testes finais e documentação

**Meta**: 90%+ acurácia em Matemática

---

## 🎯 Métricas de Sucesso

### Curto Prazo (1 mês)
- [ ] Matemática: 85%+ acurácia
- [ ] Questões fáceis (TRI < 650): 85%+ acurácia
- [ ] Álgebra: 70%+ acurácia
- [ ] Estatística: 75%+ acurácia

### Médio Prazo (3 meses)
- [ ] Matemática: 90%+ acurácia
- [ ] Todas as áreas: 90%+ acurácia
- [ ] Sistema de análise de erros funcionando
- [ ] Validação com dados reais concluída

### Longo Prazo (6 meses)
- [ ] Fine-tuning específico implementado
- [ ] Sistema adaptativo funcionando
- [ ] Dashboard de monitoramento em produção
- [ ] Documentação completa

---

## 💡 Recomendações Estratégicas

### 1. **Foco em Impacto vs Esforço**
Priorizar melhorias com maior impacto e menor esforço:
- ✅ Prompts adaptativos (alto impacto, médio esforço)
- ✅ Few-shots customizados (médio impacto, baixo esforço)
- ❌ Fine-tuning (alto impacto, muito alto esforço) - deixar para depois

### 2. **Validação Contínua**
- Testar cada melhoria isoladamente
- Medir impacto antes de implementar próxima
- Manter baseline (82.22%) para comparação

### 3. **Documentação**
- Documentar cada experimento
- Manter log de mudanças e resultados
- Criar guias de reprodução

### 4. **Custos**
- Monitorar custos de API Maritaca
- Otimizar chamadas (cache, batch)
- Considerar processamento local quando possível

---

## 🚀 Próximo Passo Imediato

**Recomendação**: Começar pelo **Sistema de Prompts Adaptativos por TRI**

**Por quê?**
1. Resolve o problema mais crítico (paradoxo fácil vs difícil)
2. Impacto alto (+5-8%)
3. Esforço moderado (2-3 dias)
4. Base para outras melhorias

**Como começar**:
```bash
# 1. Criar script de classificação por TRI
python scripts/analise_enem/70_classificar_por_tri.py

# 2. Criar prompts adaptativos
python scripts/analise_enem/71_criar_prompts_adaptativos.py

# 3. Testar em amostra pequena
python scripts/analise_enem/72_testar_prompts_adaptativos.py --limit 20

# 4. Avaliar impacto
python scripts/analise_enem/73_avaliar_impacto_prompts.py
```

---

## 📚 Recursos Necessários

### Técnicos
- ✅ API Maritaca (já configurada)
- ✅ Dados ENEM (já disponíveis)
- ⚠️ Dados reais de desempenho (precisa acesso Baserow)
- ⚠️ Infraestrutura para fine-tuning (se necessário)

### Humanos
- 1 desenvolvedor (você) - tempo parcial
- Validação com especialista ENEM (quando necessário)

### Tempo Estimado
- **Melhorias imediatas**: 2-3 semanas
- **Análise e validação**: 2-3 semanas
- **Otimização avançada**: 3-4 semanas
- **Total**: 7-10 semanas (2-2.5 meses)

---

## ✅ Conclusão

O modelo já atingiu o benchmark (82.22%) e está pronto para uso em produção. As melhorias sugeridas focam em:

1. **Resolver problemas específicos** (questões fáceis, álgebra, estatística)
2. **Aumentar confiabilidade** (análise de erros, validação)
3. **Otimizar para 90%+** (ensemble, fine-tuning)

**Recomendação final**: Começar pelas melhorias de **curto prazo** (prompts adaptativos e few-shots customizados) que têm maior impacto com menor esforço.

---

*Documento criado em: 30/11/2025*  
*Baseado em: Análise do estado atual do projeto e documentação existente*

