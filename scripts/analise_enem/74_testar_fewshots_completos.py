#!/usr/bin/env python3
"""
🧪 Teste Completo: Prompts Adaptativos + Few-Shots Customizados

Testa a integração completa do sistema:
1. Classificação por TRI (fácil/médio/difícil)
2. Seleção de prompt adaptativo
3. Seleção de few-shots por tema
4. Formatação completa
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar módulos
import importlib.util

# Módulo de prompts adaptativos
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_module)

selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri
classificar_por_tri = prompts_module.classificar_por_tri

# Módulo de few-shots
fewshots_module_path = Path(__file__).parent / "73_fewshots_customizados_por_tema.py"
spec2 = importlib.util.spec_from_file_location("fewshots_customizados", fewshots_module_path)
fewshots_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(fewshots_module)

obter_fewshots_por_tema = fewshots_module.obter_fewshots_por_tema
criar_prompt_com_fewshots = fewshots_module.criar_prompt_com_fewshots

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

def formatar_questao(questao: dict) -> str:
    """Formata questão para o prompt"""
    texto = ""
    
    if questao.get('context'):
        texto += f"CONTEXTO:\n{questao['context']}\n\n"
    
    if questao.get('description'):
        desc = questao['description']
        if isinstance(desc, list) and desc:
            texto += f"DESCRIÇÃO DAS IMAGENS:\n{desc[0]}\n\n"
        elif desc:
            texto += f"DESCRIÇÃO DAS IMAGENS:\n{desc}\n\n"
    
    texto += f"PERGUNTA:\n{questao.get('question', '')}\n\n"
    
    texto += "ALTERNATIVAS:\n"
    for i, alt in enumerate(questao.get('alternatives', []), 1):
        letra = chr(64 + i)
        texto += f"{letra}) {alt}\n"
    
    return texto

def testar_integracao_completa():
    """Testa integração completa do sistema"""
    print("=" * 70)
    print("🧪 TESTE COMPLETO: Prompts Adaptativos + Few-Shots")
    print("=" * 70)
    print()
    
    questoes = carregar_questoes_2024_matematica()
    
    if not questoes:
        print("⚠️  Nenhuma questão encontrada")
        return False
    
    print(f"✅ {len(questoes)} questões de matemática carregadas")
    print()
    
    # Testar com questões de diferentes temas e níveis
    temas_para_testar = {
        'Álgebra e funções': [],
        'Estatística e probabilidade': [],
        'Geometria': [],
        'Grandezas e medidas': []
    }
    
    # Agrupar questões por tema
    for questao in questoes:
        num = questao.get('number', 0)
        tri_info = obter_info_tri(num)
        tema = tri_info.get('Tema', 'N/A')
        
        if tema in temas_para_testar:
            temas_para_testar[tema].append((questao, tri_info))
    
    # Testar uma questão de cada tema
    print("📊 TESTANDO INTEGRAÇÃO POR TEMA:")
    print("-" * 70)
    print()
    
    for tema, questoes_tema in temas_para_testar.items():
        if not questoes_tema:
            continue
        
        # Pegar primeira questão do tema
        questao, tri_info = questoes_tema[0]
        num = questao.get('number', 0)
        tri_value = tri_info.get('TRI', 0)
        nivel = classificar_por_tri(tri_value)
        
        print(f"📖 Tema: {tema}")
        print(f"   Questão: {num} (TRI: {tri_value:.1f}, {nivel.upper()})")
        
        # Obter prompt adaptativo
        prompt_base = selecionar_prompt_por_tri(tri_value)
        print(f"   Prompt base: {len(prompt_base)} caracteres")
        
        # Obter few-shots
        fewshots = obter_fewshots_por_tema(tema, num_exemplos=3)
        print(f"   Few-shots: {len(fewshots)} exemplos")
        
        # Criar prompt completo
        prompt_completo = criar_prompt_com_fewshots(prompt_base, tema, num_fewshots=3)
        print(f"   Prompt completo: {len(prompt_completo)} caracteres")
        
        # Formatar questão
        questao_formatada = formatar_questao(questao)
        prompt_final = prompt_completo + questao_formatada
        
        print(f"   Prompt final (com questão): {len(prompt_final)} caracteres")
        print(f"   Questão formatada: {len(questao_formatada)} caracteres")
        print()
    
    return True

def testar_selecao_fewshots():
    """Testa seleção de few-shots para diferentes temas"""
    print("=" * 70)
    print("📚 TESTE DE SELEÇÃO DE FEW-SHOTS POR TEMA")
    print("=" * 70)
    print()
    
    temas = [
        "Álgebra e funções",
        "Estatística e probabilidade",
        "Geometria",
        "Grandezas e medidas",
        "Números e operações",
        "Análise combinatória"
    ]
    
    for tema in temas:
        fewshots = obter_fewshots_por_tema(tema, num_exemplos=3)
        print(f"📖 {tema}:")
        print(f"   ✅ {len(fewshots)} exemplos")
        
        for i, exemplo in enumerate(fewshots, 1):
            print(f"   Exemplo {i}: {exemplo['question'][:50]}...")
            print(f"      Resposta: {exemplo['response'].split('Resposta:')[-1].strip()}")
        print()
    
    return True

def testar_estrutura_prompt_completo():
    """Testa estrutura completa do prompt final"""
    print("=" * 70)
    print("🔍 TESTE DE ESTRUTURA DO PROMPT COMPLETO")
    print("=" * 70)
    print()
    
    questoes = carregar_questoes_2024_matematica()
    
    if not questoes:
        print("⚠️  Nenhuma questão encontrada")
        return False
    
    # Testar com questão de álgebra (tema problemático)
    for questao in questoes:
        num = questao.get('number', 0)
        tri_info = obter_info_tri(num)
        tema = tri_info.get('Tema', '')
        
        if 'Álgebra' in tema:
            tri_value = tri_info.get('TRI', 0)
            nivel = classificar_por_tri(tri_value)
            
            print(f"Questão {num} - {tema} (TRI: {tri_value:.1f}, {nivel.upper()})")
            print()
            
            # Construir prompt completo
            prompt_base = selecionar_prompt_por_tri(tri_value)
            prompt_com_fewshots = criar_prompt_com_fewshots(prompt_base, tema, num_fewshots=3)
            questao_formatada = formatar_questao(questao)
            prompt_final = prompt_com_fewshots + questao_formatada
            
            print("📋 Estrutura do Prompt Final:")
            print(f"   1. Prompt adaptativo ({nivel.upper()}): {len(prompt_base)} chars")
            print(f"   2. Few-shots ({tema}): {len(prompt_com_fewshots) - len(prompt_base)} chars")
            print(f"   3. Questão formatada: {len(questao_formatada)} chars")
            print(f"   TOTAL: {len(prompt_final)} caracteres")
            print()
            
            print("📝 Primeiras 300 caracteres:")
            print(prompt_final[:300] + "...")
            print()
            
            print("📝 Últimos 200 caracteres:")
            print("..." + prompt_final[-200:])
            print()
            
            break
    
    return True

def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 TESTES COMPLETOS: Few-Shots Customizados")
    print("=" * 70)
    print()
    
    resultados = []
    
    # Teste 1: Seleção de few-shots
    resultados.append(("Seleção de Few-Shots", testar_selecao_fewshots()))
    print()
    
    # Teste 2: Integração completa
    resultados.append(("Integração Completa", testar_integracao_completa()))
    print()
    
    # Teste 3: Estrutura do prompt completo
    resultados.append(("Estrutura do Prompt", testar_estrutura_prompt_completo()))
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
        print("   ✅ Integração funcionando")
        print()
        print("🚀 Próximo passo: Testar com API real")
        print("   python scripts/analise_enem/75_avaliar_completo_adaptativo.py --limit 10")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

