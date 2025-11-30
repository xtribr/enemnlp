#!/usr/bin/env python3
"""
🎯 Sistema de Prompts Adaptativos por TRI

Cria prompts diferentes baseados no nível de dificuldade (TRI) da questão:
- TRI 200-590 (Fácil): Prompt simplificado, direto, sem overthinking
- TRI 590-690 (Médio): Prompt padrão com CoT moderado
- TRI 700+ (Difícil): Prompt detalhado com CoT extenso

Régua Oficial ENEM:
- Fácil: 200 - 590
- Médio: 590 - 690
- Difícil: 700+

Objetivo: Resolver o paradoxo "fácil vs difícil" onde o modelo erra mais questões fáceis.
"""

# Dados TRI das questões do ENEM 2024
# ⚠️ IMPORTANTE: Este arquivo atualmente só tem dados de Matemática (136-180)
# Os dados TRI de Linguagens (1-45), Humanas (46-90) e Natureza (91-135) precisam ser adicionados
# 
# Estrutura esperada:
# {numero_questao: {"TRI": valor_tri, "H": "HXX", "Nivel": "Fácil/Intermediário/Difícil/Muito Difícil", "Tema": "...", "Gab": "A/B/C/D/E"}}
#
# Régua TRI Oficial ENEM:
# - Fácil: 200 - 590
# - Médio: 590 - 690  
# - Difícil: 700+

TRI_DATA = {
    # MATEMÁTICA (136-180) - DADOS COMPLETOS
    136: {"TRI": 755.3, "H": "H13", "Nivel": "Muito Difícil", "Tema": "Grandezas e medidas", "Gab": "C"},
    137: {"TRI": 662.3, "H": "H28", "Nivel": "Intermediário", "Tema": "Estatística e probabilidade", "Gab": "E"},
    138: {"TRI": 705.0, "H": "H3", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "B"},
    139: {"TRI": 550.2, "H": "H26", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "A"},
    140: {"TRI": 660.6, "H": "H4", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "B"},
    141: {"TRI": 701.9, "H": "H20", "Nivel": "Intermediário", "Tema": "Álgebra e funções", "Gab": "B"},
    142: {"TRI": 661.7, "H": "H2", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "A"},
    143: {"TRI": 792.0, "H": "H18", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "D"},
    144: {"TRI": 636.5, "H": "H7", "Nivel": "Fácil", "Tema": "Geometria", "Gab": "D"},
    145: {"TRI": 613.0, "H": "H8", "Nivel": "Fácil", "Tema": "Geometria", "Gab": "D"},
    146: {"TRI": 809.9, "H": "H22", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "B"},
    147: {"TRI": 601.8, "H": "H1", "Nivel": "Fácil", "Tema": "Números e operações", "Gab": "B"},
    148: {"TRI": 776.1, "H": "H21", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "C"},
    149: {"TRI": 703.3, "H": "H14", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "E"},
    150: {"TRI": 836.2, "H": "H13", "Nivel": "Muito Difícil", "Tema": "Grandezas e medidas", "Gab": "C"},
    151: {"TRI": 750.4, "H": "H11", "Nivel": "Muito Difícil", "Tema": "Geometria", "Gab": "E"},
    152: {"TRI": 604.0, "H": "H25", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "A"},
    153: {"TRI": 622.8, "H": "H1", "Nivel": "Fácil", "Tema": "Números e operações", "Gab": "D"},
    154: {"TRI": 564.5, "H": "H27", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "C"},
    155: {"TRI": 723.7, "H": "H9", "Nivel": "Difícil", "Tema": "Geometria", "Gab": "E"},
    156: {"TRI": 591.2, "H": "H19", "Nivel": "Fácil", "Tema": "Álgebra e funções", "Gab": "B"},
    157: {"TRI": 611.7, "H": "H23", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "C"},
    158: {"TRI": 643.6, "H": "H4", "Nivel": "Fácil", "Tema": "Números e operações", "Gab": "C"},
    159: {"TRI": 678.4, "H": "H10", "Nivel": "Intermediário", "Tema": "Geometria", "Gab": "C"},
    160: {"TRI": 684.5, "H": "H16", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "D"},
    161: {"TRI": 738.7, "H": "H15", "Nivel": "Difícil", "Tema": "Grandezas e medidas", "Gab": "B"},
    162: {"TRI": 760.8, "H": "H5", "Nivel": "Muito Difícil", "Tema": "Números e operações", "Gab": "A"},
    163: {"TRI": 729.8, "H": "H12", "Nivel": "Difícil", "Tema": "Grandezas e medidas", "Gab": "D"},
    164: {"TRI": 712.4, "H": "H8", "Nivel": "Intermediário", "Tema": "Geometria", "Gab": "C"},
    165: {"TRI": 786.9, "H": "H30", "Nivel": "Muito Difícil", "Tema": "Análise combinatória", "Gab": "B"},
    166: {"TRI": 673.6, "H": "H19", "Nivel": "Intermediário", "Tema": "Álgebra e funções", "Gab": "E"},
    167: {"TRI": 701.9, "H": "H3", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "D"},
    168: {"TRI": 625.9, "H": "H15", "Nivel": "Fácil", "Tema": "Grandezas e medidas", "Gab": "A"},
    169: {"TRI": 772.7, "H": "H28", "Nivel": "Muito Difícil", "Tema": "Estatística e probabilidade", "Gab": "E"},
    170: {"TRI": 729.4, "H": "H21", "Nivel": "Difícil", "Tema": "Álgebra e funções", "Gab": "C"},
    171: {"TRI": 787.2, "H": "H22", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "A"},
    172: {"TRI": 673.5, "H": "H17", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "D"},
    173: {"TRI": 647.1, "H": "H29", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "A"},
    174: {"TRI": 663.0, "H": "H6", "Nivel": "Intermediário", "Tema": "Geometria", "Gab": "C"},
    175: {"TRI": 693.9, "H": "H12", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "D"},
    176: {"TRI": 645.1, "H": "H24", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "B"},
    177: {"TRI": 673.9, "H": "H25", "Nivel": "Intermediário", "Tema": "Estatística e probabilidade", "Gab": "C"},
    178: {"TRI": 573.5, "H": "H27", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "E"},
    179: {"TRI": 706.9, "H": "H16", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "C"},
    180: {"TRI": 742.5, "H": "H2", "Nivel": "Difícil", "Tema": "Números e operações", "Gab": "E"},
    
    # LINGUAGENS (1-45) - ADICIONAR DADOS TRI AQUI
    # HUMANAS (46-90) - ADICIONAR DADOS TRI AQUI
    # NATUREZA (91-135) - ADICIONAR DADOS TRI AQUI
}

def classificar_por_tri(tri_value: float) -> str:
    """
    Classifica questão por nível de TRI (RÉGUA OFICIAL DO ENEM)
    
    Args:
        tri_value: Valor TRI da questão
        
    Returns:
        'facil', 'medio' ou 'dificil'
    
    Régua Oficial ENEM:
    - Fácil: 200 - 590
    - Médio: 590 - 690
    - Difícil: 700+
    """
    if tri_value < 200:
        # Valor muito baixo ou inválido - tratar como médio por padrão
        return 'medio'
    elif tri_value < 590:
        return 'facil'
    elif tri_value < 690:
        return 'medio'
    else:  # tri_value >= 690
        return 'dificil'

def obter_tri_questao(numero: int) -> float:
    """Obtém valor TRI de uma questão"""
    tri_info = TRI_DATA.get(numero, {})
    return tri_info.get('TRI', 0)

def criar_prompt_facil() -> str:
    """
    Prompt para questões FÁCEIS (TRI 200-590)
    
    Estratégia: Simplificado, direto, sem overthinking
    """
    return """Você é um especialista em questões do ENEM.

Esta é uma questão FÁCIL (TRI 200-590). Mantenha a simplicidade e seja direto.

⚠️ IMPORTANTE: Questões fáceis são simples. Não complique demais!

📋 METODOLOGIA SIMPLIFICADA:

1. LEIA a questão com atenção
2. IDENTIFIQUE o que está sendo pedido
3. RESOLVA de forma direta
4. VERIFIQUE se a resposta faz sentido
5. ESCOLHA a alternativa correta

🎯 DICAS PARA QUESTÕES FÁCEIS:
- A resposta geralmente é direta
- Não precisa de cálculos complexos
- Se houver figura/tabela, leia diretamente
- Não "overthink" - a solução é simples

Agora, resolva a questão abaixo de forma direta e simples:

"""

def criar_prompt_medio() -> str:
    """
    Prompt para questões MÉDIAS (TRI 590-690)
    
    Estratégia: Prompt padrão com CoT moderado
    """
    return """Você é um especialista em questões do ENEM.

Esta é uma questão de DIFICULDADE MÉDIA (TRI 590-690). Use raciocínio passo-a-passo.

📋 METODOLOGIA:

1. IDENTIFICAÇÃO DO PROBLEMA
   - Leia o contexto e a pergunta
   - Identifique o tipo de problema
   - Anote os dados fornecidos

2. PLANEJAMENTO
   - Determine qual conceito aplicar
   - Planeje os passos de resolução

3. RESOLUÇÃO
   - Resolva passo a passo
   - Mostre cálculos intermediários
   - Verifique cada etapa

4. VALIDAÇÃO
   - Verifique se a resposta faz sentido
   - Confirme unidades e contexto

5. ESCOLHA DA ALTERNATIVA
   - Compare sua resposta com as alternativas
   - Escolha a correta

Agora, resolva a questão abaixo:

"""

def criar_prompt_dificil() -> str:
    """
    Prompt para questões DIFÍCEIS (TRI 700+)
    
    Estratégia: CoT extenso e detalhado, múltiplas validações
    """
    return """Você é um especialista em questões do ENEM.

Esta é uma questão MUITO DIFÍCIL (TRI 700+). Use raciocínio detalhado e múltiplas validações.

⚠️ ATENÇÃO: Questões difíceis exigem cuidado extra e validação rigorosa.

📋 METODOLOGIA DETALHADA:

PASSO 1: ANÁLISE INICIAL PROFUNDA
- Leia o contexto COMPLETO com máxima atenção
- Identifique TODOS os dados fornecidos (explícitos e implícitos)
- Identifique o que está sendo pedido (pode haver múltiplas etapas)
- Identifique o tipo de problema
- Anote unidades de medida e relações entre dados

PASSO 2: PLANEJAMENTO ESTRATÉGICO
- Determine qual(is) conceito(s) aplicar
- Identifique se há múltiplas etapas na resolução
- Planeje TODOS os passos antes de começar
- Identifique fórmulas necessárias
- Verifique se há conversões de unidades necessárias
- Identifique possíveis armadilhas ou pegadinhas

PASSO 3: RESOLUÇÃO PASSO A PASSO DETALHADA
- Resolva o problema passo a passo
- Mostre TODOS os cálculos intermediários
- Verifique cada operação
- Mantenha precisão numérica (cuidado com arredondamentos)
- Se usar aproximações, anote claramente
- Se houver múltiplas etapas, valide cada uma antes de prosseguir

PASSO 4: VALIDAÇÃO MÚLTIPLA
- Valide usando método inverso (substituir na equação original)
- Verifique se a resposta faz sentido no contexto
- Verifique se a resposta está nas unidades corretas
- Verifique se a resposta responde à pergunta feita
- Verifique se não há erros de cálculo ou interpretação

PASSO 5: ANÁLISE DETALHADA DE CADA ALTERNATIVA
Para CADA alternativa (A, B, C, D, E):
- Calcule o valor numérico (se aplicável)
- Compare com sua resposta calculada
- Identifique se há erros comuns que levariam a essa alternativa
- Elimine alternativas claramente incorretas
- Justifique por que cada alternativa está correta ou incorreta

PASSO 6: ELIMINAÇÃO E ESCOLHA FINAL
- Elimine alternativas que você identificou como incorretas
- Entre as alternativas restantes, compare cuidadosamente
- Se houver dúvida entre duas alternativas:
  * Refaça os cálculos críticos
  * Verifique se não houve erro de sinal ou operação
  * Valide com método inverso
  * Foque na diferença entre as alternativas
- Escolha a alternativa que corresponde EXATAMENTE à sua resposta calculada

PASSO 7: VERIFICAÇÃO FINAL RIGOROSA
Antes de responder, confirme:
- ✅ Minha resposta calculada corresponde a qual alternativa?
- ✅ Eliminei as alternativas incorretas?
- ✅ Validei com método inverso?
- ✅ Verifiquei unidades e contexto?
- ✅ Verifiquei se não há erros de cálculo?
- ✅ Verifiquei se não há erros de interpretação?
- ✅ A resposta faz sentido matematicamente e contextualmente?

🎯 INSTRUÇÕES ESPECÍFICAS PARA QUESTÕES DIFÍCEIS:

1. PRECISÃO NUMÉRICA MÁXIMA:
   - Mantenha casas decimais adequadas durante os cálculos
   - Cuidado com arredondamentos prematuros
   - Use frações quando possível para maior precisão
   - Valide resultados aproximados

2. INTERPRETAÇÃO CUIDADOSA:
   - Leia cuidadosamente eixos e legendas (se houver gráfico)
   - Identifique escalas e unidades
   - Extraia dados corretamente
   - Cuidado com interpretações literais vs. matemáticas

3. PROBLEMAS CONTEXTUALIZADOS:
   - Relacione o problema com o contexto real
   - Verifique se sua resposta faz sentido prático
   - Cuidado com interpretações literais vs. matemáticas

4. MÚLTIPLAS ETAPAS:
   - Resolva cada etapa separadamente
   - Valide cada etapa antes de prosseguir
   - Verifique se todas as etapas foram completadas

5. ELIMINAÇÃO DE ALTERNATIVAS:
   - Use estimativas para eliminar alternativas absurdas
   - Compare ordens de grandeza
   - Verifique se alternativas estão em unidades corretas

⚠️ LEMBRE-SE:
- Questões difíceis exigem cuidado extra
- SEMPRE valide antes de escolher
- NÃO escolha por "intuição" - use cálculo e validação
- Se estiver em dúvida, refaça os cálculos focando na diferença entre alternativas

Agora, resolva a questão abaixo seguindo TODOS os passos acima com MÁXIMO CUIDADO:

"""

def selecionar_prompt_por_tri(tri_value: float) -> str:
    """
    Seleciona o prompt apropriado baseado no TRI
    
    Args:
        tri_value: Valor TRI da questão
        
    Returns:
        String com o prompt apropriado
    """
    nivel = classificar_por_tri(tri_value)
    
    if nivel == 'facil':
        return criar_prompt_facil()
    elif nivel == 'medio':
        return criar_prompt_medio()
    else:  # dificil
        return criar_prompt_dificil()

def obter_info_tri(numero: int) -> dict:
    """Obtém informações TRI completas de uma questão"""
    return TRI_DATA.get(numero, {
        'TRI': 0,
        'H': 'N/A',
        'Nivel': 'N/A',
        'Tema': 'N/A',
        'Gab': 'N/A'
    })

if __name__ == "__main__":
    # Teste das funções
    print("=" * 70)
    print("🎯 TESTE DO SISTEMA DE PROMPTS ADAPTATIVOS POR TRI")
    print("=" * 70)
    print()
    
    # Testar com questões de diferentes níveis
    questoes_teste = [
        (139, "Fácil"),
        (137, "Médio"),
        (143, "Difícil")
    ]
    
    for num, desc in questoes_teste:
        tri_info = obter_info_tri(num)
        tri_value = tri_info.get('TRI', 0)
        nivel = classificar_por_tri(tri_value)
        prompt = selecionar_prompt_por_tri(tri_value)
        
        print(f"Questão {num} (TRI: {tri_value:.1f}, {desc})")
        print(f"  Classificação: {nivel.upper()}")
        print(f"  Tamanho do prompt: {len(prompt)} caracteres")
        print(f"  Primeiras 100 caracteres: {prompt[:100]}...")
        print()
