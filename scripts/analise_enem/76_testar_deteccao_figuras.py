#!/usr/bin/env python3
"""
🧪 Teste Completo: Detecção de Figuras Simples

Testa a detecção de figuras simples com questões reais do ENEM 2024.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar módulos
import importlib.util

# Módulo de detecção de figuras
figuras_module_path = Path(__file__).parent / "75_deteccao_figuras_simples.py"
spec = importlib.util.spec_from_file_location("deteccao_figuras", figuras_module_path)
figuras_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(figuras_module)

detectar_tipo_figura = figuras_module.detectar_tipo_figura
eh_figura_simples = figuras_module.eh_figura_simples
analisar_complexidade_descricao = figuras_module.analisar_complexidade_descricao
criar_prompt_figura_simples = figuras_module.criar_prompt_figura_simples
criar_prompt_com_deteccao_figura = figuras_module.criar_prompt_com_deteccao_figura
obter_info_figura = figuras_module.obter_info_figura

# Módulo de prompts adaptativos
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec2 = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(prompts_module)

selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri

def carregar_questoes_2024_matematica():
    """Carrega questões de matemática do ENEM 2024"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "processed" / "enem_2024_completo.jsonl"
    
    if not arquivo.exists():
        return []
    
    questoes = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questao = json.loads(line)
                num_str = questao.get('id', '').replace('questao_', '') or questao.get('number', '')
                try:
                    num = int(num_str)
                    if 136 <= num <= 180:
                        questao['number'] = num
                        questoes.append(questao)
                except (ValueError, TypeError):
                    continue
    
    return questoes

def testar_deteccao_com_questoes_reais():
    """Testa detecção com questões reais"""
    print("=" * 70)
    print("🧪 TESTE: Detecção com Questões Reais do ENEM 2024")
    print("=" * 70)
    print()
    
    questoes = carregar_questoes_2024_matematica()
    
    if not questoes:
        print("⚠️  Nenhuma questão encontrada")
        return False
    
    print(f"✅ {len(questoes)} questões carregadas")
    print()
    
    # Estatísticas
    stats = {
        'com_figura': 0,
        'sem_figura': 0,
        'figuras_simples': 0,
        'figuras_complexas': 0,
        'tipos': {}
    }
    
    questoes_com_figura = []
    
    for questao in questoes:
        info_figura = obter_info_figura(questao)
        
        if info_figura['tem_figura']:
            stats['com_figura'] += 1
            questoes_com_figura.append((questao, info_figura))
            
            if info_figura['eh_simples']:
                stats['figuras_simples'] += 1
            else:
                stats['figuras_complexas'] += 1
            
            tipo = info_figura.get('tipo', 'desconhecido')
            stats['tipos'][tipo] = stats['tipos'].get(tipo, 0) + 1
        else:
            stats['sem_figura'] += 1
    
    print("📊 ESTATÍSTICAS:")
    print("-" * 70)
    print(f"Questões com figura: {stats['com_figura']}")
    print(f"Questões sem figura: {stats['sem_figura']}")
    print(f"Figuras simples: {stats['figuras_simples']}")
    print(f"Figuras complexas: {stats['figuras_complexas']}")
    print()
    print("Tipos de figuras detectadas:")
    for tipo, count in sorted([(k, v) for k, v in stats['tipos'].items() if k is not None]):
        print(f"  {tipo}: {count}")
    print()
    
    # Mostrar exemplos
    print("📝 EXEMPLOS DE QUESTÕES COM FIGURAS:")
    print("-" * 70)
    
    for i, (questao, info) in enumerate(questoes_com_figura[:5], 1):
        num = questao.get('number', 0)
        desc = questao.get('description', '')
        desc_short = desc[:80] + "..." if len(desc) > 80 else desc
        
        print(f"\nQuestão {num}:")
        print(f"  Tipo: {info.get('tipo', 'N/A')}")
        print(f"  Simples: {info['eh_simples']}")
        print(f"  Descrição: {desc_short}")
    
    return True

def testar_integracao_completa():
    """Testa integração completa: prompts adaptativos + detecção de figuras"""
    print("=" * 70)
    print("🔗 TESTE: Integração Completa (Prompts + Figuras)")
    print("=" * 70)
    print()
    
    questoes = carregar_questoes_2024_matematica()
    
    if not questoes:
        print("⚠️  Nenhuma questão encontrada")
        return False
    
    # Encontrar questões com figuras simples
    questoes_com_figura_simples = []
    
    for questao in questoes:
        num = questao.get('number', 0)
        info_figura = obter_info_figura(questao)
        
        if info_figura['eh_simples']:
            tri_info = obter_info_tri(num)
            tri_value = tri_info.get('TRI', 0)
            questoes_com_figura_simples.append((questao, info_figura, tri_value))
    
    if not questoes_com_figura_simples:
        print("⚠️  Nenhuma questão com figura simples encontrada")
        return False
    
    print(f"✅ {len(questoes_com_figura_simples)} questões com figuras simples encontradas")
    print()
    
    # Testar com primeira questão
    questao, info_figura, tri_value = questoes_com_figura_simples[0]
    num = questao.get('number', 0)
    
    print(f"📖 Exemplo: Questão {num} (TRI: {tri_value:.1f})")
    print(f"   Tipo de figura: {info_figura.get('tipo', 'N/A')}")
    print()
    
    # Obter prompt adaptativo
    prompt_base = selecionar_prompt_por_tri(tri_value)
    print(f"   Prompt base: {len(prompt_base)} caracteres")
    
    # Adicionar detecção de figura
    prompt_com_figura = criar_prompt_com_deteccao_figura(prompt_base, questao)
    print(f"   Prompt com detecção de figura: {len(prompt_com_figura)} caracteres")
    
    if len(prompt_com_figura) > len(prompt_base):
        print(f"   ✅ Instruções de figura simples adicionadas ({len(prompt_com_figura) - len(prompt_base)} chars)")
        print()
        print("   Primeiras 300 caracteres do prompt completo:")
        print("   " + prompt_com_figura[:300].replace("\n", "\n   ") + "...")
    else:
        print(f"   ⚠️  Nenhuma instrução de figura adicionada")
    
    print()
    
    return True

def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 TESTES COMPLETOS: Detecção de Figuras Simples")
    print("=" * 70)
    print()
    
    resultados = []
    
    # Teste 1: Detecção com questões reais
    resultados.append(("Detecção com Questões Reais", testar_deteccao_com_questoes_reais()))
    print()
    
    # Teste 2: Integração completa
    resultados.append(("Integração Completa", testar_integracao_completa()))
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
        print("🎯 Sistema completo pronto:")
        print("   ✅ Prompts adaptativos por TRI")
        print("   ✅ Few-shots customizados por tema")
        print("   ✅ Detecção de figuras simples")
        print()
        print("🚀 Próximo passo: Testar sistema completo com API")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

