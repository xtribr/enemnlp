#!/usr/bin/env python3
"""
🧪 Teste do Sistema de Prompts Adaptativos

Testa o sistema sem fazer chamadas à API (validação de estrutura).
Para teste completo com API, use: 71_avaliar_com_prompts_adaptativos.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar funções do módulo de prompts adaptativos
import importlib.util
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_module)

selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri
classificar_por_tri = prompts_module.classificar_por_tri

def carregar_questoes_2024_matematica():
    """Carrega questões de matemática do ENEM 2024"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "processed" / "enem_2024_completo.jsonl"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return []
    
    questoes = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questao = json.loads(line)
                # Detectar área pelo número da questão
                # Extrair número do ID ou number
                num_str = questao.get('id', '').replace('questao_', '') or questao.get('number', '')
                try:
                    num = int(num_str)
                    # Matemática: questões 136-180
                    if 136 <= num <= 180:
                        questao['number'] = num
                        questoes.append(questao)
                except (ValueError, TypeError):
                    continue
    
    return questoes

def testar_classificacao_tri():
    """Testa a classificação por TRI"""
    print("=" * 70)
    print("🧪 TESTE 1: Classificação por TRI")
    print("=" * 70)
    print()
    
    casos_teste = [
        (550.2, "Fácil"),
        (650.0, "Médio"),
        (700.0, "Médio"),
        (750.0, "Médio"),
        (755.0, "Difícil"),
        (800.0, "Difícil")
    ]
    
    todos_ok = True
    for tri, esperado in casos_teste:
        nivel = classificar_por_tri(tri)
        # Normalizar para comparação (remover acentos e converter para minúsculas)
        esperado_normalizado = esperado.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i')
        nivel_normalizado = nivel.lower()
        ok = nivel_normalizado == esperado_normalizado
        status = "✅" if ok else "❌"
        
        if not ok:
            todos_ok = False
        
        print(f"{status} TRI {tri:.1f} → {nivel.upper()} (esperado: {esperado.upper()})")
    
    print()
    return todos_ok

def testar_prompts_por_tri():
    """Testa a seleção de prompts por TRI"""
    print("=" * 70)
    print("🧪 TESTE 2: Seleção de Prompts por TRI")
    print("=" * 70)
    print()
    
    casos_teste = [
        (139, 550.2, "Fácil"),
        (137, 662.3, "Médio"),
        (143, 792.0, "Difícil")
    ]
    
    todos_ok = True
    for num, tri, desc in casos_teste:
        prompt = selecionar_prompt_por_tri(tri)
        nivel = classificar_por_tri(tri)
        
        # Verificar características do prompt
        if nivel == 'facil':
            ok = len(prompt) < 1000 and "FÁCIL" in prompt
        elif nivel == 'medio':
            ok = 500 < len(prompt) < 1500 and "MÉDIA" in prompt
        else:  # dificil
            ok = len(prompt) > 3000 and "DIFÍCIL" in prompt
        
        status = "✅" if ok else "❌"
        if not ok:
            todos_ok = False
        
        print(f"{status} Questão {num} (TRI: {tri:.1f}, {desc})")
        print(f"   Nível: {nivel.upper()}")
        print(f"   Tamanho prompt: {len(prompt)} caracteres")
        print(f"   Primeiras 80 chars: {prompt[:80]}...")
        print()
    
    return todos_ok

def testar_com_questoes_reais():
    """Testa com questões reais do ENEM 2024"""
    print("=" * 70)
    print("🧪 TESTE 3: Questões Reais do ENEM 2024")
    print("=" * 70)
    print()
    
    questoes = carregar_questoes_2024_matematica()
    
    if not questoes:
        print("⚠️  Nenhuma questão encontrada")
        return False
    
    print(f"✅ {len(questoes)} questões de matemática carregadas")
    print()
    
    # Estatísticas por nível
    stats = {
        'facil': 0,
        'medio': 0,
        'dificil': 0,
        'sem_tri': 0
    }
    
    # Testar primeiras 10 questões
    for i, questao in enumerate(questoes[:10]):
        num = int(questao.get('number', 0))
        tri_info = obter_info_tri(num)
        tri_value = tri_info.get('TRI', 0)
        
        if tri_value == 0:
            stats['sem_tri'] += 1
            nivel = "SEM TRI"
        else:
            nivel = classificar_por_tri(tri_value)
            stats[nivel] += 1
        
        prompt = selecionar_prompt_por_tri(tri_value) if tri_value > 0 else "N/A"
        
        print(f"Questão {num}: TRI={tri_value:.1f}, Nível={nivel.upper()}, Prompt={len(prompt)} chars")
    
    print()
    print("📊 Estatísticas (primeiras 10 questões):")
    print(f"   Fácil: {stats['facil']}")
    print(f"   Médio: {stats['medio']}")
    print(f"   Difícil: {stats['dificil']}")
    print(f"   Sem TRI: {stats['sem_tri']}")
    print()
    
    return True

def testar_formatacao_questao():
    """Testa formatação de questão com prompt adaptativo"""
    print("=" * 70)
    print("🧪 TESTE 4: Formatação Completa")
    print("=" * 70)
    print()
    
    questoes = carregar_questoes_2024_matematica()
    
    if not questoes:
        print("⚠️  Nenhuma questão encontrada")
        return False
    
    # Testar com uma questão de cada nível
    questoes_teste = []
    niveis_encontrados = {'facil': False, 'medio': False, 'dificil': False}
    
    for questao in questoes:
        num = int(questao.get('number', 0))
        tri_info = obter_info_tri(num)
        tri_value = tri_info.get('TRI', 0)
        
        if tri_value > 0:
            nivel = classificar_por_tri(tri_value)
            if not niveis_encontrados[nivel] and nivel in niveis_encontrados:
                questoes_teste.append((questao, tri_value, nivel))
                niveis_encontrados[nivel] = True
                
                if all(niveis_encontrados.values()):
                    break
    
    for questao, tri, nivel in questoes_teste:
        num = int(questao.get('number', 0))
        prompt_base = selecionar_prompt_por_tri(tri)
        
        # Formatar questão
        questao_texto = ""
        if questao.get('context'):
            questao_texto += f"CONTEXTO:\n{questao['context']}\n\n"
        questao_texto += f"PERGUNTA:\n{questao.get('question', '')}\n\n"
        questao_texto += "ALTERNATIVAS:\n"
        for i, alt in enumerate(questao.get('alternatives', []), 1):
            letra = chr(64 + i)
            questao_texto += f"{letra}) {alt}\n"
        
        prompt_completo = prompt_base + questao_texto
        
        print(f"Questão {num} (TRI: {tri:.1f}, {nivel.upper()}):")
        print(f"   Prompt base: {len(prompt_base)} chars")
        print(f"   Questão: {len(questao_texto)} chars")
        print(f"   Total: {len(prompt_completo)} chars")
        print(f"   Primeiras 150 chars do prompt completo:")
        print(f"   {prompt_completo[:150]}...")
        print()
    
    return True

def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 TESTES DO SISTEMA DE PROMPTS ADAPTATIVOS")
    print("=" * 70)
    print()
    
    resultados = []
    
    # Teste 1: Classificação
    resultados.append(("Classificação por TRI", testar_classificacao_tri()))
    print()
    
    # Teste 2: Seleção de prompts
    resultados.append(("Seleção de Prompts", testar_prompts_por_tri()))
    print()
    
    # Teste 3: Questões reais
    resultados.append(("Questões Reais", testar_com_questoes_reais()))
    print()
    
    # Teste 4: Formatação completa
    resultados.append(("Formatação Completa", testar_formatacao_questao()))
    print()
    
    # Resumo
    print("=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    print()
    
    todos_ok = True
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")
        if not resultado:
            todos_ok = False
    
    print()
    if todos_ok:
        print("✅ TODOS OS TESTES PASSARAM!")
        print()
        print("🚀 Próximo passo: Executar avaliação completa com API")
        print("   python scripts/analise_enem/71_avaliar_com_prompts_adaptativos.py --limit 10")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("   Revise os erros acima")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

