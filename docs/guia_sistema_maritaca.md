# 🤖 Guia: Sistema Integrado com Maritaca Sabiá 3

## ✅ Sistema Implementado

Agora **TODAS** as análises, criação de prompts e melhorias **sempre consultam a Maritaca Sabiá 3** como especialista em ENEM.

---

## 📋 Funções Disponíveis

### 1. `criar_prompt_com_maritaca(client, versao, area, exemplo_questao=None)`
**Sempre consulta Maritaca para criar prompt otimizado**

```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    configurar_api_maritaca,
    criar_prompt_com_maritaca
)

client, versao = configurar_api_maritaca()
prompt = criar_prompt_com_maritaca(client, versao, "mathematics")
```

### 2. `melhorar_prompt_existente_com_maritaca(client, versao, prompt_atual, resultados=None)`
**Sempre consulta Maritaca para melhorar prompt existente**

```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    melhorar_prompt_existente_com_maritaca
)

prompt_melhorado = melhorar_prompt_existente_com_maritaca(
    client, versao, prompt_atual, resultados
)
```

### 3. `analisar_erros_com_maritaca(client, versao, erros)`
**Sempre consulta Maritaca para analisar erros**

```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    analisar_erros_com_maritaca
)

analise = analisar_erros_com_maritaca(client, versao, lista_erros)
```

### 4. `interpretar_resultados_com_maritaca(client, versao, resultados)`
**Sempre consulta Maritaca para interpretar resultados**

```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    interpretar_resultados_com_maritaca
)

interpretacao = interpretar_resultados_com_maritaca(client, versao, resultados)
```

### 5. `consultar_maritaca(client, versao, pergunta, contexto="", max_tokens=2000)`
**Consulta genérica à Maritaca**

```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    consultar_maritaca
)

resposta = consultar_maritaca(
    client, versao, 
    "Como melhorar acurácia em matemática?",
    contexto="Acurácia atual: 35%"
)
```

---

## 🔄 Integração Automática

### Scripts que Já Usam o Sistema:

1. **`21_avaliacao_acuracia_maritaca.py`**:
   - ✅ Sempre consulta Maritaca para criar prompts otimizados
   - ✅ Usa expertise da especialista para cada área
   - ✅ Adapta prompt baseado em exemplos de questões

2. **Outros scripts podem usar**:
   - Importar `28_sistema_maritaca_integrado`
   - Usar as funções disponíveis
   - Sempre ter consulta à especialista

---

## 💡 Exemplos de Uso

### Exemplo 1: Criar Prompt para Matemática
```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    configurar_api_maritaca,
    criar_prompt_com_maritaca
)

client, versao = configurar_api_maritaca()
prompt = criar_prompt_com_maritaca(client, versao, "mathematics")
print(prompt)  # Prompt otimizado pela Maritaca
```

### Exemplo 2: Analisar Erros
```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    analisar_erros_com_maritaca
)

erros = [...]  # Lista de erros
analise = analisar_erros_com_maritaca(client, versao, erros)
print(analise)  # Análise detalhada da Maritaca
```

### Exemplo 3: Interpretar Resultados
```python
from scripts.analise_enem.28_sistema_maritaca_integrado import (
    interpretar_resultados_com_maritaca
)

resultados = {
    'total': 100,
    'acertos': 75,
    'acuracia': 75.0,
    'por_area': {...}
}

interpretacao = interpretar_resultados_com_maritaca(client, versao, resultados)
print(interpretacao)  # Insights da Maritaca
```

---

## 🎯 Benefícios

1. **Expertise Especializada**: Usa conhecimento específico da Maritaca sobre ENEM
2. **Otimização Contínua**: Prompts sempre melhorados pela especialista
3. **Análises Mais Precisas**: Interpretações baseadas em expertise real
4. **Melhorias Baseadas em Dados**: Sugestões práticas e específicas

---

## ✅ Status

- [x] Sistema criado e funcionando
- [x] Integração automática implementada
- [x] Funções testadas
- [x] Documentação completa

---

**Status**: ✅ **SISTEMA INTEGRADO E FUNCIONANDO**

**Agora**: Todas as análises e prompts sempre consultam a Maritaca Sabiá 3 como especialista ENEM!


