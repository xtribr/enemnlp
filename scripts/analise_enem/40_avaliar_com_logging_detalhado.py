#!/usr/bin/env python3
"""
📊 Avaliação com Logging Detalhado - ENEM Matemática

====================================================

Este script executa a avaliação do ENEM com logging completo para
identificar exatamente quais questões o modelo acerta e erra.

Funcionalidades:
- Log individual de cada questão
- Resposta do modelo vs gabarito
- Análise por tópico e TRI
- Exportação para análise posterior

Uso:
    python 40_avaliar_com_logging_detalhado.py [--area matematica|todas]
    python 40_avaliar_com_logging_detalhado.py --area matematica --limit 10  # teste rápido
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

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

# Dados TRI das questões de matemática (ENEM 2024)
TRI_DATA = {
    136: {"TRI": 755.3, "H": "H13", "Nivel": "Muito Difícil", "Tema": "Grandezas e medidas", "Gab": "C"},
    137: {"TRI": 662.3, "H": "H28", "Nivel": "Intermediário", "Tema": "Estatística e probabilidade", "Gab": "E"},
    138: {"TRI": 705.0, "H": "H3", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "B"},
    139: {"TRI": 550.2, "H": "H26", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "A"},
    140: {"TRI": 660.6, "H": "H4", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "B"},
    141: {"TRI": 701.9, "H": "H20", "Nivel": "Intermediário", "Tema": "Álgebra e funções", "Gab": "B"},
    142: {"TRI": 661.7, "H": "H2", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "A"},
    143: {"TRI": 792.0, "H": "H18", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "D"},
    144: {"TRI": 636.5, "H": "H7", "Nivel": "Fácil", "Tema": "Geometria", "Gab": "D"},
    145: {"TRI": 613.0, "H": "H8", "Nivel": "Fácil", "Tema": "Geometria", "Gab": "D"},
    146: {"TRI": 809.9, "H": "H22", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "B"},
    147: {"TRI": 601.8, "H": "H1", "Nivel": "Fácil", "Tema": "Números e operações", "Gab": "B"},
    148: {"TRI": 776.1, "H": "H21", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "C"},
    149: {"TRI": 703.3, "H": "H14", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "E"},
    150: {"TRI": 836.2, "H": "H13", "Nivel": "Muito Difícil", "Tema": "Grandezas e medidas", "Gab": "C"},
    151: {"TRI": 750.4, "H": "H11", "Nivel": "Muito Difícil", "Tema": "Geometria", "Gab": "E"},
    152: {"TRI": 604.0, "H": "H25", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "A"},
    153: {"TRI": 622.8, "H": "H1", "Nivel": "Fácil", "Tema": "Números e operações", "Gab": "D"},
    154: {"TRI": 564.5, "H": "H27", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "C"},
    155: {"TRI": 723.7, "H": "H9", "Nivel": "Difícil", "Tema": "Geometria", "Gab": "E"},
    156: {"TRI": 591.2, "H": "H19", "Nivel": "Fácil", "Tema": "Álgebra e funções", "Gab": "B"},
    157: {"TRI": 611.7, "H": "H23", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "C"},
    158: {"TRI": 643.6, "H": "H4", "Nivel": "Fácil", "Tema": "Números e operações", "Gab": "C"},
    159: {"TRI": 678.4, "H": "H10", "Nivel": "Intermediário", "Tema": "Geometria", "Gab": "C"},
    160: {"TRI": 684.5, "H": "H16", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "D"},
    161: {"TRI": 738.7, "H": "H15", "Nivel": "Difícil", "Tema": "Grandezas e medidas", "Gab": "B"},
    162: {"TRI": 760.8, "H": "H5", "Nivel": "Muito Difícil", "Tema": "Números e operações", "Gab": "A"},
    163: {"TRI": 729.8, "H": "H12", "Nivel": "Difícil", "Tema": "Grandezas e medidas", "Gab": "D"},
    164: {"TRI": 712.4, "H": "H8", "Nivel": "Intermediário", "Tema": "Geometria", "Gab": "C"},
    165: {"TRI": 786.9, "H": "H30", "Nivel": "Muito Difícil", "Tema": "Análise combinatória", "Gab": "B"},
    166: {"TRI": 673.6, "H": "H19", "Nivel": "Intermediário", "Tema": "Álgebra e funções", "Gab": "E"},
    167: {"TRI": 701.9, "H": "H3", "Nivel": "Intermediário", "Tema": "Números e operações", "Gab": "D"},
    168: {"TRI": 625.9, "H": "H15", "Nivel": "Fácil", "Tema": "Grandezas e medidas", "Gab": "A"},
    169: {"TRI": 772.7, "H": "H28", "Nivel": "Muito Difícil", "Tema": "Estatística e probabilidade", "Gab": "E"},
    170: {"TRI": 729.4, "H": "H21", "Nivel": "Difícil", "Tema": "Álgebra e funções", "Gab": "C"},
    171: {"TRI": 787.2, "H": "H22", "Nivel": "Muito Difícil", "Tema": "Álgebra e funções", "Gab": "A"},
    172: {"TRI": 673.5, "H": "H17", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "D"},
    173: {"TRI": 647.1, "H": "H29", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "A"},
    174: {"TRI": 663.0, "H": "H6", "Nivel": "Intermediário", "Tema": "Geometria", "Gab": "C"},
    175: {"TRI": 693.9, "H": "H12", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "D"},
    176: {"TRI": 645.1, "H": "H24", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "B"},
    177: {"TRI": 673.9, "H": "H25", "Nivel": "Intermediário", "Tema": "Estatística e probabilidade", "Gab": "C"},
    178: {"TRI": 573.5, "H": "H27", "Nivel": "Fácil", "Tema": "Estatística e probabilidade", "Gab": "E"},
    179: {"TRI": 706.9, "H": "H16", "Nivel": "Intermediário", "Tema": "Grandezas e medidas", "Gab": "C"},
    180: {"TRI": 742.5, "H": "H2", "Nivel": "Difícil", "Tema": "Números e operações", "Gab": "E"},
}

# Prompt CoT oficial
PROMPT_COT = """Elabore uma explicação passo-a-passo que possibilite responder a questão de múltipla escolha abaixo. Apenas uma alternativa é correta.

Encerre a explicação com "Resposta: " seguido pela alternativa."""

# Few-shot examples (simplificados para o script)
FEW_SHOT_EXAMPLES = [
    {
        "question": "Uma pessoa comprou 3 produtos por R$ 15,00 cada. Qual foi o total gasto?",
        "alternatives": ["A. R$ 30,00", "B. R$ 45,00", "C. R$ 60,00", "D. R$ 75,00", "E. R$ 90,00"],
        "response": "Para calcular o total gasto, multiplico a quantidade de produtos pelo preço unitário:\n3 × R$ 15,00 = R$ 45,00\n\nResposta: B"
    },
    {
        "question": "Se x + 5 = 12, qual o valor de x?",
        "alternatives": ["A. 5", "B. 6", "C. 7", "D. 8", "E. 17"],
        "response": "Para encontrar x, isolo a variável:\nx + 5 = 12\nx = 12 - 5\nx = 7\n\nResposta: C"
    },
    {
        "question": "Um retângulo tem base 4 cm e altura 3 cm. Qual sua área?",
        "alternatives": ["A. 7 cm²", "B. 12 cm²", "C. 14 cm²", "D. 24 cm²", "E. 36 cm²"],
        "response": "A área de um retângulo é calculada por: Área = base × altura\nÁrea = 4 × 3 = 12 cm²\n\nResposta: B"
    }
]


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
    
    # Procurar padrão "Resposta: X" ou "Resposta: X."
    patterns = [
        r'[Rr]esposta:\s*([A-Ea-e])',
        r'[Rr]esposta:\s*\(?([A-Ea-e])\)?',
        r'[Aa]lternativa:\s*([A-Ea-e])',
        r'[Aa]lternativa\s+([A-Ea-e])',
        r'\b([A-Ea-e])\s*[.)\]]?\s*$',  # Última letra A-E no final
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response_text)
        if match:
            return match.group(1).upper()
    
    # Se não encontrou, procurar a última ocorrência de A, B, C, D ou E
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
                    temperature=0.1  # Baixa temperatura para consistência
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
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return None
    
    return None


def build_messages(question_data, use_captions=True):
    """Constrói as mensagens para o modelo."""
    messages = [{"role": "system", "content": PROMPT_COT}]
    
    # Adicionar few-shot examples
    for example in FEW_SHOT_EXAMPLES:
        user_msg = f"Questão: {example['question']}\n\nAlternativas:\n"
        user_msg += "\n".join(example['alternatives'])
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": example['response']})
    
    # Construir a questão atual
    question_text = question_data['question']
    
    # Adicionar captions (descrições de imagens) se disponíveis
    if use_captions and question_data.get('description'):
        descriptions = question_data['description']
        if descriptions:
            if isinstance(descriptions, list):
                for i, desc in enumerate(descriptions):
                    question_text += f"\n\n[Descrição da imagem {i+1}]: {desc}"
            else:
                question_text += f"\n\n[Descrição da imagem]: {descriptions}"
    
    # Formatar alternativas
    alternatives = question_data['alternatives']
    alt_text = ""
    for i, alt in enumerate(alternatives):
        letter = chr(65 + i)  # A, B, C, D, E
        alt_text += f"{letter}. {alt}\n"
    
    user_msg = f"Questão: {question_text}\n\nAlternativas:\n{alt_text}"
    messages.append({"role": "user", "content": user_msg})
    
    return messages


def load_enem_data():
    """Carrega os dados do ENEM 2024."""
    print("📥 Carregando dataset do ENEM 2024...")
    ds = load_dataset('maritaca-ai/enem', split='train')
    
    # Converter para lista
    questions = []
    for q in ds:
        q_num = int(q['id'].replace('questao_', ''))
        questions.append({
            'id': q['id'],
            'numero': q_num,
            'question': q['question'],
            'alternatives': q['alternatives'],
            'label': q['label'],
            'figures': q.get('figures', []),
            'description': q.get('description', []),
            'area': get_area(q_num)
        })
    
    return questions


def get_area(q_num):
    """Retorna a área de conhecimento baseada no número da questão."""
    if 1 <= q_num <= 45:
        return "languages"
    elif 46 <= q_num <= 90:
        return "human-sciences"
    elif 91 <= q_num <= 135:
        return "natural-sciences"
    elif 136 <= q_num <= 180:
        return "mathematics"
    return "unknown"


# =============================================================================
# FUNÇÃO PRINCIPAL DE AVALIAÇÃO
# =============================================================================

def evaluate_with_logging(area="matematica", limit=None, output_dir="results"):
    """Executa avaliação com logging detalhado."""
    
    print("=" * 70)
    print("📊 AVALIAÇÃO COM LOGGING DETALHADO - ENEM 2024")
    print("=" * 70)
    print()
    
    # Setup
    client, api_type = setup_api()
    print(f"✅ API configurada (versão: {api_type})")
    
    # Carregar dados
    questions = load_enem_data()
    print(f"✅ {len(questions)} questões carregadas")
    
    # Filtrar por área
    if area == "matematica":
        questions = [q for q in questions if q['area'] == 'mathematics']
        print(f"✅ Filtrado para matemática: {len(questions)} questões")
    elif area != "todas":
        print(f"⚠️  Área '{area}' não reconhecida. Usando todas.")
    
    # Aplicar limite
    if limit:
        questions = questions[:limit]
        print(f"✅ Limitado a {limit} questões")
    
    print()
    print("-" * 70)
    print("🚀 Iniciando avaliação...")
    print("-" * 70)
    print()
    
    # Resultados
    results = []
    correct = 0
    total = 0
    
    # Estatísticas por categoria
    stats_by_nivel = {"Fácil": {"correct": 0, "total": 0},
                      "Intermediário": {"correct": 0, "total": 0},
                      "Difícil": {"correct": 0, "total": 0},
                      "Muito Difícil": {"correct": 0, "total": 0}}
    
    stats_by_tema = {}
    
    for i, q in enumerate(questions):
        q_num = q['numero']
        total += 1
        
        # Obter dados TRI
        tri_info = TRI_DATA.get(q_num, {})
        tri = tri_info.get('TRI', 'N/A')
        nivel = tri_info.get('Nivel', 'N/A')
        tema = tri_info.get('Tema', 'N/A')
        habilidade = tri_info.get('H', 'N/A')
        
        print(f"[{i+1}/{len(questions)}] Questão {q_num} (TRI: {tri}, {nivel})")
        
        # Construir mensagens e chamar modelo
        messages = build_messages(q, use_captions=True)
        response = call_model(client, api_type, messages)
        
        if response is None:
            print(f"   ❌ Erro ao obter resposta")
            model_answer = None
            is_correct = False
        else:
            model_answer = extract_answer(response)
            correct_answer = q['label']
            is_correct = (model_answer == correct_answer)
            
            if is_correct:
                correct += 1
                print(f"   ✅ Correto! (Modelo: {model_answer}, Gabarito: {correct_answer})")
            else:
                print(f"   ❌ Errado! (Modelo: {model_answer}, Gabarito: {correct_answer})")
        
        # Atualizar estatísticas
        if nivel in stats_by_nivel:
            stats_by_nivel[nivel]['total'] += 1
            if is_correct:
                stats_by_nivel[nivel]['correct'] += 1
        
        if tema not in stats_by_tema:
            stats_by_tema[tema] = {'correct': 0, 'total': 0}
        stats_by_tema[tema]['total'] += 1
        if is_correct:
            stats_by_tema[tema]['correct'] += 1
        
        # Salvar resultado detalhado
        result = {
            'questao': q_num,
            'id': q['id'],
            'tri': tri,
            'nivel': nivel,
            'tema': tema,
            'habilidade': habilidade,
            'gabarito': q['label'],
            'resposta_modelo': model_answer,
            'correto': is_correct,
            'resposta_completa': response[:500] if response else None,  # Truncar para economizar espaço
            'questao_texto': q['question'][:300],  # Truncar
            'tem_figura': len(q.get('figures', [])) > 0,
            'tem_descricao': len(q.get('description', [])) > 0
        }
        results.append(result)
        
        # Pequena pausa para não sobrecarregar a API
        time.sleep(0.5)
    
    # Calcular métricas finais
    accuracy = correct / total if total > 0 else 0
    
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    print(f"📈 Acurácia Geral: {accuracy:.2%} ({correct}/{total})")
    print()
    
    # Resultados por nível
    print("📊 Por Nível de Dificuldade:")
    print("-" * 50)
    for nivel in ['Fácil', 'Intermediário', 'Difícil', 'Muito Difícil']:
        stats = stats_by_nivel[nivel]
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            print(f"   {nivel:15} | {acc:6.1%} ({stats['correct']}/{stats['total']})")
    
    print()
    print("📊 Por Tema:")
    print("-" * 50)
    for tema, stats in sorted(stats_by_tema.items(), key=lambda x: -x[1]['total']):
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            print(f"   {tema:25} | {acc:6.1%} ({stats['correct']}/{stats['total']})")
    
    # Listar erros
    erros = [r for r in results if not r['correto']]
    print()
    print(f"❌ QUESTÕES ERRADAS ({len(erros)}):")
    print("-" * 70)
    for erro in erros:
        print(f"   Q{erro['questao']} | TRI: {erro['tri']:>6} | {erro['nivel']:15} | {erro['tema']}")
        print(f"      Gabarito: {erro['gabarito']} | Modelo: {erro['resposta_modelo']}")
        print()
    
    # Salvar resultados
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/avaliacao_detalhada_{timestamp}.json"
    
    output_data = {
        'config': {
            'area': area,
            'limit': limit,
            'timestamp': timestamp,
            'model': 'sabia-3',
            'num_fewshot': 3,
            'use_captions': True
        },
        'metricas': {
            'accuracy': accuracy,
            'correct': correct,
            'total': total,
            'por_nivel': {k: {'accuracy': v['correct']/v['total'] if v['total'] > 0 else 0, **v} 
                        for k, v in stats_by_nivel.items()},
            'por_tema': {k: {'accuracy': v['correct']/v['total'] if v['total'] > 0 else 0, **v} 
                        for k, v in stats_by_tema.items()}
        },
        'resultados': results,
        'erros': erros
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"✅ Resultados salvos em: {output_file}")
    
    # Salvar também um CSV para fácil análise
    csv_file = f"{output_dir}/erros_matematica_{timestamp}.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("Questao,TRI,Nivel,Tema,Habilidade,Gabarito,Resposta_Modelo,Tem_Figura\n")
        for erro in erros:
            f.write(f"{erro['questao']},{erro['tri']},{erro['nivel']},{erro['tema']},"
                   f"{erro['habilidade']},{erro['gabarito']},{erro['resposta_modelo']},"
                   f"{erro['tem_figura']}\n")
    
    print(f"✅ CSV de erros salvo em: {csv_file}")
    
    return output_data


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Avaliação ENEM com logging detalhado")
    parser.add_argument("--area", type=str, default="matematica",
                       choices=["matematica", "todas"],
                       help="Área a avaliar (padrão: matematica)")
    parser.add_argument("--limit", type=int, default=None,
                       help="Limitar número de questões (para teste)")
    parser.add_argument("--output-dir", type=str, default="results",
                       help="Diretório de saída")
    
    args = parser.parse_args()
    
    evaluate_with_logging(
        area=args.area,
        limit=args.limit,
        output_dir=args.output_dir
    )

