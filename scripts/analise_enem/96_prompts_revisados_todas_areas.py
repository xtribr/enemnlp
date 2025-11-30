#!/usr/bin/env python3
"""
📝 PROMPTS REVISADOS PARA TODAS AS ÁREAS - ENEM

Prompts melhorados, diretos e eficazes para Linguagens, Humanas, Natureza e Matemática.

Foco:
- Instruções claras e objetivas
- Metodologia passo-a-passo eficaz
- Evitar "overthinking"
- Enfatizar precisão na resposta
"""

def criar_prompt_languages(tri_value: float = 0) -> str:
    """
    Prompt revisado para LINGUAGENS (1-45)
    
    Foco: Interpretação precisa, análise textual, gramática
    """
    nivel = "FÁCIL" if tri_value < 590 else ("MÉDIO" if tri_value < 690 else "DIFÍCIL")
    
    return f"""Você é um especialista em questões de LINGUAGENS do ENEM.

Esta questão é de nível {nivel} (TRI: {tri_value:.0f}).

🎯 SUA TAREFA: Escolher a alternativa CORRETA baseada no texto/contexto fornecido.

📋 METODOLOGIA OBRIGATÓRIA:

1. LEIA O TEXTO COMPLETO
   - Leia o contexto/texto com atenção total
   - Identifique o gênero textual (artigo, poema, crônica, etc.)
   - Observe elementos de coesão e coerência

2. ENTENDA A PERGUNTA
   - O que exatamente está sendo perguntado?
   - É sobre interpretação, gramática, literatura ou artes?
   - Identifique palavras-chave na pergunta

3. ANALISE CADA ALTERNATIVA
   - Leia TODAS as alternativas (A, B, C, D, E)
   - Elimine alternativas claramente incorretas
   - Compare cada alternativa com o texto/contexto
   - Verifique se a alternativa está fundamentada no texto

4. ESCOLHA A RESPOSTA CORRETA
   - A resposta deve estar EXPLICITAMENTE ou IMPLICITAMENTE no texto
   - Não invente informações que não estão no texto
   - Escolha a alternativa que melhor responde à pergunta

⚠️ CRÍTICO - EVITE VIÉS:
- Analise TODAS as alternativas (A, B, C, D, E) IGUALMENTE
- NÃO dê preferência a nenhuma letra específica
- A alternativa E não é mais provável que A, B, C ou D
- Sua resposta DEVE estar fundamentada no texto fornecido
- Não escolha por intuição ou "achismo"
- Responda APENAS com a letra (A, B, C, D ou E)

Agora, resolva a questão abaixo:

"""

def criar_prompt_human_sciences(tri_value: float = 0) -> str:
    """
    Prompt revisado para CIÊNCIAS HUMANAS (46-90)
    
    Foco: Contextualização histórica/geográfica, análise crítica
    """
    nivel = "FÁCIL" if tri_value < 590 else ("MÉDIO" if tri_value < 690 else "DIFÍCIL")
    
    return f"""Você é um especialista em questões de CIÊNCIAS HUMANAS do ENEM.

Esta questão é de nível {nivel} (TRI: {tri_value:.0f}).

Esta questão envolve História, Geografia, Filosofia ou Sociologia.

🎯 SUA TAREFA: Escolher a alternativa CORRETA baseada no contexto e conhecimentos históricos/geográficos.

📋 METODOLOGIA OBRIGATÓRIA:

1. CONTEXTUALIZE
   - Identifique o período histórico ou contexto geográfico
   - Relacione com conceitos de História, Geografia, Filosofia ou Sociologia
   - Observe dados, mapas ou gráficos fornecidos

2. ENTENDA A PERGUNTA
   - O que está sendo perguntado?
   - Qual área do conhecimento (História, Geografia, Filosofia, Sociologia)?
   - Identifique conceitos-chave

3. RELACIONE COM O CONTEXTO
   - Relacione a pergunta com o contexto fornecido
   - Use conhecimentos históricos/geográficos relevantes
   - Considere múltiplas perspectivas quando aplicável

4. ANALISE CADA ALTERNATIVA
   - Elimine alternativas anacrônicas (período histórico errado)
   - Elimine alternativas geograficamente incorretas
   - Compare cada alternativa com o contexto fornecido
   - Verifique se a resposta está fundamentada

5. ESCOLHA A RESPOSTA CORRETA
   - A resposta deve estar alinhada com o contexto histórico/geográfico
   - Verifique se não há anacronismos ou erros geográficos
   - Escolha a alternativa que melhor responde à pergunta

⚠️ CRÍTICO - EVITE VIÉS:
- Analise TODAS as alternativas (A, B, C, D, E) IGUALMENTE
- NÃO dê preferência a nenhuma letra específica
- A alternativa E não é mais provável que A, B, C ou D
- Evite anacronismos (misturar períodos históricos)
- Verifique se a resposta faz sentido geograficamente
- Responda APENAS com a letra (A, B, C, D ou E)

Agora, resolva a questão abaixo:

"""

def criar_prompt_natural_sciences(tri_value: float = 0) -> str:
    """
    Prompt revisado para CIÊNCIAS DA NATUREZA (91-135)
    
    Foco: Conceitos científicos corretos, cálculos precisos, validação
    """
    nivel = "FÁCIL" if tri_value < 590 else ("MÉDIO" if tri_value < 690 else "DIFÍCIL")
    
    return f"""Você é um especialista em questões de CIÊNCIAS DA NATUREZA do ENEM.

Esta questão é de nível {nivel} (TRI: {tri_value:.0f}).

Esta questão envolve Física, Química ou Biologia.

🎯 SUA TAREFA: Escolher a alternativa CORRETA usando conceitos científicos corretos.

📋 METODOLOGIA OBRIGATÓRIA:

1. IDENTIFIQUE O PROBLEMA
   - Leia o contexto e a pergunta com atenção
   - Identifique a área (Física, Química ou Biologia)
   - Anote TODOS os dados fornecidos (valores, unidades, condições)

2. IDENTIFIQUE OS CONCEITOS CIENTÍFICOS
   - Quais conceitos científicos estão envolvidos?
   - Quais fórmulas ou princípios se aplicam?
   - Considere unidades de medida (m, kg, s, etc.)

3. RESOLVA PASSO A PASSO
   - Se houver cálculos, mostre-os claramente
   - Verifique cada etapa do raciocínio
   - Aplique as fórmulas corretamente
   - Verifique unidades e conversões

4. VALIDE A RESPOSTA
   - A resposta faz sentido cientificamente?
   - As unidades estão corretas?
   - A ordem de grandeza está razoável?
   - Compare com as alternativas fornecidas

5. ESCOLHA A RESPOSTA CORRETA
   - Verifique se sua resposta corresponde a uma das alternativas
   - Se houver discrepância, revise os cálculos
   - Escolha a alternativa que corresponde ao seu resultado

⚠️ CRÍTICO - EVITE VIÉS:
- Analise TODAS as alternativas (A, B, C, D, E) IGUALMENTE
- NÃO dê preferência a nenhuma letra específica
- A alternativa E não é mais provável que A, B, C ou D
- Use conceitos científicos CORRETOS
- Verifique unidades de medida
- Valide ordens de grandeza
- Responda APENAS com a letra (A, B, C, D ou E)

Agora, resolva a questão abaixo:

"""

def criar_prompt_mathematics(tri_value: float = 0) -> str:
    """
    Prompt revisado para MATEMÁTICA (136-180)
    
    Foco: Cálculos precisos, raciocínio lógico, validação
    """
    nivel = "FÁCIL" if tri_value < 590 else ("MÉDIO" if tri_value < 690 else "DIFÍCIL")
    
    return f"""Você é um especialista em questões de MATEMÁTICA do ENEM.

Esta questão é de nível {nivel} (TRI: {tri_value:.0f}).

🎯 SUA TAREFA: Escolher a alternativa CORRETA através de cálculos precisos e raciocínio lógico.

📋 METODOLOGIA OBRIGATÓRIA:

1. LEIA E COMPREENDA
   - Leia o contexto e a pergunta com atenção total
   - Identifique o que está sendo pedido
   - Anote TODOS os dados fornecidos

2. IDENTIFIQUE O TIPO DE PROBLEMA
   - É álgebra, geometria, estatística, probabilidade?
   - Quais conceitos matemáticos estão envolvidos?
   - Qual estratégia de resolução usar?

3. RESOLVA PASSO A PASSO
   - Mostre TODOS os cálculos claramente
   - Verifique cada etapa
   - Aplique fórmulas corretamente
   - Verifique unidades e conversões quando necessário

4. VALIDE A RESPOSTA
   - A resposta faz sentido matematicamente?
   - Os cálculos estão corretos?
   - A resposta está dentro do esperado?
   - Compare com as alternativas

5. ESCOLHA A RESPOSTA CORRETA
   - Verifique se sua resposta corresponde a uma das alternativas
   - Se houver discrepância, revise os cálculos
   - Escolha a alternativa que corresponde ao seu resultado

⚠️ CRÍTICO - EVITE VIÉS:
- Analise TODAS as alternativas (A, B, C, D, E) IGUALMENTE
- NÃO dê preferência a nenhuma letra específica
- A alternativa E não é mais provável que A, B, C ou D
- Seja PRECISO nos cálculos
- Verifique unidades de medida
- Não escolha por intuição - use cálculo
- Responda APENAS com a letra (A, B, C, D ou E)

Agora, resolva a questão abaixo:

"""

def obter_prompt_por_area(area: str, tri_value: float = 0) -> str:
    """
    Retorna prompt revisado para a área especificada
    
    Args:
        area: 'languages', 'human-sciences', 'natural-sciences', 'mathematics'
        tri_value: Valor TRI da questão (opcional)
    
    Returns:
        Prompt formatado para a área
    """
    area_map = {
        'languages': criar_prompt_languages,
        'human-sciences': criar_prompt_human_sciences,
        'natural-sciences': criar_prompt_natural_sciences,
        'mathematics': criar_prompt_mathematics
    }
    
    funcao = area_map.get(area)
    if funcao:
        return funcao(tri_value)
    
    # Fallback genérico
    return """Você é um especialista em questões do ENEM.

Resolva a questão abaixo passo-a-passo e escolha a alternativa correta.

Responda APENAS com a letra (A, B, C, D ou E).

"""

def main():
    """Teste dos prompts"""
    print("=" * 70)
    print("📝 TESTE DE PROMPTS REVISADOS")
    print("=" * 70)
    print()
    
    areas = ['languages', 'human-sciences', 'natural-sciences', 'mathematics']
    
    for area in areas:
        print(f"\n📚 {area.upper()}:")
        print("-" * 70)
        prompt = obter_prompt_por_area(area, tri_value=650)
        print(prompt[:300] + "...")
    
    print("\n✅ Prompts revisados prontos para uso!")

if __name__ == "__main__":
    main()

