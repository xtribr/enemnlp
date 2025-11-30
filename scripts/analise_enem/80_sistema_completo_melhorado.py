#!/usr/bin/env python3
"""
🚀 Sistema Completo Melhorado - BrainX

Integra TODAS as melhorias para superar todos os modelos:
1. Prompts adaptativos por TRI
2. Few-shots customizados por tema
3. Detecção de figuras simples
4. Self-Consistency (múltiplas passagens)
5. Validação de respostas
6. Prompt ultra-simples para questões fáceis

Meta: 94%+ acurácia (superar GPT-4o com 93.85%)
"""

import os
import sys
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import openai
except ImportError:
    print("❌ Erro: openai não instalado")
    sys.exit(1)

# Importar todos os módulos
import importlib.util

# Módulos existentes
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_module)

fewshots_module_path = Path(__file__).parent / "73_fewshots_customizados_por_tema.py"
spec2 = importlib.util.spec_from_file_location("fewshots_customizados", fewshots_module_path)
fewshots_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(fewshots_module)

figuras_module_path = Path(__file__).parent / "75_deteccao_figuras_simples.py"
spec3 = importlib.util.spec_from_file_location("deteccao_figuras", figuras_module_path)
figuras_module = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(figuras_module)

prompt_simples_module_path = Path(__file__).parent / "79_prompt_ultra_simples_facil.py"
spec4 = importlib.util.spec_from_file_location("prompt_simples", prompt_simples_module_path)
prompt_simples_module = importlib.util.module_from_spec(spec4)
spec4.loader.exec_module(prompt_simples_module)

# Funções importadas
selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri
classificar_por_tri = prompts_module.classificar_por_tri
criar_prompt_com_fewshots = fewshots_module.criar_prompt_com_fewshots
criar_prompt_com_deteccao_figura = figuras_module.criar_prompt_com_deteccao_figura
obter_info_figura = figuras_module.obter_info_figura
aplicar_prompt_ultra_simples = prompt_simples_module.aplicar_prompt_ultra_simples

def configurar_api():
    """Configura API"""
    api_key = os.getenv('CURSORMINIMAC') or os.getenv('MARITALK_API_SECRET_KEY')
    if not api_key:
        print("❌ Erro: Chave API não encontrada")
        sys.exit(1)
    return openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")

def extrair_resposta(texto: str) -> Optional[str]:
    """Extrai resposta do modelo"""
    texto = texto.upper().strip()
    for letra in ['A', 'B', 'C', 'D', 'E']:
        if f"RESPOSTA: {letra}" in texto or f"ALTERNATIVA {letra}" in texto:
            return letra
    for letra in ['E', 'D', 'C', 'B', 'A']:
        if letra in texto:
            return letra
    return None

def validar_resposta(resposta: Optional[str], alternativas: List[str]) -> tuple[bool, str]:
    """Valida resposta"""
    if not resposta:
        return False, "Resposta não encontrada"
    if resposta not in ['A', 'B', 'C', 'D', 'E']:
        return False, f"Resposta '{resposta}' inválida"
    indice = ord(resposta) - ord('A')
    if indice >= len(alternativas):
        return False, f"Resposta fora do range"
    return True, "Resposta válida"

def construir_prompt_final(questao: dict) -> tuple[str, dict]:
    """
    Constrói prompt final com TODAS as melhorias
    
    Returns:
        (prompt_final, info)
    """
    num = questao.get('number', 0)
    
    # 1. Obter TRI
    tri_info = obter_info_tri(num)
    tri_value = tri_info.get('TRI', 0)
    nivel = classificar_por_tri(tri_value)
    tema = tri_info.get('Tema', 'N/A')
    
    # 2. Selecionar prompt adaptativo
    prompt_base = selecionar_prompt_por_tri(tri_value)
    
    # 3. Aplicar prompt ultra-simples se fácil
    prompt_com_simples = aplicar_prompt_ultra_simples(prompt_base, questao, tri_value)
    
    # 4. Adicionar few-shots (apenas para médio)
    if nivel == 'medio':
        prompt_com_fewshots = criar_prompt_com_fewshots(prompt_com_simples, tema, num_fewshots=3)
    else:
        prompt_com_fewshots = prompt_com_simples
    
    # 5. Adicionar detecção de figuras
    prompt_final = criar_prompt_com_deteccao_figura(prompt_com_fewshots, questao)
    
    return prompt_final, {
        'tri': tri_value,
        'nivel': nivel,
        'tema': tema,
        'tem_figura_simples': obter_info_figura(questao).get('eh_simples', False)
    }

def formatar_questao(questao: dict) -> str:
    """Formata questão"""
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

def resolver_questao_com_self_consistency(
    client, 
    questao: dict, 
    n_passagens: int = 5
) -> Dict:
    """Resolve questão com self-consistency"""
    respostas = []
    resultados = []
    
    prompt_final, info = construir_prompt_final(questao)
    questao_formatada = formatar_questao(questao)
    prompt_completo = prompt_final + questao_formatada
    
    for i in range(n_passagens):
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
            resposta_extraida = extrair_resposta(resposta_texto)
            
            if resposta_extraida:
                respostas.append(resposta_extraida)
            
            resultados.append({
                'resposta': resposta_extraida,
                'passagem': i+1,
                'sucesso': resposta_extraida is not None
            })
            
            time.sleep(0.3)
        except Exception as e:
            resultados.append({
                'resposta': None,
                'erro': str(e),
                'passagem': i+1,
                'sucesso': False
            })
    
    if not respostas:
        return {
            'resposta_final': None,
            'confianca': 0.0,
            'info': info
        }
    
    # Votação majoritária
    contador = Counter(respostas)
    resposta_mais_frequente = contador.most_common(1)[0]
    resposta_final = resposta_mais_frequente[0]
    frequencia = resposta_mais_frequente[1]
    confianca = frequencia / len(respostas)
    
    return {
        'resposta_final': resposta_final,
        'confianca': confianca,
        'frequencia': frequencia,
        'total_passagens': len(respostas),
        'distribuicao': dict(contador),
        'info': info
    }

def avaliar_sistema_completo_melhorado(limit=None, n_passagens=5):
    """Avalia com sistema completo melhorado"""
    from scripts.analise_enem.77_avaliar_sistema_completo_adaptativo import (
        carregar_questoes_2024_matematica
    )
    
    print("=" * 70)
    print("🚀 AVALIAÇÃO COM SISTEMA COMPLETO MELHORADO")
    print("=" * 70)
    print()
    print("✨ Melhorias ativas:")
    print("   1. ✅ Prompts adaptativos por TRI")
    print("   2. ✅ Few-shots customizados por tema")
    print("   3. ✅ Detecção de figuras simples")
    print("   4. ✅ Self-Consistency ({} passagens)".format(n_passagens))
    print("   5. ✅ Validação de respostas")
    print("   6. ✅ Prompt ultra-simples para fáceis")
    print()
    print("🎯 Meta: 94%+ acurácia (superar GPT-4o com 93.85%)")
    print()
    
    client = configurar_api()
    questions = carregar_questoes_2024_matematica()
    
    if limit:
        questions = questions[:limit]
    
    print(f"✅ {len(questions)} questões carregadas")
    print()
    
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
        q_num = q.get('number', 0)
        total += 1
        
        print(f"[{i+1}/{len(questions)}] Questão {q_num}")
        
        # Resolver com self-consistency
        resultado = resolver_questao_com_self_consistency(client, q, n_passagens=n_passagens)
        
        resposta_final = resultado['resposta_final']
        confianca = resultado['confianca']
        info = resultado['info']
        
        # Validar
        is_valid, msg = validar_resposta(resposta_final, q.get('alternatives', []))
        if not is_valid:
            resposta_final = None
        
        # Comparar
        correct_answer = q.get('label', '')
        is_correct = (resposta_final == correct_answer) if resposta_final else False
        
        if is_correct:
            correct += 1
            stats_by_nivel[info['nivel']]['correct'] += 1
            print(f"   ✅ Correto! (Resposta: {resposta_final}, Confiança: {confianca:.1%})")
        else:
            print(f"   ❌ Errado! (Resposta: {resposta_final}, Gabarito: {correct_answer}, Confiança: {confianca:.1%})")
        
        stats_by_nivel[info['nivel']]['total'] += 1
        
        resultados.append({
            'numero': q_num,
            'resposta': resposta_final,
            'gabarito': correct_answer,
            'correto': is_correct,
            'confianca': confianca,
            'nivel': info['nivel'],
            'tema': info['tema']
        })
        
        time.sleep(0.5)
    
    elapsed_time = time.time() - start_time
    accuracy = correct / total if total > 0 else 0
    
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    print(f"🎯 Acurácia Geral: {accuracy:.2%} ({correct}/{total})")
    print(f"⏱️  Tempo: {elapsed_time:.1f}s ({elapsed_time/total:.1f}s por questão)")
    print()
    
    print("📊 Por Nível:")
    print("-" * 50)
    for nivel, stats in stats_by_nivel.items():
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            print(f"{nivel.upper():<10} {stats['correct']:>3}/{stats['total']:<3} = {acc:>5.1f}%")
    print()
    
    # Comparação
    print("📈 Comparação:")
    print("-" * 50)
    print(f"BrainX (Atual):     86.59%")
    print(f"BrainX (Melhorado): {accuracy:.2%}")
    print(f"GPT-4o (Paper):    93.85%")
    print(f"Gap para GPT-4o:    {93.85 - accuracy*100:+.2f} pontos")
    print()
    
    if accuracy >= 0.94:
        print("🎉 PARABÉNS! BrainX superou GPT-4o!")
    elif accuracy >= 0.90:
        print("✅ Excelente! Muito próximo do GPT-4o!")
    else:
        print("⚠️  Ainda há espaço para melhorias")
    
    # Salvar
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"avaliacao_completa_melhorada_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'n_passagens': n_passagens,
            'stats_by_nivel': stats_by_nivel,
            'resultados': resultados,
            'timestamp': timestamp
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Avaliar com sistema completo melhorado")
    parser.add_argument("--limit", type=int, help="Limitar número de questões")
    parser.add_argument("--passagens", type=int, default=5, help="Número de passagens (default: 5)")
    args = parser.parse_args()
    
    avaliar_sistema_completo_melhorado(limit=args.limit, n_passagens=args.passagens)

