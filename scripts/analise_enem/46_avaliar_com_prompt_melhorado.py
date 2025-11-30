#!/usr/bin/env python3
"""
📊 Avaliação com Prompt Melhorado - ENEM Matemática
====================================================

Este script executa a avaliação do ENEM com:
- Few-shots específicos para questões com figuras/tabelas
- Instruções melhoradas para leitura cuidadosa de enunciados
- Prompt otimizado baseado na análise de correlação

Uso:
    python 46_avaliar_com_prompt_melhorado.py [--area matematica|todas] [--limit N]
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

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

# Prompt CoT melhorado com instruções detalhadas
PROMPT_COT_MELHORADO = """Você é um especialista em resolver questões de matemática do ENEM. Siga estas instruções cuidadosamente:

**INSTRUÇÕES DE LEITURA:**
1. Leia o enunciado COMPLETO antes de começar qualquer cálculo
2. Identifique TODAS as informações fornecidas (números, unidades, condições)
3. Preste atenção especial a palavras-chave: "máximo", "mínimo", "exatamente", "pelo menos", "no máximo"
4. Se houver figuras, gráficos ou tabelas, analise-os com atenção antes de responder
5. Verifique as unidades de medida e se precisam ser convertidas
6. Identifique o que está sendo pedido na questão

**METODOLOGIA DE RESOLUÇÃO:**
1. Identifique o tipo de problema (álgebra, geometria, estatística, etc.)
2. Liste todas as informações conhecidas
3. Determine qual fórmula ou método usar
4. Execute os cálculos passo a passo
5. Verifique se a resposta faz sentido (dimensões, ordem de grandeza)
6. Compare com as alternativas e escolha a correta

**IMPORTANTE:**
- Se a questão mencionar figuras, gráficos ou tabelas, use essas informações na resolução
- Verifique se há alguma condição especial ou restrição no enunciado
- Evite erros de interpretação: leia cada palavra cuidadosamente
- Encerre sempre com "Resposta: " seguido pela letra da alternativa (A, B, C, D ou E)

Agora, resolva a questão abaixo seguindo essas instruções:"""

# Few-shot examples básicos (sem figuras)
FEW_SHOT_BASICOS = [
    {
        "question": "Uma pessoa comprou 3 produtos por R$ 15,00 cada. Qual foi o total gasto?",
        "alternatives": ["A. R$ 30,00", "B. R$ 45,00", "C. R$ 60,00", "D. R$ 75,00", "E. R$ 90,00"],
        "response": """PASSO 1 - Leitura cuidadosa: A questão pede o total gasto na compra de 3 produtos, cada um custando R$ 15,00.

PASSO 2 - Identificação: Tipo de problema: multiplicação simples.

PASSO 3 - Cálculo: Total = 3 × R$ 15,00 = R$ 45,00

PASSO 4 - Verificação: A resposta R$ 45,00 faz sentido e corresponde à alternativa B.

Resposta: B"""
    },
    {
        "question": "Se x + 5 = 12, qual o valor de x?",
        "alternatives": ["A. 5", "B. 6", "C. 7", "D. 8", "E. 17"],
        "response": """PASSO 1 - Leitura cuidadosa: A questão pede o valor de x em uma equação linear simples.

PASSO 2 - Identificação: Tipo de problema: equação do primeiro grau.

PASSO 3 - Cálculo: 
x + 5 = 12
x = 12 - 5
x = 7

PASSO 4 - Verificação: Substituindo x = 7: 7 + 5 = 12 ✓

Resposta: C"""
    },
    {
        "question": "Um retângulo tem base 4 cm e altura 3 cm. Qual sua área?",
        "alternatives": ["A. 7 cm²", "B. 12 cm²", "C. 14 cm²", "D. 24 cm²", "E. 36 cm²"],
        "response": """PASSO 1 - Leitura cuidadosa: A questão pede a área de um retângulo com base 4 cm e altura 3 cm.

PASSO 2 - Identificação: Tipo de problema: cálculo de área de retângulo.

PASSO 3 - Cálculo: 
Área = base × altura
Área = 4 cm × 3 cm = 12 cm²

PASSO 4 - Verificação: A resposta 12 cm² está correta e corresponde à alternativa B.

Resposta: B"""
    }
]

# Few-shot examples com figuras/tabelas
FEW_SHOT_COM_FIGURAS = [
    {
        "question": "A tabela abaixo mostra a quantidade de alunos por turma em uma escola. Qual turma tem mais alunos?\n\n[Descrição da tabela]: Tabela com 3 colunas: Turma, Número de Alunos. Linha 1: A, 25. Linha 2: B, 30. Linha 3: C, 28.",
        "alternatives": ["A. Turma A", "B. Turma B", "C. Turma C", "D. Todas têm o mesmo número", "E. Não é possível determinar"],
        "response": """PASSO 1 - Leitura cuidadosa: A questão pede para identificar qual turma tem mais alunos, usando informações de uma tabela.

PASSO 2 - Análise da tabela: 
- Turma A: 25 alunos
- Turma B: 30 alunos
- Turma C: 28 alunos

PASSO 3 - Comparação: Comparando os valores: 30 > 28 > 25. Portanto, a Turma B tem mais alunos.

PASSO 4 - Verificação: A resposta Turma B (alternativa B) está correta.

Resposta: B"""
    },
    {
        "question": "O gráfico abaixo mostra a evolução das vendas de uma loja ao longo de 4 meses. Em qual mês as vendas foram maiores?\n\n[Descrição do gráfico]: Gráfico de barras com 4 barras. Janeiro: 100 unidades. Fevereiro: 120 unidades. Março: 90 unidades. Abril: 110 unidades.",
        "alternatives": ["A. Janeiro", "B. Fevereiro", "C. Março", "D. Abril", "E. Todos os meses foram iguais"],
        "response": """PASSO 1 - Leitura cuidadosa: A questão pede para identificar o mês com maior venda usando um gráfico de barras.

PASSO 2 - Análise do gráfico:
- Janeiro: 100 unidades
- Fevereiro: 120 unidades
- Março: 90 unidades
- Abril: 110 unidades

PASSO 3 - Comparação: O maior valor é 120 unidades, correspondente a Fevereiro.

PASSO 4 - Verificação: A resposta Fevereiro (alternativa B) está correta.

Resposta: B"""
    },
    {
        "question": "A figura abaixo mostra um triângulo retângulo. Se o cateto adjacente mede 3 cm e a hipotenusa mede 5 cm, qual é a medida do cateto oposto?\n\n[Descrição da figura]: Triângulo retângulo com hipotenusa de 5 cm, cateto adjacente de 3 cm e cateto oposto desconhecido.",
        "alternatives": ["A. 2 cm", "B. 4 cm", "C. 6 cm", "D. 8 cm", "E. 10 cm"],
        "response": """PASSO 1 - Leitura cuidadosa: A questão pede o cateto oposto de um triângulo retângulo, conhecendo a hipotenusa (5 cm) e o cateto adjacente (3 cm).

PASSO 2 - Identificação: Tipo de problema: Teorema de Pitágoras.

PASSO 3 - Cálculo usando Teorema de Pitágoras:
a² + b² = c²
(3)² + b² = (5)²
9 + b² = 25
b² = 25 - 9 = 16
b = √16 = 4 cm

PASSO 4 - Verificação: 3² + 4² = 9 + 16 = 25 = 5² ✓

Resposta: B"""
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
                    max_tokens=2000,
                    temperature=0.0  # Temperatura zero para consistência
                )
                return response.choices[0].message.content
            else:
                response = openai.ChatCompletion.create(
                    model="sabia-3",
                    messages=messages,
                    max_tokens=2000,
                    temperature=0.0
                )
                return response.choices[0].message.content
        except Exception as e:
            print(f"   ⚠️  Tentativa {attempt + 1} falhou: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return None
    return None

def build_messages(question_data, use_captions=True, tem_figura=False):
    """Constrói as mensagens para o modelo com few-shots apropriados."""
    messages = [{"role": "system", "content": PROMPT_COT_MELHORADO}]
    
    # Escolher few-shots baseado na presença de figuras
    if tem_figura:
        # Usar 2 exemplos básicos + 2 exemplos com figuras
        few_shots = FEW_SHOT_BASICOS[:2] + FEW_SHOT_COM_FIGURAS[:2]
    else:
        # Usar apenas exemplos básicos
        few_shots = FEW_SHOT_BASICOS
    
    # Adicionar few-shot examples
    for example in few_shots:
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
    """Determina a área baseado no número da questão."""
    if 1 <= q_num <= 45:
        return 'Linguagens'
    elif 46 <= q_num <= 90:
        return 'Humanas'
    elif 91 <= q_num <= 135:
        return 'Natureza'
    elif 136 <= q_num <= 180:
        return 'Matemática'
    return 'Desconhecida'

# =============================================================================
# FUNÇÃO PRINCIPAL DE AVALIAÇÃO
# =============================================================================

def evaluate_with_improved_prompt(area="matematica", limit=None, output_dir="results"):
    """Avalia questões usando o prompt melhorado."""
    
    # Configurar API
    client, api_type = setup_api()
    print(f"✅ API configurada (versão: {api_type})")
    
    # Carregar dados
    all_questions = load_enem_data()
    
    # Filtrar por área
    if area == "matematica":
        questions = [q for q in all_questions if q['area'] == 'Matemática']
    else:
        questions = all_questions
    
    if limit:
        questions = questions[:limit]
    
    print(f"📊 Total de questões a avaliar: {len(questions)}")
    print()
    
    # Estatísticas
    results = []
    correct = 0
    total = 0
    
    stats_by_nivel = defaultdict(lambda: {'correct': 0, 'total': 0})
    stats_by_tema = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    # Avaliar cada questão
    for i, q in enumerate(questions, 1):
        q_num = q['numero']
        tri_info = TRI_DATA.get(q_num, {})
        tri = tri_info.get('TRI', 'N/A')
        nivel = tri_info.get('Nivel', 'N/A')
        tema = tri_info.get('Tema', 'N/A')
        habilidade = tri_info.get('H', 'N/A')
        
        print(f"[{i}/{len(questions)}] Questão {q_num} (TRI: {tri}, {nivel})...", end=' ', flush=True)
        
        # Verificar se tem figura
        tem_figura = len(q.get('figures', [])) > 0 or len(q.get('description', [])) > 0
        
        # Construir mensagens
        messages = build_messages(q, use_captions=True, tem_figura=tem_figura)
        
        # Chamar modelo
        response = call_model(client, api_type, messages)
        
        if not response:
            print("❌ Erro na chamada")
            continue
        
        # Extrair resposta
        model_answer = extract_answer(response)
        resposta_correta = q['label'].upper()
        is_correct = model_answer == resposta_correta if model_answer else False
        
        if is_correct:
            correct += 1
            print(f"✅ {model_answer}")
        else:
            print(f"❌ {model_answer} (correto: {resposta_correta})")
        
        total += 1
        
        # Atualizar estatísticas
        stats_by_nivel[nivel]['total'] += 1
        if is_correct:
            stats_by_nivel[nivel]['correct'] += 1
        
        stats_by_tema[tema]['total'] += 1
        if is_correct:
            stats_by_tema[tema]['correct'] += 1
        
        # Salvar resultado
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
            'resposta_completa': response[:500] if response else None,
            'questao_texto': q['question'][:300],
            'tem_figura': tem_figura,
            'tem_descricao': len(q.get('description', [])) > 0
        }
        results.append(result)
        
        # Pequena pausa
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
    
    # Salvar resultados
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"avaliacao_melhorada_{timestamp}.json"
    
    output_data = {
        'config': {
            'area': area,
            'total_questoes': len(questions),
            'prompt_version': 'melhorado_v1',
            'timestamp': timestamp
        },
        'metricas': {
            'accuracy': accuracy,
            'correct': correct,
            'total': total,
            'por_nivel': {k: {'accuracy': v['correct']/v['total'] if v['total'] > 0 else 0, 
                            'correct': v['correct'], 'total': v['total']} 
                         for k, v in stats_by_nivel.items()},
            'por_tema': {k: {'accuracy': v['correct']/v['total'] if v['total'] > 0 else 0,
                            'correct': v['correct'], 'total': v['total']}
                        for k, v in stats_by_tema.items()}
        },
        'resultados': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"💾 Resultados salvos em: {output_file}")
    
    return output_data

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Avaliação ENEM com prompt melhorado")
    parser.add_argument("--area", type=str, default="matematica",
                       choices=["matematica", "todas"],
                       help="Área a avaliar (padrão: matematica)")
    parser.add_argument("--limit", type=int, default=None,
                       help="Limitar número de questões (para teste)")
    parser.add_argument("--output-dir", type=str, default="results",
                       help="Diretório de saída")
    
    args = parser.parse_args()
    
    evaluate_with_improved_prompt(
        area=args.area,
        limit=args.limit,
        output_dir=args.output_dir
    )

