#!/usr/bin/env python3
"""
🖼️ Sistema de Detecção de Figuras Simples

Detecta quando uma figura é simples (tabela, gráfico básico) e aplica
prompt específico para evitar overthinking em questões fáceis com figuras.

Objetivo: Resolver problema onde modelo erra questões fáceis com figuras (71.4% acerto).
"""

import re
from typing import Dict, Optional

def detectar_tipo_figura(description: str) -> Optional[str]:
    """
    Detecta o tipo de figura baseado na descrição
    
    Args:
        description: Descrição textual da figura
        
    Returns:
        'tabela', 'grafico_basico', 'grafico_complexo', 'diagrama', 'imagem', ou None
    """
    if not description or len(description) < 10:
        return None
    
    desc_lower = description.lower()
    
    # Gráfico básico (barra, linha simples, pizza) - VERIFICAR PRIMEIRO
    # (antes de tabela, pois "linha" pode aparecer em ambos)
    if any(palavra in desc_lower for palavra in [
        'gráfico de barras', 'bar chart', 'gráfico de linha', 'line chart',
        'gráfico de pizza', 'pie chart', 'gráfico simples', 'gráfico básico',
        'barras verticais', 'barras horizontais', 'gráfico de colunas'
    ]):
        return 'grafico_basico'
    
    # Tabela (verificar depois de gráficos)
    if any(palavra in desc_lower for palavra in [
        'tabela', 'table', 'colunas e linhas', 'dados tabulares', 
        'valores em tabela', 'organizado em tabela', 'tabela com'
    ]):
        return 'tabela'
    
    # Gráfico complexo
    if any(palavra in desc_lower for palavra in [
        'gráfico complexo', 'múltiplos gráficos', 'gráfico composto',
        'gráfico de dispersão', 'scatter plot', 'gráfico de área'
    ]):
        return 'grafico_complexo'
    
    # Diagrama
    if any(palavra in desc_lower for palavra in [
        'diagrama', 'esquema', 'fluxograma', 'organograma', 'diagrama de venn'
    ]):
        return 'diagrama'
    
    # Imagem/foto
    if any(palavra in desc_lower for palavra in [
        'fotografia', 'imagem', 'foto', 'ilustração', 'desenho'
    ]):
        return 'imagem'
    
    return None

def eh_figura_simples(description: str) -> bool:
    """
    Determina se uma figura é simples (tabela ou gráfico básico)
    
    Args:
        description: Descrição textual da figura
        
    Returns:
        True se for figura simples, False caso contrário
    """
    tipo = detectar_tipo_figura(description)
    
    # Figuras simples: tabelas e gráficos básicos
    figuras_simples = ['tabela', 'grafico_basico']
    
    return tipo in figuras_simples

def analisar_complexidade_descricao(description) -> Dict:
    """
    Analisa a complexidade de uma descrição de figura
    
    Args:
        description: Descrição textual da figura (string ou list)
        
    Returns:
        Dicionário com análise de complexidade
    """
    # Converter lista para string se necessário
    if isinstance(description, list):
        description = ' '.join(str(d) for d in description if d)
    
    if not description or len(str(description)) < 10:
        return {
            'tem_figura': False,
            'tipo': None,
            'eh_simples': False,
            'comprimento': 0,
            'palavras_chave_simples': 0
        }
    
    description_str = str(description)
    tipo = detectar_tipo_figura(description_str)
    eh_simples = eh_figura_simples(description_str)
    
    # Contar palavras-chave de simplicidade
    palavras_simples = ['tabela', 'gráfico de barras', 'gráfico de linha', 
                       'gráfico de pizza', 'dados', 'valores', 'números']
    palavras_chave_simples = sum(1 for palavra in palavras_simples 
                                 if palavra in description_str.lower())
    
    return {
        'tem_figura': True,
        'tipo': tipo,
        'eh_simples': eh_simples,
        'comprimento': len(description_str),
        'palavras_chave_simples': palavras_chave_simples
    }

def criar_prompt_figura_simples() -> str:
    """
    Cria prompt específico para questões com figuras simples
    
    Estratégia: Instruções diretas para ler tabela/gráfico sem complicar
    """
    return """
⚠️ ATENÇÃO: Esta questão tem uma FIGURA SIMPLES (tabela ou gráfico básico).

🎯 INSTRUÇÕES ESPECÍFICAS PARA FIGURAS SIMPLES:

1. LEIA DIRETAMENTE
   - Não complique! A figura é simples
   - Leia os valores diretamente da tabela/gráfico
   - Não tente interpretar além do que está mostrado

2. IDENTIFIQUE O QUE ESTÁ SENDO PEDIDO
   - O que a pergunta quer saber?
   - Qual dado específico você precisa encontrar?
   - Onde esse dado está na figura?

3. LOCALIZE O DADO NA FIGURA
   - Encontre exatamente o que está sendo pedido
   - Leia o valor diretamente
   - Não faça cálculos complexos se não for necessário

4. VERIFIQUE A RESPOSTA
   - Confira se você leu o valor correto
   - Verifique se respondeu o que foi perguntado
   - A resposta geralmente está diretamente na figura

⚠️ LEMBRE-SE:
- Figuras simples = Respostas simples
- Não "overthink" - leia diretamente
- A resposta geralmente está explícita na figura

"""

def criar_prompt_com_deteccao_figura(prompt_base: str, questao: Dict) -> str:
    """
    Adiciona instruções de figura simples ao prompt base se necessário
    
    Args:
        prompt_base: Prompt base (adaptativo)
        questao: Dados da questão
        
    Returns:
        Prompt completo com detecção de figura
    """
    # Verificar se há descrição de figura
    description = questao.get('description', '')
    
    # Normalizar description
    if isinstance(description, list):
        description = description[0] if description else ''
    
    if not description or len(str(description)) < 10:
        # Se não tem descrição, pode ter figura mas sem descrição
        # Verificar campo has_images ou figures
        has_images = questao.get('has_images', False) or bool(questao.get('figures', []))
        if not has_images:
            return prompt_base
        # Se tem imagem mas sem descrição, não podemos detectar se é simples
        return prompt_base
    
    # Analisar descrição
    analise = analisar_complexidade_descricao(description)
    
    if analise['eh_simples']:
        # Adicionar instruções para figura simples
        prompt_figura = criar_prompt_figura_simples()
        
        # Inserir antes da questão (no final do prompt base)
        if "Agora, resolva a questão abaixo" in prompt_base:
            prompt_completo = prompt_base.replace(
                "Agora, resolva a questão abaixo:",
                prompt_figura + "\nAgora, resolva a questão abaixo:"
            )
        else:
            prompt_completo = prompt_base + "\n\n" + prompt_figura
    
    else:
        # Figura complexa - usar prompt normal
        prompt_completo = prompt_base
    
    return prompt_completo

def obter_info_figura(questao: Dict) -> Dict:
    """
    Obtém informações sobre a figura de uma questão
    
    Args:
        questao: Dados da questão
        
    Returns:
        Dicionário com informações da figura
    """
    description = questao.get('description', '')
    
    # Normalizar description (pode ser string, list ou None)
    if isinstance(description, list):
        description = description[0] if description else ''
    elif not description:
        description = ''
    
    if not description or len(str(description)) < 10:
        has_images = questao.get('has_images', False) or bool(questao.get('figures', []))
        return {
            'tem_figura': has_images,
            'tem_descricao': False,
            'tipo': None,
            'eh_simples': False
        }
    
    analise = analisar_complexidade_descricao(description)
    
    return {
        'tem_figura': True,
        'tem_descricao': True,
        'tipo': analise['tipo'],
        'eh_simples': analise['eh_simples'],
        'comprimento_descricao': analise['comprimento']
    }

if __name__ == "__main__":
    # Teste das funções
    print("=" * 70)
    print("🖼️ TESTE DO SISTEMA DE DETECÇÃO DE FIGURAS SIMPLES")
    print("=" * 70)
    print()
    
    # Casos de teste
    casos_teste = [
        ("Uma tabela com 3 colunas e 5 linhas mostrando valores numéricos", "tabela", True),
        ("Gráfico de barras mostrando vendas por mês", "grafico_basico", True),
        ("Gráfico de linha com tendência temporal", "grafico_basico", True),
        ("Gráfico de pizza com distribuição percentual", "grafico_basico", True),
        ("Diagrama complexo com múltiplas conexões", "diagrama", False),
        ("Gráfico de dispersão com correlação", "grafico_complexo", False),
        ("Fotografia de um objeto", "imagem", False),
        ("", None, False),
    ]
    
    print("📊 TESTE 1: Detecção de Tipo de Figura")
    print("-" * 70)
    todos_ok = True
    for desc, tipo_esperado, simples_esperado in casos_teste:
        tipo_detectado = detectar_tipo_figura(desc)
        simples_detectado = eh_figura_simples(desc)
        
        ok_tipo = tipo_detectado == tipo_esperado
        ok_simples = simples_detectado == simples_esperado
        
        if not ok_tipo or not ok_simples:
            todos_ok = False
        
        status = "✅" if (ok_tipo and ok_simples) else "❌"
        print(f"{status} '{desc[:50]}...'")
        print(f"   Tipo: {tipo_detectado} (esperado: {tipo_esperado})")
        print(f"   Simples: {simples_detectado} (esperado: {simples_esperado})")
        print()
    
    print("=" * 70)
    if todos_ok:
        print("✅ TODOS OS TESTES DE DETECÇÃO PASSARAM")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
    print("=" * 70)
    print()
    
    # Teste de prompt
    print("📝 TESTE 2: Prompt para Figuras Simples")
    print("-" * 70)
    prompt_figura = criar_prompt_figura_simples()
    print(f"Tamanho do prompt: {len(prompt_figura)} caracteres")
    print(f"Primeiras 200 caracteres:")
    print(prompt_figura[:200] + "...")
    print()

