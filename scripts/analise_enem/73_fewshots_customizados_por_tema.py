#!/usr/bin/env python3
"""
📚 Sistema de Few-Shots Customizados por Tema

Cria bancos de few-shots específicos para cada tema de matemática:
- Álgebra e funções
- Estatística e probabilidade
- Geometria
- Grandezas e medidas
- Números e operações

Objetivo: Melhorar acurácia em temas problemáticos (Álgebra: 62.5%, Estatística: 70%)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar dados TRI e funções auxiliares
import importlib.util
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_module)

TRI_DATA = prompts_module.TRI_DATA
obter_info_tri = prompts_module.obter_info_tri

def carregar_questoes_por_tema():
    """Carrega questões organizadas por tema usando dados TRI"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "processed" / "enem_2024_completo.jsonl"
    
    questoes_por_tema = {
        'Álgebra e funções': [],
        'Estatística e probabilidade': [],
        'Geometria': [],
        'Grandezas e medidas': [],
        'Números e operações': [],
        'Análise combinatória': []
    }
    
    if not arquivo.exists():
        return questoes_por_tema
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questao = json.loads(line)
                num_str = questao.get('id', '').replace('questao_', '') or questao.get('number', '')
                try:
                    num = int(num_str)
                    if 136 <= num <= 180:  # Matemática
                        tri_info = obter_info_tri(num)
                        tema = tri_info.get('Tema', 'N/A')
                        if tema in questoes_por_tema:
                            questao['number'] = num
                            questao['tema'] = tema
                            questao['tri'] = tri_info.get('TRI', 0)
                            questoes_por_tema[tema].append(questao)
                except (ValueError, TypeError):
                    continue
    
    return questoes_por_tema

def criar_fewshot_algebra():
    """Cria few-shots para Álgebra e Funções"""
    return [
        {
            'question': 'Uma função f é definida por f(x) = 2x + 3. Qual é o valor de f(5)?',
            'alternatives': ['A) 10', 'B) 11', 'C) 13', 'D) 15', 'E) 17'],
            'response': 'Para encontrar f(5), substituo x por 5 na função: f(5) = 2(5) + 3 = 10 + 3 = 13. Resposta: C'
        },
        {
            'question': 'Se uma função quadrática tem raízes em x = 2 e x = -3, qual é a forma fatorada?',
            'alternatives': ['A) (x-2)(x+3)', 'B) (x+2)(x-3)', 'C) (x-2)(x-3)', 'D) (x+2)(x+3)', 'E) x(x-2)(x+3)'],
            'response': 'Se as raízes são x = 2 e x = -3, a forma fatorada é (x-2)(x-(-3)) = (x-2)(x+3). Resposta: A'
        },
        {
            'question': 'Em um sistema de equações, se x + y = 10 e x - y = 4, qual é o valor de x?',
            'alternatives': ['A) 3', 'B) 5', 'C) 7', 'D) 9', 'E) 11'],
            'response': 'Somando as equações: (x+y) + (x-y) = 10 + 4 → 2x = 14 → x = 7. Resposta: C'
        }
    ]

def criar_fewshot_estatistica():
    """Cria few-shots para Estatística e Probabilidade"""
    return [
        {
            'question': 'Em uma pesquisa com 200 pessoas, 120 preferem A e 80 preferem B. Qual a probabilidade de escolher alguém que prefere A?',
            'alternatives': ['A) 0.4', 'B) 0.5', 'C) 0.6', 'D) 0.7', 'E) 0.8'],
            'response': 'Probabilidade = casos favoráveis / total = 120/200 = 0.6. Resposta: C'
        },
        {
            'question': 'Em um conjunto de dados {2, 4, 6, 8, 10}, qual é a média?',
            'alternatives': ['A) 4', 'B) 5', 'C) 6', 'D) 7', 'E) 8'],
            'response': 'Média = (2+4+6+8+10)/5 = 30/5 = 6. Resposta: C'
        },
        {
            'question': 'Uma urna tem 5 bolas brancas e 3 pretas. Qual a probabilidade de tirar uma bola branca?',
            'alternatives': ['A) 3/8', 'B) 5/8', 'C) 1/2', 'D) 3/5', 'E) 5/3'],
            'response': 'Total: 8 bolas. Brancas: 5. Probabilidade = 5/8. Resposta: B'
        }
    ]

def criar_fewshot_geometria():
    """Cria few-shots para Geometria"""
    return [
        {
            'question': 'Em um triângulo retângulo, os catetos medem 3 cm e 4 cm. Qual é a medida da hipotenusa?',
            'alternatives': ['A) 5 cm', 'B) 6 cm', 'C) 7 cm', 'D) 8 cm', 'E) 9 cm'],
            'response': 'Teorema de Pitágoras: h² = 3² + 4² = 9 + 16 = 25 → h = 5 cm. Resposta: A'
        },
        {
            'question': 'Um retângulo tem comprimento 8 m e largura 5 m. Qual é sua área?',
            'alternatives': ['A) 13 m²', 'B) 26 m²', 'C) 40 m²', 'D) 45 m²', 'E) 50 m²'],
            'response': 'Área do retângulo = comprimento × largura = 8 × 5 = 40 m². Resposta: C'
        },
        {
            'question': 'Um círculo tem raio de 6 cm. Qual é sua área? (use π = 3.14)',
            'alternatives': ['A) 18.84 cm²', 'B) 37.68 cm²', 'C) 113.04 cm²', 'D) 226.08 cm²', 'E) 452.16 cm²'],
            'response': 'Área do círculo = π × r² = 3.14 × 6² = 3.14 × 36 = 113.04 cm². Resposta: C'
        }
    ]

def criar_fewshot_grandezas():
    """Cria few-shots para Grandezas e Medidas"""
    return [
        {
            'question': 'Quantos metros há em 2,5 quilômetros?',
            'alternatives': ['A) 25 m', 'B) 250 m', 'C) 2500 m', 'D) 25000 m', 'E) 250000 m'],
            'response': '1 km = 1000 m. Então 2,5 km = 2,5 × 1000 = 2500 m. Resposta: C'
        },
        {
            'question': 'Um tanque tem capacidade de 500 litros. Quantos mililitros são?',
            'alternatives': ['A) 50 ml', 'B) 500 ml', 'C) 5000 ml', 'D) 50000 ml', 'E) 500000 ml'],
            'response': '1 litro = 1000 ml. Então 500 litros = 500 × 1000 = 500000 ml. Resposta: E'
        },
        {
            'question': 'Uma escala de 1:1000 significa que 1 cm no mapa representa quantos metros na realidade?',
            'alternatives': ['A) 1 m', 'B) 10 m', 'C) 100 m', 'D) 1000 m', 'E) 10000 m'],
            'response': 'Escala 1:1000 significa 1 cm = 1000 cm = 10 m na realidade. Resposta: B'
        }
    ]

def criar_fewshot_numeros():
    """Cria few-shots para Números e Operações"""
    return [
        {
            'question': 'Qual é o resultado de 15% de 200?',
            'alternatives': ['A) 15', 'B) 20', 'C) 30', 'D) 35', 'E) 40'],
            'response': '15% de 200 = (15/100) × 200 = 0.15 × 200 = 30. Resposta: C'
        },
        {
            'question': 'Se 3/4 de um número é 24, qual é esse número?',
            'alternatives': ['A) 18', 'B) 28', 'C) 32', 'D) 36', 'E) 48'],
            'response': 'Se 3/4 × x = 24, então x = 24 ÷ (3/4) = 24 × (4/3) = 96/3 = 32. Resposta: C'
        },
        {
            'question': 'Uma razão entre dois números é 2:3. Se o menor é 8, qual é o maior?',
            'alternatives': ['A) 10', 'B) 12', 'C) 14', 'D) 16', 'E) 18'],
            'response': 'Razão 2:3 significa que se o menor é 8, então 2 partes = 8, logo 1 parte = 4. O maior = 3 partes = 3 × 4 = 12. Resposta: B'
        }
    ]

def criar_fewshot_combinatoria():
    """Cria few-shots para Análise Combinatória"""
    return [
        {
            'question': 'De quantas formas diferentes podemos organizar 3 livros em uma prateleira?',
            'alternatives': ['A) 3', 'B) 6', 'C) 9', 'D) 12', 'E) 15'],
            'response': 'Permutação de 3 elementos: 3! = 3 × 2 × 1 = 6 formas. Resposta: B'
        },
        {
            'question': 'Quantos números de 3 algarismos distintos podemos formar com os dígitos 1, 2, 3, 4?',
            'alternatives': ['A) 12', 'B) 24', 'C) 36', 'D) 48', 'E) 64'],
            'response': 'Arranjo de 4 elementos tomados 3 a 3: A(4,3) = 4 × 3 × 2 = 24. Resposta: B'
        }
    ]

def obter_fewshots_por_tema(tema: str, num_exemplos: int = 3) -> List[Dict]:
    """
    Retorna few-shots específicos para um tema
    
    Args:
        tema: Tema da questão
        num_exemplos: Número de exemplos a retornar
        
    Returns:
        Lista de exemplos few-shot
    """
    tema_lower = tema.lower()
    
    # Mapear temas
    if 'álgebra' in tema_lower or 'função' in tema_lower or 'funções' in tema_lower:
        fewshots = criar_fewshot_algebra()
    elif 'estatística' in tema_lower or 'probabilidade' in tema_lower:
        fewshots = criar_fewshot_estatistica()
    elif 'geometria' in tema_lower:
        fewshots = criar_fewshot_geometria()
    elif 'grandezas' in tema_lower or 'medidas' in tema_lower:
        fewshots = criar_fewshot_grandezas()
    elif 'números' in tema_lower or 'operações' in tema_lower or 'números e operações' in tema_lower:
        fewshots = criar_fewshot_numeros()
    elif 'combinatória' in tema_lower or 'análise combinatória' in tema_lower:
        fewshots = criar_fewshot_combinatoria()
    else:
        # Few-shots genéricos (mistura de temas)
        fewshots = criar_fewshot_numeros()[:2] + criar_fewshot_geometria()[:1]
    
    return fewshots[:num_exemplos]

def formatar_fewshot_para_prompt(exemplo: Dict) -> str:
    """Formata um exemplo few-shot para incluir no prompt"""
    texto = f"Exemplo:\n"
    texto += f"Questão: {exemplo['question']}\n\n"
    texto += "Alternativas:\n"
    for alt in exemplo['alternatives']:
        texto += f"{alt}\n"
    texto += f"\nResolução: {exemplo['response']}\n\n"
    return texto

def criar_prompt_com_fewshots(prompt_base: str, tema: str, num_fewshots: int = 3) -> str:
    """
    Adiciona few-shots customizados ao prompt base
    
    Args:
        prompt_base: Prompt base (do sistema adaptativo)
        tema: Tema da questão
        num_fewshots: Número de exemplos few-shot
        
    Returns:
        Prompt completo com few-shots
    """
    fewshots = obter_fewshots_por_tema(tema, num_fewshots)
    
    if not fewshots:
        return prompt_base
    
    # Adicionar seção de exemplos ao prompt
    exemplos_texto = "\n\n📚 EXEMPLOS DE QUESTÕES SIMILARES (Use como referência):\n\n"
    for i, exemplo in enumerate(fewshots, 1):
        exemplos_texto += f"--- Exemplo {i} ---\n"
        exemplos_texto += formatar_fewshot_para_prompt(exemplo)
    
    exemplos_texto += "\n" + "="*50 + "\n"
    exemplos_texto += "Agora, resolva a questão abaixo usando os exemplos acima como referência:\n\n"
    
    # Inserir exemplos antes da questão (no final do prompt base)
    # O prompt base já termina com "Agora, resolva a questão abaixo:"
    # Vamos substituir isso para incluir os exemplos
    if "Agora, resolva a questão abaixo" in prompt_base:
        # Encontrar onde termina o prompt base
        prompt_completo = prompt_base.replace(
            "Agora, resolva a questão abaixo:",
            exemplos_texto
        )
    elif "Agora, resolva a questão abaixo" in prompt_base:
        prompt_completo = prompt_base.replace(
            "Agora, resolva a questão abaixo",
            exemplos_texto
        )
    else:
        # Se não encontrar, adicionar no final
        prompt_completo = prompt_base + exemplos_texto
    
    return prompt_completo

if __name__ == "__main__":
    # Teste das funções
    print("=" * 70)
    print("📚 TESTE DO SISTEMA DE FEW-SHOTS CUSTOMIZADOS")
    print("=" * 70)
    print()
    
    temas_teste = [
        "Álgebra e funções",
        "Estatística e probabilidade",
        "Geometria",
        "Grandezas e medidas",
        "Números e operações",
        "Análise combinatória"
    ]
    
    for tema in temas_teste:
        print(f"📖 Tema: {tema}")
        fewshots = obter_fewshots_por_tema(tema, num_exemplos=2)
        print(f"   ✅ {len(fewshots)} exemplos disponíveis")
        if fewshots:
            print(f"   Primeiro exemplo: {fewshots[0]['question'][:60]}...")
        print()
    
    # Testar integração com prompt adaptativo
    print("=" * 70)
    print("🔗 TESTE DE INTEGRAÇÃO COM PROMPTS ADAPTATIVOS")
    print("=" * 70)
    print()
    
    # Importar função de prompt adaptativo
    selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
    
    # Testar com questão de álgebra (TRI médio)
    tri_value = 701.9  # Questão 141 - Álgebra, Intermediário
    prompt_base = selecionar_prompt_por_tri(tri_value)
    prompt_completo = criar_prompt_com_fewshots(prompt_base, "Álgebra e funções", num_fewshots=3)
    
    print(f"Prompt base (TRI {tri_value:.1f}): {len(prompt_base)} caracteres")
    print(f"Prompt com few-shots: {len(prompt_completo)} caracteres")
    print(f"Few-shots adicionaram: {len(prompt_completo) - len(prompt_base)} caracteres")
    print()
    print("Primeiras 200 caracteres do prompt completo:")
    print(prompt_completo[:200] + "...")
    print()
    
    print("=" * 70)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 70)

