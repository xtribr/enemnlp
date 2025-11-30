#!/usr/bin/env python3
"""
🧪 TESTE LOCAL - PROMPTS REVISADOS COM CORREÇÕES ANTI-VIÉS

Testa os prompts revisados localmente para validar as correções do viés para E.

Uso:
    python 98_teste_prompts_revisados_local.py [--area natureza] [--limit 45]
"""

import os
import sys
import json
import time
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Carregar .env PRIMEIRO
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

try:
    import openai
except ImportError:
    print("❌ Erro: openai não instalado")
    print("   Execute: pip install openai")
    sys.exit(1)

# Importar módulos
import importlib.util

# PROMPTS REVISADOS (com correções anti-viés)
prompts_revisados_path = Path(__file__).parent / "96_prompts_revisados_todas_areas.py"
spec = importlib.util.spec_from_file_location("prompts_revisados", prompts_revisados_path)
prompts_revisados_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompts_revisados_module)

obter_prompt_por_area = prompts_revisados_module.obter_prompt_por_area

# Módulos auxiliares
prompts_module_path = Path(__file__).parent / "70_prompts_adaptativos_por_tri.py"
spec2 = importlib.util.spec_from_file_location("prompts_adaptativos", prompts_module_path)
prompts_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(prompts_module)

figuras_module_path = Path(__file__).parent / "75_deteccao_figuras_simples.py"
spec3 = importlib.util.spec_from_file_location("deteccao_figuras", figuras_module_path)
figuras_module = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(figuras_module)

def configurar_api():
    """Configura API"""
    api_key = os.getenv('CURSORMINIMAC') or os.getenv('MARITALK_API_SECRET_KEY')
    if not api_key:
        raise ValueError("Chave API não configurada! Configure CURSORMINIMAC no .env")
    
    return openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")

def carregar_questoes_por_area(area: str, limit: Optional[int] = None):
    """Carrega questões de uma área específica"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "processed" / "enem_2024_completo.jsonl"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return []
    
    questoes = []
    area_map = {
        'languages': (1, 45),
        'human-sciences': (46, 90),
        'natural-sciences': (91, 135),
        'mathematics': (136, 180)
    }
    
    inicio, fim = area_map.get(area, (1, 180))
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questao = json.loads(line)
                num_str = questao.get('id', '').replace('questao_', '') or questao.get('number', '')
                try:
                    num = int(num_str)
                    if inicio <= num <= fim:
                        questao['number'] = num
                        questao['area'] = area
                        questoes.append(questao)
                        if limit and len(questoes) >= limit:
                            break
                except (ValueError, TypeError):
                    continue
    
    return questoes

def extrair_resposta(texto: str) -> Optional[str]:
    """Extrai resposta do modelo - versão melhorada"""
    if not texto:
        return None
    
    import re
    texto_upper = texto.upper().strip()
    
    # Padrões explícitos (prioridade alta)
    padroes_explicitos = [
        r'RESPOSTA:\s*([A-E])',
        r'ALTERNATIVA\s*([A-E])',
        r'GABARITO:\s*([A-E])',
        r'A\s*RESPOSTA\s*É\s*([A-E])',
        r'RESPOSTA\s*CORRETA:\s*([A-E])',
        r'LETRA\s*([A-E])',
    ]
    
    for padrao in padroes_explicitos:
        match = re.search(padrao, texto_upper)
        if match:
            letra = match.group(1)
            if letra in ['A', 'B', 'C', 'D', 'E']:
                return letra
    
    # Procurar por padrões no final do texto
    padroes_finais = re.findall(r'\b([A-E])\s*[\)\.:]?\s*$', texto_upper[-200:])
    if padroes_finais:
        letra = padroes_finais[-1]
        if letra in ['A', 'B', 'C', 'D', 'E']:
            return letra
    
    # Procurar por letras isoladas nas últimas palavras
    palavras_finais = texto_upper.split()[-10:]
    for palavra in reversed(palavras_finais):
        palavra_limpa = palavra.strip('.,:;!?()[]{}')
        if palavra_limpa in ['A', 'B', 'C', 'D', 'E']:
            return palavra_limpa
    
    return None

def formatar_questao(questao: Dict) -> str:
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

def resolver_questao(client, questao: Dict, n_passagens: int = 3):
    """Resolve questão com self-consistency"""
    area = questao.get('area', '')
    num = questao.get('number', 0)
    
    # Obter TRI
    tri_info = prompts_module.obter_info_tri(num)
    tri_value = tri_info.get('TRI', 0)
    
    # Usar prompt revisado
    prompt_base = obter_prompt_por_area(area, tri_value)
    
    # Detecção de figuras
    prompt_final = figuras_module.criar_prompt_com_deteccao_figura(prompt_base, questao)
    
    questao_formatada = formatar_questao(questao)
    prompt_completo = prompt_final + questao_formatada
    
    respostas = []
    
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
            
            time.sleep(0.2)  # Delay entre passagens
        except Exception as e:
            print(f"      ⚠️  Erro passagem {i+1}: {str(e)[:50]}")
            continue
    
    if not respostas:
        return None, 0.0
    
    # Votação majoritária
    contador = Counter(respostas)
    resposta_mais_frequente = contador.most_common(1)[0]
    resposta_final = resposta_mais_frequente[0]
    frequencia = resposta_mais_frequente[1]
    confianca = frequencia / len(respostas)
    
    return resposta_final, confianca

def main():
    parser = argparse.ArgumentParser(description='Teste local com prompts revisados')
    parser.add_argument('--area', type=str, default='natural-sciences',
                       choices=['languages', 'human-sciences', 'natural-sciences', 'mathematics'],
                       help='Área a testar')
    parser.add_argument('--limit', type=int, default=45,
                       help='Número máximo de questões')
    parser.add_argument('--passagens', type=int, default=3,
                       help='Número de passagens para self-consistency')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🧪 TESTE LOCAL - PROMPTS REVISADOS (CORREÇÕES ANTI-VIÉS)")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    try:
        client = configurar_api()
        print("✅ API configurada")
    except Exception as e:
        print(f"❌ Erro ao configurar API: {e}")
        sys.exit(1)
    
    # Carregar questões
    print(f"\n📥 Carregando questões de {args.area}...")
    questoes = carregar_questoes_por_area(args.area, args.limit)
    
    if not questoes:
        print("❌ Nenhuma questão encontrada")
        sys.exit(1)
    
    print(f"✅ {len(questoes)} questões carregadas")
    
    # Executar avaliação
    print(f"\n🚀 Iniciando avaliação...")
    print(f"   Área: {args.area}")
    print(f"   Questões: {len(questoes)}")
    print(f"   Passagens: {args.passagens}")
    print()
    
    resultados = []
    stats = {'correct': 0, 'total': 0}
    respostas_preditas = Counter()
    respostas_corretas = Counter()
    
    start_time = time.time()
    
    for i, questao in enumerate(questoes, 1):
        num = questao.get('number', 0)
        print(f"Q{num}: ", end='', flush=True)
        
        resposta_final, confianca = resolver_questao(client, questao, args.passagens)
        
        # Normalizar gabarito
        gabarito_raw = questao.get('label', '') or questao.get('answer', '') or questao.get('gabarito', '')
        gabarito = str(gabarito_raw).upper().strip()
        
        if gabarito not in ['A', 'B', 'C', 'D', 'E']:
            print(f"⚠️  Gabarito inválido: '{gabarito_raw}'")
            continue
        
        # Comparar
        is_correct = (resposta_final == gabarito) if resposta_final else False
        
        if is_correct:
            stats['correct'] += 1
            print(f"✅ ({resposta_final}, conf: {confianca:.0%})")
        else:
            print(f"❌ ({resposta_final} vs {gabarito}, conf: {confianca:.0%})")
        
        stats['total'] += 1
        respostas_preditas[resposta_final] += 1
        respostas_corretas[gabarito] += 1
        
        resultados.append({
            'numero': num,
            'resposta': resposta_final,
            'gabarito': gabarito,
            'correto': is_correct,
            'confianca': confianca
        })
        
        time.sleep(0.5)  # Delay entre questões
    
    elapsed = time.time() - start_time
    
    # Estatísticas finais
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    
    acuracia = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
    print(f"🎯 Acurácia: {acuracia:.2f}% ({stats['correct']}/{stats['total']})")
    print(f"⏱️  Tempo: {elapsed:.1f}s ({elapsed/stats['total']:.1f}s por questão)")
    print()
    
    print("📊 DISTRIBUIÇÃO DE RESPOSTAS:")
    print()
    print("   Preditas pelo modelo:")
    for letra in ['A', 'B', 'C', 'D', 'E']:
        count = respostas_preditas.get(letra, 0)
        pct = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"      {letra}: {count:2d} vezes ({pct:5.1f}%)")
    print()
    print("   Corretas (gabarito):")
    for letra in ['A', 'B', 'C', 'D', 'E']:
        count = respostas_corretas.get(letra, 0)
        pct = (count / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"      {letra}: {count:2d} vezes ({pct:5.1f}%)")
    print()
    
    # Verificar viés
    count_e_predita = respostas_preditas.get('E', 0)
    count_e_correta = respostas_corretas.get('E', 0)
    pct_e_predita = (count_e_predita / stats['total']) * 100 if stats['total'] > 0 else 0
    pct_e_correta = (count_e_correta / stats['total']) * 100 if stats['total'] > 0 else 0
    
    if count_e_predita > count_e_correta * 1.5:
        print(f"⚠️  VIÉS DETECTADO: Modelo escolheu E {count_e_predita} vezes ({pct_e_predita:.1f}%)")
        print(f"   Respostas corretas E: {count_e_correta} vezes ({pct_e_correta:.1f}%)")
        print(f"   Razão: {count_e_predita/count_e_correta:.1f}x mais que o esperado")
    else:
        print("✅ Sem viés significativo para E")
    print()
    
    # Salvar resultados
    output_file = Path(__file__).parent.parent.parent / "results" / f"teste_prompts_revisados_{args.area}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        'area': args.area,
        'total': stats['total'],
        'correct': stats['correct'],
        'accuracy': acuracia / 100,
        'tempo_total': elapsed,
        'tempo_por_questao': elapsed / stats['total'] if stats['total'] > 0 else 0,
        'distribuicao_predita': dict(respostas_preditas),
        'distribuicao_correta': dict(respostas_corretas),
        'resultados': resultados,
        'timestamp': datetime.now().isoformat()
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    main()

