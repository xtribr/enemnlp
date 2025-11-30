#!/usr/bin/env python3
"""
🔄 Sistema de Self-Consistency para BrainX

Executa a mesma questão múltiplas vezes e usa votação majoritária
para aumentar acurácia e reduzir erros aleatórios.

Impacto esperado: +3-5% acurácia
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

# Importar módulos existentes
import importlib.util

# Módulo de prompts adaptativos
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_module)

selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri

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

def configurar_api():
    """Configura API OpenAI/Maritaca"""
    api_key = os.getenv('CURSORMINIMAC') or os.getenv('MARITALK_API_SECRET_KEY')
    
    if not api_key:
        print("❌ Erro: Chave API não encontrada")
        sys.exit(1)
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://chat.maritaca.ai/api"
    )
    
    return client

def extrair_resposta(texto: str) -> Optional[str]:
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

def resolver_questao(client, questao: Dict, num_passagem: int = 1) -> Dict:
    """
    Resolve uma questão usando o modelo
    
    Args:
        client: Cliente OpenAI/Maritaca
        questao: Dados da questão
        num_passagem: Número da passagem (para logging)
        
    Returns:
        Dicionário com resposta e metadados
    """
    from scripts.analise_enem.77_avaliar_sistema_completo_adaptativo import (
        construir_prompt_completo, formatar_questao
    )
    
    # Construir prompt completo
    prompt_completo, info = construir_prompt_completo(questao)
    questao_formatada = formatar_questao(questao, use_captions=True)
    prompt_final = prompt_completo + questao_formatada
    
    try:
        response = client.chat.completions.create(
            model="sabia-3",
            messages=[
                {"role": "system", "content": "Você é um especialista em questões do ENEM."},
                {"role": "user", "content": prompt_final}
            ],
            temperature=0.1,  # Baixa temperatura para consistência
            max_tokens=2000
        )
        
        resposta_texto = response.choices[0].message.content
        resposta_extraida = extrair_resposta(resposta_texto)
        
        return {
            'resposta': resposta_extraida,
            'resposta_completa': resposta_texto,
            'passagem': num_passagem,
            'sucesso': resposta_extraida is not None
        }
    except Exception as e:
        return {
            'resposta': None,
            'erro': str(e),
            'passagem': num_passagem,
            'sucesso': False
        }

def resolver_com_self_consistency(
    client, 
    questao: Dict, 
    n_passagens: int = 5,
    min_consenso: int = 3
) -> Dict:
    """
    Resolve questão com self-consistency (múltiplas passagens)
    
    Args:
        client: Cliente OpenAI/Maritaca
        questao: Dados da questão
        n_passagens: Número de passagens (default: 5)
        min_consenso: Mínimo de respostas iguais para consenso (default: 3)
        
    Returns:
        Dicionário com resposta final e estatísticas
    """
    respostas = []
    resultados = []
    
    print(f"   🔄 Executando {n_passagens} passagens...")
    
    for i in range(n_passagens):
        resultado = resolver_questao(client, questao, num_passagem=i+1)
        resultados.append(resultado)
        
        if resultado['sucesso'] and resultado['resposta']:
            respostas.append(resultado['resposta'])
        
        # Pequeno delay entre passagens
        time.sleep(0.3)
    
    # Análise de respostas
    if not respostas:
        return {
            'resposta_final': None,
            'confianca': 0.0,
            'respostas': [],
            'resultados': resultados,
            'erro': 'Nenhuma resposta válida obtida'
        }
    
    # Contar frequência de respostas
    contador = Counter(respostas)
    resposta_mais_frequente = contador.most_common(1)[0]
    resposta_final = resposta_mais_frequente[0]
    frequencia = resposta_mais_frequente[1]
    
    # Calcular confiança (0-1)
    confianca = frequencia / len(respostas)
    
    # Verificar se há consenso suficiente
    tem_consenso = frequencia >= min_consenso
    
    return {
        'resposta_final': resposta_final,
        'confianca': confianca,
        'frequencia': frequencia,
        'total_passagens': len(respostas),
        'respostas_todas': respostas,
        'distribuicao': dict(contador),
        'tem_consenso': tem_consenso,
        'resultados': resultados
    }

def validar_resposta(resposta: Optional[str], alternativas: List[str]) -> tuple[bool, str]:
    """
    Valida se a resposta é válida
    
    Args:
        resposta: Resposta extraída
        alternativas: Lista de alternativas
        
    Returns:
        Tupla (é_válida, mensagem)
    """
    if not resposta:
        return False, "Resposta não encontrada"
    
    if resposta not in ['A', 'B', 'C', 'D', 'E']:
        return False, f"Resposta '{resposta}' não é uma alternativa válida"
    
    # Verificar se há alternativa correspondente
    indice = ord(resposta) - ord('A')
    if indice >= len(alternativas):
        return False, f"Resposta '{resposta}' está fora do range de alternativas"
    
    return True, "Resposta válida"

def avaliar_com_self_consistency(limit=None, n_passagens=5):
    """
    Avalia questões usando self-consistency
    
    Args:
        limit: Limite de questões (None = todas)
        n_passagens: Número de passagens por questão (default: 5)
    """
    from scripts.analise_enem.77_avaliar_sistema_completo_adaptativo import (
        carregar_questoes_2024_matematica
    )
    
    print("=" * 70)
    print("🔄 AVALIAÇÃO COM SELF-CONSISTENCY")
    print("=" * 70)
    print()
    print(f"📊 Configuração:")
    print(f"   - Passagens por questão: {n_passagens}")
    print(f"   - Método: Votação majoritária")
    print()
    
    # Configurar API
    client = configurar_api()
    
    # Carregar questões
    questions = carregar_questoes_2024_matematica()
    
    if limit:
        questions = questions[:limit]
    
    print(f"✅ {len(questions)} questões carregadas")
    print()
    
    # Estatísticas
    total = 0
    correct = 0
    correct_sem_consenso = 0
    stats_consenso = {
        'com_consenso': {'correct': 0, 'total': 0},
        'sem_consenso': {'correct': 0, 'total': 0}
    }
    
    resultados = []
    start_time = time.time()
    
    for i, q in enumerate(questions):
        q_num = q.get('number', 0)
        total += 1
        
        print(f"[{i+1}/{len(questions)}] Questão {q_num}")
        
        # Resolver com self-consistency
        resultado_sc = resolver_com_self_consistency(client, q, n_passagens=n_passagens)
        
        resposta_final = resultado_sc['resposta_final']
        confianca = resultado_sc['confianca']
        tem_consenso = resultado_sc['tem_consenso']
        
        # Validar resposta
        is_valid, msg = validar_resposta(resposta_final, q.get('alternatives', []))
        
        if not is_valid:
            print(f"   ⚠️  Resposta inválida: {msg}")
            resposta_final = None
        
        # Comparar com gabarito
        correct_answer = q.get('label', '')
        is_correct = (resposta_final == correct_answer) if resposta_final else False
        
        if is_correct:
            correct += 1
            print(f"   ✅ Correto! (Resposta: {resposta_final}, Confiança: {confianca:.1%})")
        else:
            print(f"   ❌ Errado! (Resposta: {resposta_final}, Gabarito: {correct_answer}, Confiança: {confianca:.1%})")
        
        # Estatísticas de consenso
        if tem_consenso:
            stats_consenso['com_consenso']['total'] += 1
            if is_correct:
                stats_consenso['com_consenso']['correct'] += 1
        else:
            stats_consenso['sem_consenso']['total'] += 1
            if is_correct:
                stats_consenso['sem_consenso']['correct'] += 1
                correct_sem_consenso += 1
        
        # Salvar resultado
        resultados.append({
            'numero': q_num,
            'resposta_final': resposta_final,
            'gabarito': correct_answer,
            'correto': is_correct,
            'confianca': confianca,
            'tem_consenso': tem_consenso,
            'distribuicao': resultado_sc.get('distribuicao', {}),
            'n_passagens': n_passagens
        })
        
        # Delay entre questões
        time.sleep(0.5)
    
    elapsed_time = time.time() - start_time
    
    # Estatísticas finais
    accuracy = correct / total if total > 0 else 0
    
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    print(f"Acurácia Geral: {accuracy:.2%} ({correct}/{total})")
    print(f"Tempo total: {elapsed_time:.1f}s ({elapsed_time/total:.1f}s por questão)")
    print()
    
    print("📊 Por Consenso:")
    print("-" * 50)
    for tipo, stats in stats_consenso.items():
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            print(f"{tipo.replace('_', ' ').title():<20} {stats['correct']:>3}/{stats['total']:<3} = {acc:>5.1f}%")
    print()
    
    # Salvar resultados
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"avaliacao_self_consistency_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'n_passagens': n_passagens,
            'stats_consenso': stats_consenso,
            'resultados': resultados,
            'timestamp': timestamp
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)
    print("✅ AVALIAÇÃO CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Avaliar com self-consistency")
    parser.add_argument("--limit", type=int, help="Limitar número de questões")
    parser.add_argument("--passagens", type=int, default=5, help="Número de passagens (default: 5)")
    
    args = parser.parse_args()
    
    avaliar_com_self_consistency(limit=args.limit, n_passagens=args.passagens)

