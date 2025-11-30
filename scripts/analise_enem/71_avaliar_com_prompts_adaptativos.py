#!/usr/bin/env python3
"""
🎯 Avaliação com Prompts Adaptativos por TRI

Integra o sistema de prompts adaptativos no processo de avaliação.
Usa prompts diferentes baseados no TRI da questão.

Uso:
    python 71_avaliar_com_prompts_adaptativos.py --area matematica [--limit 10]
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# Importar sistema de prompts adaptativos
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importar funções do módulo de prompts adaptativos
import importlib.util
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_module)

selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri
obter_tri_questao = prompts_module.obter_tri_questao

# Tentar importar dependências
try:
    from datasets import load_dataset
except ImportError:
    print("❌ Erro: datasets não instalado")
    print("   Execute: pip install datasets")
    sys.exit(1)

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

def formatar_questao(questao: dict, use_captions: bool = True) -> str:
    """Formata questão para o prompt"""
    texto = ""
    
    if questao.get('context'):
        texto += f"CONTEXTO:\n{questao['context']}\n\n"
    
    if use_captions and questao.get('description'):
        texto += f"DESCRIÇÃO DAS IMAGENS:\n{questao['description']}\n\n"
    
    texto += f"PERGUNTA:\n{questao['question']}\n\n"
    
    texto += "ALTERNATIVAS:\n"
    for i, alt in enumerate(questao.get('alternatives', []), 1):
        letra = chr(64 + i)  # A, B, C, D, E
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

def avaliar_com_prompts_adaptativos(area="matematica", limit=None):
    """Avalia questões usando prompts adaptativos por TRI"""
    
    print("=" * 70)
    print("🎯 AVALIAÇÃO COM PROMPTS ADAPTATIVOS POR TRI")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    client, api_type = configurar_api()
    print("✅ API configurada")
    print()
    
    # Carregar questões
    print("📥 Carregando questões...")
    dataset = load_dataset("maritaca-ai/enem", split="test")
    
    if area == "matematica":
        questions = [q for q in dataset if q['area'] == 'mathematics']
    elif area == "todas":
        questions = list(dataset)
    else:
        questions = [q for q in dataset if q['area'] == area]
    
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
    
    resultados = []
    start_time = time.time()
    
    for i, q in enumerate(questions):
        q_num = int(q['number'])
        total += 1
        
        # Obter TRI e classificar
        tri_info = obter_info_tri(q_num)
        tri_value = tri_info.get('TRI', 0)
        nivel = 'facil' if tri_value < 650 else ('medio' if tri_value <= 750 else 'dificil')
        
        print(f"[{i+1}/{len(questions)}] Questão {q_num} (TRI: {tri_value:.1f}, {nivel.upper()})")
        
        # Selecionar prompt adaptativo
        prompt_base = selecionar_prompt_por_tri(tri_value)
        questao_formatada = formatar_questao(q, use_captions=True)
        prompt_completo = prompt_base + questao_formatada
        
        # Chamar modelo
        try:
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[
                    {"role": "system", "content": "Você é um especialista em questões do ENEM."},
                    {"role": "user", "content": prompt_completo}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            resposta_texto = response.choices[0].message.content
            model_answer = extrair_resposta(resposta_texto)
            correct_answer = q['label']
            is_correct = (model_answer == correct_answer)
            
            if is_correct:
                correct += 1
                stats_by_nivel[nivel]['correct'] += 1
                print(f"   ✅ Correto! (Modelo: {model_answer}, Gabarito: {correct_answer})")
            else:
                print(f"   ❌ Errado! (Modelo: {model_answer}, Gabarito: {correct_answer})")
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            model_answer = None
            is_correct = False
        
        stats_by_nivel[nivel]['total'] += 1
        
        # Salvar resultado
        resultados.append({
            'numero': q_num,
            'tri': tri_value,
            'nivel': nivel,
            'tema': tri_info.get('Tema', 'N/A'),
            'modelo': model_answer,
            'gabarito': correct_answer,
            'correto': is_correct
        })
        
        # Pequeno delay para não sobrecarregar API
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
    
    # Salvar resultados
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"avaliacao_prompts_adaptativos_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'area': area,
            'total': total,
            'correct': correct,
            'accuracy': correct/total,
            'stats_by_nivel': stats_by_nivel,
            'resultados': resultados,
            'timestamp': timestamp
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)
    print("✅ AVALIAÇÃO CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Avaliar com prompts adaptativos")
    parser.add_argument("--area", default="matematica", help="Área (matematica, todas)")
    parser.add_argument("--limit", type=int, help="Limitar número de questões")
    
    args = parser.parse_args()
    
    avaliar_com_prompts_adaptativos(area=args.area, limit=args.limit)

