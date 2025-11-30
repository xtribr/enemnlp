#!/usr/bin/env python3
"""
🔬 Prompt Especializado para Ciências da Natureza

Cria prompt específico para melhorar desempenho em Natureza.
Gap atual: -9.09% vs GPT-4o (84.09% vs 93.18%)

Objetivo: Aumentar para 93%+
"""

PROMPT_ESPECIALIZADO_NATUREZA = """
🔬 INSTRUÇÕES ESPECÍFICAS PARA CIÊNCIAS DA NATUREZA

Esta é uma questão de Ciências da Natureza (Física, Química ou Biologia).

🎯 METODOLOGIA ESPECÍFICA:

1. IDENTIFICAR O TIPO DE QUESTÃO
   - Física: Mecânica, Termodinâmica, Eletromagnetismo, etc.
   - Química: Estequiometria, Soluções, Equilíbrio, etc.
   - Biologia: Genética, Ecologia, Fisiologia, etc.

2. VERIFICAR UNIDADES
   - Sempre verificar unidades nas alternativas
   - Converter unidades se necessário (km → m, g → kg, etc.)
   - Verificar se a resposta tem unidade correta

3. APLICAR CONCEITOS CIENTÍFICOS
   - Usar fórmulas corretas (F=ma, PV=nRT, etc.)
   - Verificar relações causa-efeito
   - Aplicar leis científicas (Lei de Boyle, Mendel, etc.)

4. ANALISAR GRÁFICOS E TABELAS
   - Ler valores diretamente do gráfico
   - Identificar tendências (crescente, decrescente)
   - Verificar escalas e unidades nos eixos

5. VALIDAR RESPOSTA
   - Verificar se a resposta faz sentido fisicamente/quimicamente
   - Verificar se unidades estão corretas
   - Verificar se valores são razoáveis (ex: temperatura não pode ser negativa em Kelvin)

⚠️ ATENÇÃO ESPECIAL:
- Gráficos científicos: Ler valores diretamente, verificar escalas
- Cálculos: Sempre verificar unidades e conversões
- Relações: Verificar se causa-efeito está correta
- Valores: Verificar se são fisicamente possíveis

"""

def criar_prompt_natureza(prompt_base: str) -> str:
    """
    Adiciona instruções específicas de Natureza ao prompt base
    
    Args:
        prompt_base: Prompt base (adaptativo)
        
    Returns:
        Prompt com instruções de Natureza
    """
    if "Agora, resolva a questão abaixo" in prompt_base:
        prompt_final = prompt_base.replace(
            "Agora, resolva a questão abaixo:",
            PROMPT_ESPECIALIZADO_NATUREZA + "\nAgora, resolva a questão abaixo:"
        )
    else:
        prompt_final = prompt_base + "\n\n" + PROMPT_ESPECIALIZADO_NATUREZA
    
    return prompt_final

if __name__ == "__main__":
    print("=" * 70)
    print("🔬 Prompt Especializado para Natureza")
    print("=" * 70)
    print()
    print(PROMPT_ESPECIALIZADO_NATUREZA)
    print()
    print("✅ Prompt criado com sucesso!")
    print("🎯 Objetivo: Reduzir gap de -9.09% para 0% (superar GPT-4o)")

