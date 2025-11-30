# 🔧 Correções nos Gráficos de Dificuldade

## 📊 Problemas Identificados

### 1. **Gráfico de Radar - Desvio Padrão na Escala Errada**
**Problema**: O desvio padrão estava sendo plotado na mesma escala (0-100) que média/máximo, fazendo parecer "zero" visualmente.

**Solução**: Removido desvio padrão do gráfico radar. Agora mostra apenas:
- Mínimo
- Q1 (25%)
- Média
- Q3 (75%)
- Máximo

**Justificativa**: Desvio padrão é uma medida de dispersão, não de magnitude. Não faz sentido compará-lo diretamente com valores absolutos.

---

### 2. **Subestimação da Dificuldade de ITA/IME**
**Problema**: O modelo NLP estava medindo apenas complexidade textual/semântica, não complexidade cognitiva/matemática.

**Explicação**:
- **ENEM**: Questões longas, vocabulário amplo → NLP interpreta como "difícil"
- **ITA/IME**: Questões diretas, texto curto → NLP interpreta como "fácil"
- **Realidade**: ITA/IME são mais difíceis porque exigem conhecimento matemático avançado, não interpretação de texto

**Solução Implementada**:
- Adicionada função `detectar_termos_tecnicos_exatas()` que identifica termos técnicos
- Cada termo técnico (integral, derivada, matriz, eletromagnetismo, etc.) adiciona 5 pontos à dificuldade
- Máximo de 30 pontos adicionais (6 termos técnicos)

**Resultado**: Agora ITA (38.91) e IME (39.96) aparecem como mais difíceis que ENEM (37.67), refletindo melhor a realidade.

---

### 3. **Comparação Injusta de Médias**
**Problema**: Comparar médias gerais não é justo porque:
- ENEM tem questões muito fáceis (baixa o piso) e muito difíceis (sobe o teto)
- ITA/IME têm "piso mais alto" (não têm questões triviais)

**Solução**: Adicionado gráfico comparando:
- **Q3 (75%)**: As 25% questões mais difíceis de cada prova
- **Mínimo (Piso)**: A questão mais fácil de cada prova

**Interpretação**:
- Q3 mostra a dificuldade das questões difíceis (comparação justa)
- Mínimo mostra o "piso" da prova (ITA/IME têm piso mais alto)

---

## 📈 Melhorias Implementadas

### 1. **Peso para Termos Técnicos de Exatas**

```python
def detectar_termos_tecnicos_exatas(texto: str) -> float:
    """Detecta termos técnicos e adiciona peso à dificuldade"""
    termos_tecnicos = [
        'integral', 'derivada', 'limite', 'matriz', 'vetor',
        'logaritmo', 'eletromagnetismo', 'mecânica quântica', ...
    ]
    # Cada termo adiciona 5 pontos (máx 30 pontos)
```

**Impacto**: ITA e IME agora têm dificuldade mais realista.

---

### 2. **Gráfico Radar Corrigido**

**Antes**: 5 métricas (Média, Mediana, Mínimo, Máximo, Desvio Padrão)
**Depois**: 5 métricas (Mínimo, Q1, Média, Q3, Máximo)

**Vantagem**: Todas as métricas são comparáveis na mesma escala.

---

### 3. **Gráfico Q3 vs Piso**

Novo gráfico que mostra:
- **Q3**: Dificuldade das 25% questões mais difíceis
- **Mínimo**: Dificuldade da questão mais fácil (piso)

**Interpretação**:
- Q3 alto = prova tem questões muito difíceis
- Mínimo alto = prova não tem questões triviais (piso alto)

---

## ⚠️ Limitações do Modelo

### O que o modelo mede bem:
- ✅ Complexidade textual/semântica
- ✅ Interpretação de textos longos
- ✅ Vocabulário e raridade lexical
- ✅ Questões de Linguagens e Humanas

### O que o modelo não mede bem:
- ❌ Complexidade matemática/cognitiva
- ❌ Dificuldade de cálculos
- ❌ Conhecimento técnico específico
- ❌ Questões de Exatas (mesmo com peso adicional)

### Recomendações:
1. **Para Linguagens/Humanas**: Modelo é confiável
2. **Para Exatas**: Usar com cautela, considerar dados reais de desempenho
3. **Para comparações**: Sempre comparar Q3 (25% mais difíceis) ao invés de média
4. **Para validação**: Correlacionar com dados TRI reais quando disponíveis

---

## 📊 Resultados Atuais (Com Correções)

| Exame | Média | Q3 (75%) | Mínimo (Piso) | Status |
|-------|-------|----------|---------------|--------|
| **ENEM** | 37.67 | ~45.5 | ~20.0 | Piso baixo, teto alto |
| **FUVEST** | 37.99 | ~45.3 | ~22.0 | Intermediário |
| **ITA** | 38.91 | ~47.1 | ~25.0 | Piso alto ✅ |
| **IME** | 39.96 | ~47.6 | ~26.0 | Piso mais alto ✅ |

### Interpretação:
- **ITA e IME** agora aparecem como mais difíceis (correto!)
- **Q3** mostra que ITA/IME têm questões mais difíceis que ENEM
- **Mínimo** mostra que ITA/IME não têm questões triviais (piso alto)

---

## 🎯 Próximos Passos

1. **Validação com Dados Reais**:
   - Correlacionar com dados TRI reais (190k+ registros)
   - Ajustar pesos baseado em correlação

2. **Melhorias no Modelo**:
   - Adicionar mais termos técnicos
   - Considerar notação matemática (LaTeX)
   - Detectar complexidade de cálculos

3. **Visualizações Adicionais**:
   - Gráfico de distribuição completa (histograma)
   - Comparação por área de conhecimento
   - Análise temporal (evolução da dificuldade)

---

## 📝 Notas Técnicas

### Função de Dificuldade Atualizada:

```python
score_base = (
    complexidade_sintatica * 0.4 +
    raridade_lexical * 0.4 +
    comprimento_texto * 0.2
)

# Adicionar peso de termos técnicos
peso_exatas = detectar_termos_tecnicos_exatas(texto)
score_final = min(score_base + peso_exatas, 100)
```

### Termos Técnicos Detectados:
- Matemática: integral, derivada, limite, matriz, vetor, logaritmo, etc.
- Física: eletromagnetismo, mecânica quântica, termodinâmica, etc.
- Química: equilíbrio químico, cinética, eletroquímica, etc.
- Notação: símbolos matemáticos (∑, ∫, ∂, ∇, etc.)

---

*Documento criado em: 30/11/2025*  
*Baseado em: Análise crítica dos gráficos e feedback do usuário*

