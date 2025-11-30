#!/usr/bin/env python3
"""
🚀 Teste Rápido - Todas as Áreas do ENEM 2024

Testa o sistema completo melhorado em todas as áreas:
- Linguagens (01-45)
- Humanas (46-90)
- Natureza (91-135)
- Matemática (136-180)

Uso:
    python 83_teste_rapido_todas_areas.py [--questoes_por_area 5]
"""

import os
import sys
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Carregar .env PRIMEIRO (antes de qualquer import)
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # Se dotenv não estiver instalado, ler manualmente
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

try:
    import openai
except ImportError:
    print("❌ Erro: openai não instalado")
    sys.exit(1)

# Importar módulos
import importlib.util

# Módulos do sistema adaptativo
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

# Few-shots Natureza
natureza_module_path = Path(__file__).parent / "81_fewshots_natureza_expandido.py"
spec5 = importlib.util.spec_from_file_location("fewshots_natureza", natureza_module_path)
natureza_module = importlib.util.module_from_spec(spec5)
spec5.loader.exec_module(natureza_module)

# Prompt Natureza
prompt_natureza_module_path = Path(__file__).parent / "82_prompt_especializado_natureza.py"
spec6 = importlib.util.spec_from_file_location("prompt_natureza", prompt_natureza_module_path)
prompt_natureza_module = importlib.util.module_from_spec(spec6)
spec6.loader.exec_module(prompt_natureza_module)

# Funções importadas
selecionar_prompt_por_tri = prompts_module.selecionar_prompt_por_tri
obter_info_tri = prompts_module.obter_info_tri
classificar_por_tri = prompts_module.classificar_por_tri
criar_prompt_com_fewshots = fewshots_module.criar_prompt_com_fewshots
criar_prompt_com_deteccao_figura = figuras_module.criar_prompt_com_deteccao_figura
obter_info_figura = figuras_module.obter_info_figura
aplicar_prompt_ultra_simples = prompt_simples_module.aplicar_prompt_ultra_simples
obter_fewshots_natureza = natureza_module.obter_fewshots_natureza
criar_prompt_natureza = prompt_natureza_module.criar_prompt_natureza

def configurar_api():
    """Configura API"""
    # Forçar leitura do .env (sobrescreve variáveis de ambiente se necessário)
    env_file = Path(__file__).parent.parent.parent / ".env"
    api_key = None
    
    if env_file.exists():
        # Ler diretamente do arquivo (prioridade)
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key == 'CURSORMINIMAC':
                        api_key = value
                        os.environ[key] = value  # Atualizar também no ambiente
                        break
    
    # Se não encontrou no .env, tentar variável de ambiente
    if not api_key:
        api_key = os.getenv('CURSORMINIMAC') or os.getenv('MARITALK_API_SECRET_KEY')
    
    if not api_key:
        print("❌ Erro: Chave API não encontrada")
        print("   Configure: export CURSORMINIMAC=... ou crie arquivo .env")
        sys.exit(1)
    
    print(f"🔑 Usando chave: ...{api_key[-10:]}")
    return openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")

def carregar_questoes_todas_areas():
    """Carrega questões de todas as áreas do ENEM 2024"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "processed" / "enem_2024_completo.jsonl"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return []
    
    questoes_por_area = {
        'languages': [],      # 01-45
        'human-sciences': [],  # 46-90
        'natural-sciences': [], # 91-135
        'mathematics': []      # 136-180
    }
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                questao = json.loads(line)
                num_str = questao.get('id', '').replace('questao_', '') or questao.get('number', '')
                try:
                    num = int(num_str)
                    area = questao.get('area', '')
                    
                    # Classificar por número
                    if 1 <= num <= 45:
                        area = 'languages'
                    elif 46 <= num <= 90:
                        area = 'human-sciences'
                    elif 91 <= num <= 135:
                        area = 'natural-sciences'
                    elif 136 <= num <= 180:
                        area = 'mathematics'
                    
                    if area in questoes_por_area:
                        questao['number'] = num
                        questao['area'] = area
                        questoes_por_area[area].append(questao)
                except (ValueError, TypeError):
                    continue
    
    return questoes_por_area

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

def construir_prompt_final(questao: dict) -> tuple[str, dict]:
    """Constrói prompt final com todas as melhorias"""
    num = questao.get('number', 0)
    area = questao.get('area', '')
    
    # Obter TRI (pode não existir para todas as áreas)
    tri_info = obter_info_tri(num)
    tri_value = tri_info.get('TRI', 0)
    nivel = classificar_por_tri(tri_value) if tri_value > 0 else 'medio'
    tema = tri_info.get('Tema', 'N/A')
    
    # Selecionar prompt adaptativo
    if tri_value > 0:
        prompt_base = selecionar_prompt_por_tri(tri_value)
    else:
        # Prompt padrão para áreas sem TRI
        prompt_base = "Você é um especialista em questões do ENEM. Resolva a questão abaixo passo-a-passo.\n\n"
    
    # Aplicar prompt ultra-simples se fácil
    if tri_value > 0 and tri_value < 650:
        prompt_com_simples = aplicar_prompt_ultra_simples(prompt_base, questao, tri_value, obter_info_figura)
    else:
        prompt_com_simples = prompt_base
    
    # Adicionar few-shots específicos por área
    if area == 'natural-sciences':
        # Prompt especializado para Natureza
        prompt_com_simples = criar_prompt_natureza(prompt_com_simples)
        # Few-shots de Natureza (se nível médio)
        if nivel == 'medio':
            fewshots_nat = obter_fewshots_natureza(5)
            # Adicionar few-shots manualmente
            for fs in fewshots_nat:
                prompt_com_simples += f"\n\nExemplo:\n{fs['question']}\n{fs['response']}\n"
    elif area == 'mathematics' and nivel == 'medio':
        # Few-shots de Matemática
        prompt_com_fewshots = criar_prompt_com_fewshots(prompt_com_simples, tema, num_fewshots=3)
        prompt_com_simples = prompt_com_fewshots
    else:
        # Manter prompt base
        pass
    
    # Adicionar detecção de figuras
    prompt_final = criar_prompt_com_deteccao_figura(prompt_com_simples, questao)
    
    return prompt_final, {
        'tri': tri_value,
        'nivel': nivel,
        'tema': tema,
        'area': area,
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

def resolver_questao(client, questao: dict, n_passagens: int = 3) -> Dict:
    """Resolve questão com self-consistency (versão rápida: 3 passagens)"""
    respostas = []
    
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
            
            time.sleep(0.2)  # Delay menor para teste rápido
        except Exception as e:
            print(f"      ⚠️  Erro na passagem {i+1}: {str(e)[:50]}")
            continue
    
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
        'info': info
    }

def teste_rapido_todas_areas(questoes_por_area: int = 5, n_passagens: int = 3):
    """Teste rápido em todas as áreas"""
    print("=" * 70)
    print("🚀 TESTE RÁPIDO - TODAS AS ÁREAS")
    print("=" * 70)
    print()
    print("✨ Sistema completo melhorado ativo:")
    print("   1. ✅ Prompts adaptativos por TRI")
    print("   2. ✅ Few-shots customizados")
    print("   3. ✅ Detecção de figuras")
    print("   4. ✅ Self-Consistency ({} passagens)".format(n_passagens))
    print("   5. ✅ Prompt ultra-simples para fáceis")
    print("   6. ✅ Prompt especializado para Natureza")
    print()
    print(f"📊 Configuração: {questoes_por_area} questões por área")
    print()
    
    client = configurar_api()
    questoes_por_area_dict = carregar_questoes_todas_areas()
    
    # Mapear nomes de áreas
    area_names = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    # Estatísticas
    stats_por_area = defaultdict(lambda: {'correct': 0, 'total': 0})
    resultados = []
    total_geral = 0
    correct_geral = 0
    start_time = time.time()
    
    # Testar cada área
    for area_key, area_name in area_names.items():
        questoes = questoes_por_area_dict.get(area_key, [])
        
        if not questoes:
            print(f"⚠️  Nenhuma questão encontrada para {area_name}")
            continue
        
        # Limitar número de questões
        questoes_teste = questoes[:questoes_por_area]
        
        print(f"📚 {area_name} ({len(questoes_teste)} questões)")
        print("-" * 70)
        
        for i, q in enumerate(questoes_teste, 1):
            q_num = q.get('number', 0)
            total_geral += 1
            stats_por_area[area_name]['total'] += 1
            
            print(f"  [{i}/{len(questoes_teste)}] Questão {q_num}", end=" ... ")
            
            # Resolver
            resultado = resolver_questao(client, q, n_passagens=n_passagens)
            resposta_final = resultado['resposta_final']
            confianca = resultado['confianca']
            
            # Comparar
            correct_answer = q.get('label', '')
            is_correct = (resposta_final == correct_answer) if resposta_final else False
            
            if is_correct:
                correct_geral += 1
                stats_por_area[area_name]['correct'] += 1
                print(f"✅ ({resposta_final}, conf: {confianca:.0%})")
            else:
                print(f"❌ ({resposta_final} vs {correct_answer}, conf: {confianca:.0%})")
            
            resultados.append({
                'area': area_name,
                'numero': q_num,
                'resposta': resposta_final,
                'gabarito': correct_answer,
                'correto': is_correct,
                'confianca': confianca
            })
            
            time.sleep(0.3)
        
        print()
    
    elapsed_time = time.time() - start_time
    accuracy_geral = correct_geral / total_geral if total_geral > 0 else 0
    
    # Resultados
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print()
    print(f"🎯 Acurácia Geral: {accuracy_geral:.2%} ({correct_geral}/{total_geral})")
    print(f"⏱️  Tempo: {elapsed_time:.1f}s ({elapsed_time/total_geral:.1f}s por questão)")
    print()
    
    print("📊 Por Área:")
    print("-" * 50)
    for area_name in ['Linguagens', 'Humanas', 'Natureza', 'Matemática']:
        stats = stats_por_area[area_name]
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            print(f"{area_name:<15} {stats['correct']:>3}/{stats['total']:<3} = {acc:>5.1f}%")
    print()
    
    # Comparação
    print("📈 Comparação com Benchmarks:")
    print("-" * 50)
    print(f"BrainX (Teste):     {accuracy_geral:.2%}")
    print(f"BrainX (Atual):     86.59%")
    print(f"GPT-4o (Paper):     93.85%")
    print(f"Gap para GPT-4o:    {93.85 - accuracy_geral*100:+.2f} pontos")
    print()
    
    if accuracy_geral >= 0.94:
        print("🎉 PARABÉNS! BrainX superou GPT-4o!")
    elif accuracy_geral >= 0.90:
        print("✅ Excelente! Muito próximo do GPT-4o!")
    elif accuracy_geral >= 0.87:
        print("✅ Bom resultado! Melhorias funcionando!")
    else:
        print("⚠️  Ainda há espaço para melhorias")
    
    # Salvar
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"teste_rapido_todas_areas_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': total_geral,
            'correct': correct_geral,
            'accuracy': accuracy_geral,
            'questoes_por_area': questoes_por_area,
            'n_passagens': n_passagens,
            'stats_por_area': dict(stats_por_area),
            'resultados': resultados,
            'timestamp': timestamp
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {output_file}")
    print()
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Teste rápido todas as áreas")
    parser.add_argument("--questoes_por_area", type=int, default=5, help="Questões por área (default: 5)")
    parser.add_argument("--passagens", type=int, default=3, help="Número de passagens (default: 3)")
    args = parser.parse_args()
    
    teste_rapido_todas_areas(questoes_por_area=args.questoes_por_area, n_passagens=args.passagens)

