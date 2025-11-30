#!/usr/bin/env python3
"""
🚀 Iniciar Treinamento/Avaliação ENEM 2025
===========================================

Este script inicia a avaliação das 180 questões do ENEM 2025 usando Maritaca Sabiá-3.

Uso:
    python 55_iniciar_treinamento_2025.py [--area todas|linguagens|humanas|natureza|matematica] [--limit N]
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import openai
except ImportError:
    print("❌ Erro: openai não instalado")
    print("   Execute: pip install openai")
    sys.exit(1)

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

PROMPT_COT_IMPROVED = """Você é um especialista em resolução de questões do ENEM. Sua tarefa é analisar a questão de múltipla escolha abaixo, elaborar uma explicação passo-a-passo detalhada e, por fim, indicar a alternativa correta.

Siga rigorosamente os passos abaixo:
1. **Leitura Atenta e Compreensão do Enunciado:** Leia a questão completa, incluindo textos de apoio, gráficos, tabelas ou figuras. Identifique o que está sendo pedido e quais são as informações fornecidas.
2. **Identificação do Tipo de Problema:** Classifique a questão em uma área do conhecimento e identifique os conceitos envolvidos.
3. **Extração de Dados Relevantes:** Liste todos os dados numéricos e informações cruciais presentes no enunciado, figuras ou tabelas.
4. **Definição da Estratégia de Resolução:** Descreva o plano de ataque para resolver o problema.
5. **Cálculos e Desenvolvimento:** Execute os cálculos passo a passo, mostrando claramente cada etapa.
6. **Verificação e Validação:** Revise os cálculos e o raciocínio.
7. **Comparação com Alternativas:** Compare o resultado obtido com as alternativas fornecidas.
8. **Resposta Final:** Indique a alternativa correta.

Apenas uma alternativa é correta. Encerre a explicação com "Resposta: " seguido pela alternativa."""

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def setup_api():
    """Configura a API da Maritaca."""
    api_key = os.environ.get('CURSORMINIMAC') or os.environ.get('MARITALK_API_SECRET_KEY')
    
    if not api_key:
        print("❌ Erro: Chave API não encontrada")
        print("   Configure CURSORMINIMAC ou MARITALK_API_SECRET_KEY")
        sys.exit(1)
    
    # Detectar versão do openai
    openai_version = int(openai.__version__.split('.')[0])
    
    if openai_version >= 1:
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://chat.maritaca.ai/api"
        )
        return client, "new"
    else:
        openai.api_key = api_key
        openai.api_base = "https://chat.maritaca.ai/api"
        return None, "old"

def extract_answer(response_text):
    """Extrai a resposta (A, B, C, D ou E) do texto do modelo."""
    import re
    patterns = [
        r'[Rr]esposta:\s*([A-Ea-e])',
        r'[Rr]esposta:\s*\(?([A-Ea-e])\)?',
        r'[Aa]lternativa:\s*([A-Ea-e])',
        r'\b([A-Ea-e])\s*[.)\]]?\s*$',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response_text)
        if match:
            return match.group(1).upper()
    
    letters = re.findall(r'\b([A-Ea-e])[.)\]]?\b', response_text)
    if letters:
        return letters[-1].upper()
    
    return None

def call_model(client, api_type, messages, max_retries=3):
    """Chama o modelo com retry."""
    for attempt in range(max_retries):
        try:
            if api_type == "new":
                response = client.chat.completions.create(
                    model="sabia-3",
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.1
                )
                return response.choices[0].message.content
            else:
                response = openai.ChatCompletion.create(
                    model="sabia-3",
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.1
                )
                return response.choices[0].message.content
        except Exception as e:
            print(f"   ⚠️  Tentativa {attempt + 1} falhou: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None
    return None

def build_messages(question_data):
    """Constrói as mensagens para o modelo."""
    messages = [{"role": "system", "content": PROMPT_COT_IMPROVED}]
    
    # Construir a questão
    question_text = question_data.get('question', '')
    context = question_data.get('context', '')
    
    if context:
        question_text = f"{context}\n\n{question_text}" if question_text else context
    
    # Adicionar descrição de imagem se houver
    if question_data.get('image_description'):
        question_text += f"\n\n[Descrição da imagem]: {question_data['image_description']}"
    
    # Formatar alternativas
    alternatives = question_data.get('alternatives', [])
    alt_text = ""
    for i, alt in enumerate(alternatives):
        if alt and alt.strip():
            letter = chr(65 + i)  # A, B, C, D, E
            alt_text += f"{letter}. {alt}\n"
    
    user_msg = f"Questão: {question_text}\n\nAlternativas:\n{alt_text}"
    messages.append({"role": "user", "content": user_msg})
    
    return messages

def load_questions_2025(area: str = "todas"):
    """Carrega questões do ENEM 2025."""
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    if area == "todas":
        arquivo = processed_dir / "enem_2025_completo.jsonl"
    else:
        area_map = {
            'linguagens': 'languages',
            'humanas': 'human-sciences',
            'natureza': 'natural-sciences',
            'matematica': 'mathematics'
        }
        area_norm = area_map.get(area.lower(), area)
        arquivo = processed_dir / f"enem_2025_{area_norm}.jsonl"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        print("   Execute primeiro: python 54_integrar_todas_questoes_2025.py")
        sys.exit(1)
    
    questions = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                q = json.loads(line)
                # Filtrar por área se necessário
                if area != "todas":
                    area_map = {
                        'linguagens': 'languages',
                        'humanas': 'human-sciences',
                        'natureza': 'natural-sciences',
                        'matematica': 'mathematics'
                    }
                    area_norm = area_map.get(area.lower(), area)
                    if q.get('area') != area_norm:
                        continue
                # Filtrar questões sem label válido
                if not q.get('label') or q.get('label') == 'ANULADO':
                    continue
                questions.append(q)
    
    return questions

def main():
    parser = argparse.ArgumentParser(description="Avaliação ENEM 2025 com Maritaca")
    parser.add_argument("--area", type=str, default="todas",
                       help="Área para avaliar (todas, linguagens, humanas, natureza, matematica)")
    parser.add_argument("--limit", type=int, default=None,
                       help="Número máximo de questões para avaliar (para testes)")
    args = parser.parse_args()
    
    print("=" * 70)
    print("🚀 INICIANDO TREINAMENTO/AVALIAÇÃO - ENEM 2025")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    client, api_type = setup_api()
    print("✅ API configurada")
    
    # Carregar questões
    print(f"\n📥 Carregando questões de {args.area.upper()}...")
    questions = load_questions_2025(args.area)
    
    if args.limit:
        questions = questions[:args.limit]
    
    print(f"✅ {len(questions)} questões carregadas")
    
    if not questions:
        print("❌ Nenhuma questão para avaliar")
        sys.exit(1)
    
    # Estatísticas iniciais
    print("\n📊 Estatísticas das Questões:")
    stats = defaultdict(int)
    for q in questions:
        stats[q.get('area', 'unknown')] += 1
    for area, count in sorted(stats.items()):
        print(f"  {area}: {count} questões")
    
    # Iniciar avaliação
    print(f"\n🎯 Iniciando avaliação de {len(questions)} questões...")
    print()
    
    results = []
    correct_count = 0
    start_time = time.time()
    
    for i, question_data in enumerate(questions):
        q_id = question_data.get('id', 'unknown')
        q_num = question_data.get('number', 'unknown')
        correct_label = question_data.get('label', '').upper()
        area = question_data.get('area', 'unknown')
        
        print(f"[{i+1}/{len(questions)}] Questão {q_num} ({area}) - ID: {q_id}")
        
        # Construir mensagens
        messages = build_messages(question_data)
        
        # Chamar modelo
        model_response = call_model(client, api_type, messages)
        
        if model_response:
            model_answer = extract_answer(model_response)
            is_correct = (model_answer == correct_label) if model_answer else False
            
            if is_correct:
                correct_count += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"  {status} Esperado: {correct_label}, Modelo: {model_answer or 'N/A'}")
            
            results.append({
                'id': q_id,
                'number': q_num,
                'area': area,
                'correct_label': correct_label,
                'model_answer': model_answer,
                'model_response_raw': model_response[:200] + "..." if len(model_response) > 200 else model_response,
                'correto': is_correct,
                'has_images': question_data.get('has_images', False)
            })
        else:
            print(f"  ⚠️  Erro ao obter resposta do modelo")
            results.append({
                'id': q_id,
                'number': q_num,
                'area': area,
                'correct_label': correct_label,
                'model_answer': None,
                'model_response_raw': None,
                'correto': False,
                'has_images': question_data.get('has_images', False)
            })
        
        # Mostrar progresso
        accuracy = (correct_count / (i + 1)) * 100
        elapsed = time.time() - start_time
        avg_time = elapsed / (i + 1)
        remaining = avg_time * (len(questions) - i - 1)
        
        print(f"  Progresso: {accuracy:.1f}% | Tempo: {elapsed:.0f}s | Restante: ~{remaining:.0f}s")
        print()
        
        # Pequena pausa para não sobrecarregar a API
        time.sleep(0.5)
    
    # Calcular estatísticas finais
    final_accuracy = (correct_count / len(questions)) * 100 if questions else 0
    total_time = time.time() - start_time
    
    # Estatísticas por área
    area_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in results:
        area = r['area']
        area_stats[area]['total'] += 1
        if r['correto']:
            area_stats[area]['correct'] += 1
    
    # Salvar resultados
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"avaliacao_enem_2025_{args.area}_{timestamp}.json"
    
    output_data = {
        'timestamp': timestamp,
        'area': args.area,
        'total_questions': len(questions),
        'correct_answers': correct_count,
        'accuracy': final_accuracy,
        'total_time_seconds': total_time,
        'area_stats': {
            area: {
                'total': stats['total'],
                'correct': stats['correct'],
                'accuracy': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            }
            for area, stats in area_stats.items()
        },
        'results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # Mostrar resultados
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    print(f"Total de questões: {len(questions)}")
    print(f"Acertos: {correct_count}")
    print(f"Acurácia geral: {final_accuracy:.2f}%")
    print(f"Tempo total: {total_time:.1f} segundos")
    print(f"Tempo médio por questão: {total_time/len(questions):.1f} segundos")
    print()
    
    print("📊 Por Área:")
    for area in sorted(area_stats.keys()):
        stats = area_stats[area]
        acc = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {area:20s}: {stats['correct']:3d}/{stats['total']:3d} = {acc:5.1f}%")
    
    print()
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)
    print("✅ AVALIAÇÃO CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()

