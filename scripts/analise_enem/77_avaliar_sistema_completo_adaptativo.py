#!/usr/bin/env python3
"""
🎯 Avaliação com Sistema Completo Adaptativo

Integra TODAS as melhorias:
1. Prompts adaptativos por TRI (fácil/médio/difícil)
2. Few-shots customizados por tema
3. Detecção de figuras simples

Uso:
    python 77_avaliar_sistema_completo_adaptativo.py --area matematica [--limit 10]
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
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

criar_prompt_com_fewshots = fewshots_module.criar_prompt_com_fewshots

# Módulo de detecção de figuras
figuras_module_path = Path(__file__).parent / "75_deteccao_figuras_simples.py"
spec3 = importlib.util.spec_from_file_location("deteccao_figuras", figuras_module_path)
figuras_module = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(figuras_module)

criar_prompt_com_deteccao_figura = figuras_module.criar_prompt_com_deteccao_figura
obter_info_figura = figuras_module.obter_info_figura

# Tentar importar dependências
try:
    import openai
except ImportError:
    print("❌ Erro: openai não instalado")
    print("   Execute: pip install openai")
    sys.exit(1)

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

def configurar_api():
    """Configura API OpenAI/Maritaca"""
    api_key = os.getenv('CURSORMINIMAC') or os.getenv('MARITALK_API_SECRET_KEY')
    
    if not api_key:
        print("❌ Erro: Chave API não encontrada")
        print("   Configure: export CURSORMINIMAC=...")
        sys.exit(1)
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.maritaca.ai/v1"
    )
    
    return client, 'v0'

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
                num_str = questao.get('id', '').replace('questao_', '') or questao.get('number', '')
                try:
                    num = int(num_str)
                    if 136 <= num <= 180:
                        questao['number'] = num
                        questoes.append(questao)
                except (ValueError, TypeError):
                    continue
    
    return questoes

def formatar_questao(questao: dict, use_captions: bool = True) -> str:
    """Formata questão para o prompt"""
    texto = ""
    
    if questao.get('context'):
        texto += f"CONTEXTO:\n{questao['context']}\n\n"
    
    if use_captions and questao.get('description'):
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

def extrair_resposta(texto: str) -> str:
    """Extrai resposta do modelo"""
    texto = texto.upper().strip()
    
    # Procurar por padrões comuns
    for letra in ['A', 'B', 'C', 'D', 'E']:
        if f"RESPOSTA: {letra}" in texto:
            return letra
        if f"ALTERNATIVA {letra}" in texto:
            return letra
        if f"LETRA {letra}" in texto:
            return letra
        if texto.endswith(letra) and len(texto) < 10:
            return letra
    
    # Procurar última ocorrência de A, B, C, D ou E
    for letra in ['E', 'D', 'C', 'B', 'A']:
        if letra in texto:
            return letra
    
    return None

def construir_prompt_completo(questao: dict) -> str:
    """
    Constrói prompt completo usando todas as melhorias:
    1. Prompt adaptativo por TRI
    2. Few-shots por tema
    3. Detecção de figuras simples
    """
    num = questao.get('number', 0)
    
    # 1. Obter TRI e classificar
    tri_info = obter_info_tri(num)
    tri_value = tri_info.get('TRI', 0)
    nivel = classificar_por_tri(tri_value)
    tema = tri_info.get('Tema', 'N/A')
    
    # 2. Selecionar prompt adaptativo
    prompt_base = selecionar_prompt_por_tri(tri_value)
    
    # 3. Adicionar few-shots (apenas para nível médio)
    if nivel == 'medio':
        prompt_com_fewshots = criar_prompt_com_fewshots(prompt_base, tema, num_fewshots=3)
    else:
        prompt_com_fewshots = prompt_base
    
    # 4. Adicionar detecção de figuras simples
    prompt_final = criar_prompt_com_deteccao_figura(prompt_com_fewshots, questao)
    
    return prompt_final, {
        'tri': tri_value,
        'nivel': nivel,
        'tema': tema,
        'tem_figura_simples': obter_info_figura(questao).get('eh_simples', False)
    }

def avaliar_sistema_completo(limit=None):
    """Avalia questões usando sistema completo adaptativo"""
    
    print("=" * 70)
    print("🎯 AVALIAÇÃO COM SISTEMA COMPLETO ADAPTATIVO")
    print("=" * 70)
    print()
    print("✨ Melhorias ativas:")
    print("   1. ✅ Prompts adaptativos por TRI")
    print("   2. ✅ Few-shots customizados por tema")
    print("   3. ✅ Detecção de figuras simples")
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    client, api_type = configurar_api()
    print("✅ API configurada")
    print()
    
    # Carregar questões
    print("📥 Carregando questões...")
    questions = carregar_questoes_2024_matematica()
    
    if limit:
        questions = questions[:limit]
    
    print(f"✅ {len(questions)} questões carregadas")
    print()
    
    # Estatísticas
    total = 0
    correct = 0
    stats_by_nivel = {
        'facil': {'correct': 0, 'total': 0},
        'medio': {'correct': 0, 'total': 0},
        'dificil': {'correct': 0, 'total': 0}
    }
    stats_by_tema = {}
    stats_figuras = {'com_figura_simples': {'correct': 0, 'total': 0}}
    
    resultados = []
    start_time = time.time()
    
    for i, q in enumerate(questions):
        q_num = q.get('number', 0)
        total += 1
        
        # Construir prompt completo
        prompt_completo, info = construir_prompt_completo(q)
        questao_formatada = formatar_questao(q, use_captions=True)
        prompt_final = prompt_completo + questao_formatada
        
        print(f"[{i+1}/{len(questions)}] Questão {q_num} (TRI: {info['tri']:.1f}, {info['nivel'].upper()}, {info['tema']})")
        if info['tem_figura_simples']:
            print(f"   🖼️  Figura simples detectada")
        
        # Chamar modelo
        try:
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[
                    {"role": "system", "content": "Você é um especialista em questões do ENEM."},
                    {"role": "user", "content": prompt_final}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            resposta_texto = response.choices[0].message.content
            model_answer = extrair_resposta(resposta_texto)
            correct_answer = q.get('label', '')
            is_correct = (model_answer == correct_answer)
            
            if is_correct:
                correct += 1
                stats_by_nivel[info['nivel']]['correct'] += 1
                print(f"   ✅ Correto! (Modelo: {model_answer}, Gabarito: {correct_answer})")
            else:
                print(f"   ❌ Errado! (Modelo: {model_answer}, Gabarito: {correct_answer})")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            model_answer = None
            is_correct = False
        
        stats_by_nivel[info['nivel']]['total'] += 1
        
        # Estatísticas por tema
        tema = info['tema']
        if tema not in stats_by_tema:
            stats_by_tema[tema] = {'correct': 0, 'total': 0}
        stats_by_tema[tema]['total'] += 1
        if is_correct:
            stats_by_tema[tema]['correct'] += 1
        
        # Estatísticas de figuras
        if info['tem_figura_simples']:
            stats_figuras['com_figura_simples']['total'] += 1
            if is_correct:
                stats_figuras['com_figura_simples']['correct'] += 1
        
        # Salvar resultado
        resultados.append({
            'numero': q_num,
            'tri': info['tri'],
            'nivel': info['nivel'],
            'tema': tema,
            'tem_figura_simples': info['tem_figura_simples'],
            'modelo': model_answer,
            'gabarito': correct_answer,
            'correto': is_correct
        })
        
        # Pequeno delay
        time.sleep(0.5)
    
    elapsed_time = time.time() - start_time
    
    # Estatísticas finais
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    print(f"Acurácia Geral: {correct}/{total} = {100*correct/total:.2f}%")
    print(f"Tempo total: {elapsed_time:.1f}s ({elapsed_time/total:.1f}s por questão)")
    print()
    
    print("📊 Por Nível de Dificuldade:")
    print("-" * 50)
    for nivel, stats in stats_by_nivel.items():
        if stats['total'] > 0:
            acc = 100 * stats['correct'] / stats['total']
            print(f"{nivel.upper():<10} {stats['correct']:>3}/{stats['total']:<3} = {acc:>5.1f}%")
    print()
    
    print("📊 Por Tema:")
    print("-" * 50)
    for tema, stats in sorted(stats_by_tema.items()):
        if stats['total'] > 0:
            acc = 100 * stats['correct'] / stats['total']
            print(f"{tema:<30} {stats['correct']:>3}/{stats['total']:<3} = {acc:>5.1f}%")
    print()
    
    if stats_figuras['com_figura_simples']['total'] > 0:
        stats_fig = stats_figuras['com_figura_simples']
        acc_fig = 100 * stats_fig['correct'] / stats_fig['total']
        print(f"📊 Questões com Figura Simples: {stats_fig['correct']}/{stats_fig['total']} = {acc_fig:.1f}%")
        print()
    
    # Salvar resultados
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"avaliacao_sistema_completo_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': total,
            'correct': correct,
            'accuracy': correct/total,
            'stats_by_nivel': stats_by_nivel,
            'stats_by_tema': stats_by_tema,
            'stats_figuras': stats_figuras,
            'resultados': resultados,
            'timestamp': timestamp
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)
    print("✅ AVALIAÇÃO CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Avaliar com sistema completo adaptativo")
    parser.add_argument("--limit", type=int, help="Limitar número de questões")
    
    args = parser.parse_args()
    
    avaliar_sistema_completo(limit=args.limit)

