#!/usr/bin/env python3
"""
⚡ Prompt Ultra-Simples para Questões Fáceis

Resolve o problema de overthinking em questões fáceis (TRI < 650).
Acurácia atual: 71.4% → Meta: 85%+

Impacto esperado: +8-12% em questões fáceis
"""

PROMPT_ULTRA_SIMPLES_FACIL = """
⚠️ ATENÇÃO: Esta é uma questão FÁCIL (TRI < 650).

🎯 REGRAS OBRIGATÓRIAS PARA QUESTÕES FÁCEIS:

1. NÃO COMPLIQUE
   - A resposta está DIRETA no enunciado
   - Não tente encontrar "pegadinhas" - não há
   - Não faça cálculos complexos se não for necessário

2. LEIA UMA VEZ
   - Leia o enunciado UMA vez apenas
   - Identifique o que está sendo pedido
   - A resposta geralmente está explícita

3. RESPONDA IMEDIATAMENTE
   - Não pense demais
   - Não tente várias abordagens
   - Escolha a resposta mais óbvia

4. SE HOUVER FIGURA
   - Leia os valores DIRETAMENTE da figura
   - Não interprete além do que está mostrado
   - A resposta está na figura, não precisa calcular

5. VERIFIQUE RAPIDAMENTE
   - Confira se a resposta faz sentido básico
   - Verifique se está nas alternativas
   - Se sim, responda e pare

⚠️ LEMBRE-SE:
- Questões fáceis = Respostas diretas
- Não "overthink" - leia e responda
- A resposta geralmente está explícita no texto/figura

"""

PROMPT_FACIL_COM_FIGURA = """
⚠️ ATENÇÃO: Questão FÁCIL com FIGURA SIMPLES (TRI < 650).

🎯 INSTRUÇÕES ESPECÍFICAS:

1. A FIGURA É SIMPLES
   - Tabela ou gráfico básico
   - Leia os valores DIRETAMENTE
   - Não complique a interpretação

2. O QUE ESTÁ SENDO PEDIDO?
   - Leia a pergunta
   - Identifique qual dado você precisa
   - Onde esse dado está na figura?

3. LEIA DIRETAMENTE DA FIGURA
   - Encontre o valor na figura
   - Leia exatamente o que está pedido
   - Não faça cálculos se não for necessário

4. RESPONDA
   - O valor está na figura
   - Escolha a alternativa correspondente
   - Pare aqui - não pense mais

⚠️ REGRA DE OURO:
- Figura simples = Leitura direta
- Não calcule se não precisar
- Não interprete além do óbvio
- A resposta está explícita na figura

"""

def criar_prompt_ultra_simples(questao: dict, tem_figura: bool = False) -> str:
    """
    Cria prompt ultra-simples para questões fáceis
    
    Args:
        questao: Dados da questão
        tem_figura: Se a questão tem figura
        
    Returns:
        Prompt ultra-simples
    """
    if tem_figura:
        return PROMPT_FACIL_COM_FIGURA
    else:
        return PROMPT_ULTRA_SIMPLES_FACIL

def aplicar_prompt_ultra_simples(prompt_base: str, questao: dict, tri_value: float, obter_info_figura_func=None) -> str:
    """
    Aplica prompt ultra-simples se a questão for fácil
    
    Args:
        prompt_base: Prompt base (adaptativo)
        questao: Dados da questão
        tri_value: Valor TRI da questão
        obter_info_figura_func: Função para obter info de figura (opcional)
        
    Returns:
        Prompt final (ultra-simples se fácil, normal caso contrário)
    """
    # Apenas para questões fáceis (TRI < 650)
    if tri_value < 650:
        # Verificar se tem figura
        if obter_info_figura_func:
            info_figura = obter_info_figura_func(questao)
            tem_figura = info_figura.get('tem_figura', False)
        else:
            tem_figura = bool(questao.get('description') or questao.get('figures') or questao.get('has_images'))
        
        # Criar prompt ultra-simples
        prompt_ultra_simples = criar_prompt_ultra_simples(questao, tem_figura)
        
        # Substituir ou adicionar ao prompt base
        if "Agora, resolva a questão abaixo" in prompt_base:
            prompt_final = prompt_base.replace(
                "Agora, resolva a questão abaixo:",
                prompt_ultra_simples + "\nAgora, resolva a questão abaixo:"
            )
        else:
            prompt_final = prompt_base + "\n\n" + prompt_ultra_simples
        
        return prompt_final
    
    # Para questões médias/difíceis, usar prompt normal
    return prompt_base

if __name__ == "__main__":
    # Teste do prompt
    print("=" * 70)
    print("⚡ TESTE: Prompt Ultra-Simples para Questões Fáceis")
    print("=" * 70)
    print()
    
    print("📝 Prompt para Questão Fácil (sem figura):")
    print("-" * 70)
    print(PROMPT_ULTRA_SIMPLES_FACIL)
    print()
    
    print("📝 Prompt para Questão Fácil (com figura):")
    print("-" * 70)
    print(PROMPT_FACIL_COM_FIGURA)
    print()
    
    print("✅ Prompts criados com sucesso!")
    print()
    print("🎯 Uso:")
    print("   - Aplicar automaticamente para TRI < 650")
    print("   - Meta: Aumentar acurácia de 71.4% para 85%+")
    print("   - Impacto esperado: +8-12% em questões fáceis")

