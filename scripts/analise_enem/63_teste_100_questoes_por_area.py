#!/usr/bin/env python3
"""
🧪 Teste com 100 Questões por Área - ENEM
==========================================

Seleciona 100 questões de cada área e avalia usando Maritaca Sabiá-3.

Uso:
    python 63_teste_100_questoes_por_area.py [--anos 2009,2010,2011,...]
"""

import os
import sys
import json
import time
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
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

def call_model(client, api_type, messages, max_retries=3, max_tokens=2000):
    """Chama o modelo com retry."""
    for attempt in range(max_retries):
        try:
            if api_type == "new":
                response = client.chat.completions.create(
                    model="sabia-3",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.1
                )
                return response.choices[0].message.content
            else:
                response = openai.ChatCompletion.create(
                    model="sabia-3",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.1
                )
                return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"⚠️  Erro na tentativa {attempt + 1}/{max_retries}: {e}")
                print(f"   Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
            else:
                print(f"❌ Erro após {max_retries} tentativas: {e}")
                return None
    return None

def formatar_questao(questao: Dict) -> str:
    """Formata questão para o prompt."""
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    
    texto = ""
    if contexto:
        texto += f"CONTEXTO:\n{contexto}\n\n"
    
    texto += f"PERGUNTA:\n{pergunta}\n\n"
    texto += "ALTERNATIVAS:\n"
    
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)  # A, B, C, D, E
        texto += f"{letra}. {alt}\n"
    
    return texto

def avaliar_questao(client, api_type: str, questao: Dict) -> Dict:
    """Avalia uma questão usando Maritaca."""
    questao_formatada = formatar_questao(questao)
    
    prompt_completo = f"{PROMPT_COT_IMPROVED}\n\n{questao_formatada}"
    
    messages = [
        {"role": "system", "content": "Você é um especialista em resolução de questões do ENEM."},
        {"role": "user", "content": prompt_completo}
    ]
    
    resposta_correta = questao.get('label', '').upper().strip()
    
    inicio = time.time()
    resposta_modelo = call_model(client, api_type, messages, max_tokens=2000)
    tempo_resposta = time.time() - inicio
    
    resposta_extraida = extract_answer(resposta_modelo) if resposta_modelo else None
    acertou = resposta_extraida == resposta_correta if resposta_extraida else False
    
    return {
        'questao_id': questao.get('id', 'N/A'),
        'ano': questao.get('exam', 'N/A'),
        'area': questao.get('area', 'N/A'),
        'resposta_correta': resposta_correta,
        'resposta_modelo': resposta_extraida,
        'resposta_completa': resposta_modelo[:500] if resposta_modelo else None,
        'acertou': acertou,
        'tempo_resposta': tempo_resposta
    }

def carregar_questoes_por_area(processed_dir: Path, anos: Optional[List[int]] = None) -> Dict[str, List[Dict]]:
    """Carrega questões agrupadas por área."""
    questoes_por_area = defaultdict(list)
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        
        if anos and ano not in anos:
            continue
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    area = questao.get('area', 'desconhecida')
                    # Filtrar questões anuladas
                    if questao.get('label', '').upper() != 'ANULADO':
                        questoes_por_area[area].append(questao)
    
    return questoes_por_area

def selecionar_questoes_balanceadas(questoes: List[Dict], num_questoes: int = 100) -> List[Dict]:
    """Seleciona questões balanceadas por ano."""
    if len(questoes) <= num_questoes:
        return questoes
    
    # Agrupar por ano
    questoes_por_ano = defaultdict(list)
    for questao in questoes:
        ano = questao.get('exam', 'desconhecido')
        questoes_por_ano[ano].append(questao)
    
    # Selecionar proporcionalmente de cada ano
    anos = sorted(questoes_por_ano.keys())
    questoes_selecionadas = []
    
    # Calcular quantas questões por ano
    questoes_por_ano_count = {ano: len(questoes_por_ano[ano]) for ano in anos}
    total_questoes = sum(questoes_por_ano_count.values())
    
    for ano in anos:
        proporcao = questoes_por_ano_count[ano] / total_questoes
        num_do_ano = max(1, int(num_questoes * proporcao))
        questoes_ano = questoes_por_ano[ano]
        
        if len(questoes_ano) <= num_do_ano:
            questoes_selecionadas.extend(questoes_ano)
        else:
            questoes_selecionadas.extend(random.sample(questoes_ano, num_do_ano))
    
    # Se ainda faltar, completar aleatoriamente
    if len(questoes_selecionadas) < num_questoes:
        questoes_restantes = [q for q in questoes if q not in questoes_selecionadas]
        num_faltando = num_questoes - len(questoes_selecionadas)
        if questoes_restantes:
            questoes_selecionadas.extend(random.sample(questoes_restantes, 
                                                      min(num_faltando, len(questoes_restantes))))
    
    # Se sobrou, reduzir aleatoriamente
    if len(questoes_selecionadas) > num_questoes:
        questoes_selecionadas = random.sample(questoes_selecionadas, num_questoes)
    
    return questoes_selecionadas

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Teste com 100 questões por área')
    parser.add_argument('--anos', type=str, help='Anos a incluir (ex: 2009,2010,2011)')
    parser.add_argument('--num-questoes', type=int, default=100, help='Número de questões por área (padrão: 100)')
    parser.add_argument('--areas', type=str, help='Áreas a testar (ex: languages,human-sciences)')
    args = parser.parse_args()
    
    # Processar argumentos
    anos = None
    if args.anos:
        anos = [int(a.strip()) for a in args.anos.split(',')]
    
    areas_filtro = None
    if args.areas:
        areas_filtro = [a.strip() for a in args.areas.split(',')]
    
    print("=" * 70)
    print("🧪 TESTE COM QUESTÕES POR ÁREA - ENEM")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    client, api_type = setup_api()
    print(f"✅ API configurada (tipo: {api_type})")
    print()
    
    # Carregar questões
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    print("📥 Carregando questões...")
    questoes_por_area = carregar_questoes_por_area(processed_dir, anos)
    
    # Mapear áreas
    areas_map = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    print(f"✅ Questões carregadas:")
    for area_codigo, area_nome in areas_map.items():
        if area_codigo in questoes_por_area:
            print(f"   {area_nome}: {len(questoes_por_area[area_codigo])} questões")
    print()
    
    # Selecionar questões
    print(f"🎯 Selecionando {args.num_questoes} questões por área...")
    questoes_selecionadas = {}
    
    for area_codigo, area_nome in areas_map.items():
        if area_codigo not in questoes_por_area:
            continue
        
        if areas_filtro and area_codigo not in areas_filtro:
            continue
        
        questoes_area = questoes_por_area[area_codigo]
        selecionadas = selecionar_questoes_balanceadas(questoes_area, args.num_questoes)
        questoes_selecionadas[area_codigo] = selecionadas
        print(f"   {area_nome}: {len(selecionadas)} questões selecionadas")
    print()
    
    # Avaliar questões
    resultados_por_area = {}
    tempo_total_inicio = time.time()
    
    for area_codigo, questoes in questoes_selecionadas.items():
        area_nome = areas_map[area_codigo]
        print(f"📊 Avaliando {area_nome} ({len(questoes)} questões)...")
        print("-" * 70)
        
        resultados_area = []
        acertos = 0
        
        for i, questao in enumerate(questoes, 1):
            print(f"   [{i}/{len(questoes)}] {questao.get('id', 'N/A')}...", end=' ', flush=True)
            
            resultado = avaliar_questao(client, api_type, questao)
            resultados_area.append(resultado)
            
            if resultado['acertou']:
                acertos += 1
                print(f"✅ {resultado['resposta_modelo']}")
            else:
                print(f"❌ {resultado['resposta_modelo']} (correta: {resultado['resposta_correta']})")
            
            # Pequena pausa para não sobrecarregar API
            time.sleep(0.5)
        
        acuracia = (acertos / len(questoes)) * 100 if questoes else 0
        resultados_por_area[area_codigo] = {
            'area': area_nome,
            'total': len(questoes),
            'acertos': acertos,
            'erros': len(questoes) - acertos,
            'acuracia': acuracia,
            'resultados': resultados_area
        }
        
        print(f"\n   ✅ {area_nome}: {acertos}/{len(questoes)} ({acuracia:.2f}%)")
        print()
    
    tempo_total = time.time() - tempo_total_inicio
    
    # Gerar relatório
    print("=" * 70)
    print("📊 RELATÓRIO FINAL")
    print("=" * 70)
    print()
    
    total_questoes = sum(r['total'] for r in resultados_por_area.values())
    total_acertos = sum(r['acertos'] for r in resultados_por_area.values())
    acuracia_geral = (total_acertos / total_questoes * 100) if total_questoes > 0 else 0
    
    print(f"📈 Resumo Geral:")
    print(f"   Total de questões: {total_questoes}")
    print(f"   Total de acertos: {total_acertos}")
    print(f"   Acurácia geral: {acuracia_geral:.2f}%")
    print(f"   Tempo total: {tempo_total/60:.2f} minutos")
    print()
    
    print(f"📋 Por Área:")
    for area_codigo, resultado in resultados_por_area.items():
        print(f"   {resultado['area']}:")
        print(f"      Acurácia: {resultado['acuracia']:.2f}% ({resultado['acertos']}/{resultado['total']})")
    
    # Salvar resultados
    output_dir = project_root / "reports" / "avaliacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_resultados = output_dir / f"teste_100_questoes_{timestamp}.json"
    
    relatorio = {
        'timestamp': timestamp,
        'configuracao': {
            'num_questoes_por_area': args.num_questoes,
            'anos': anos,
            'areas': list(questoes_selecionadas.keys())
        },
        'resumo': {
            'total_questoes': total_questoes,
            'total_acertos': total_acertos,
            'acuracia_geral': acuracia_geral,
            'tempo_total_minutos': tempo_total / 60
        },
        'resultados_por_area': resultados_por_area
    }
    
    with open(arquivo_resultados, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2, default=str)
    
    print()
    print(f"💾 Resultados salvos em: {arquivo_resultados}")
    print()
    print("=" * 70)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    main()

