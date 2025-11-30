#!/usr/bin/env python3
"""
Usa API Maritaca (Sabiá-3) para analisar erros e sugerir melhorias no prompt

A Maritaca é especialista em ENEM e pode fornecer insights valiosos.
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def configurar_api_maritaca():
    """Configura conexão com API Maritaca"""
    import openai
    
    api_key = (
        os.environ.get("CURSORMINIMAC") or
        os.environ.get("MARITALK_API_SECRET_KEY") or
        os.environ.get("MARITACA_API_KEY")
    )
    
    if not api_key:
        print("❌ Chave API não configurada!")
        return None, None
    
    openai.api_base = "https://chat.maritaca.ai/api"
    openai_version = openai.__version__
    major_version = int(openai_version.split('.')[0])
    
    if major_version >= 1:
        client = openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")
        return client, 'v1'
    else:
        openai.api_key = api_key
        return openai, 'v0'

def obter_amostra_erros(erros: List[Dict], questoes_completas: Dict, num_amostras: int = 10) -> List[Dict]:
    """Obtém amostra de erros com questões completas"""
    import random
    
    # Carregar questões completas
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    questoes_dict = {}
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    questoes_dict[questao.get('id', '')] = questao
    
    # Amostrar erros
    amostras = random.sample(erros, min(num_amostras, len(erros)))
    
    # Adicionar questão completa a cada erro
    amostras_completas = []
    for erro in amostras:
        questao_id = erro.get('id', '')
        if questao_id in questoes_dict:
            erro_completo = erro.copy()
            erro_completo['questao'] = questoes_dict[questao_id]
            amostras_completas.append(erro_completo)
    
    return amostras_completas

def consultar_maritaca_sobre_erros(client, versao: str, analise_erros: Dict, amostras: List[Dict]) -> str:
    """Consulta Maritaca para análise de erros e sugestões de melhoria"""
    
    # Preparar resumo dos erros
    resumo_erros = f"""
ANÁLISE DE ERROS DO ENEM:

Total de erros: {analise_erros.get('total_erros', 0)}
Total de acertos: {analise_erros.get('total_acertos', 0)}
Acurácia geral: {analise_erros.get('acuracia_geral', 0):.2f}%

Erros por área:
"""
    for area, dados in analise_erros.get('erros_por_area', {}).items():
        resumo_erros += f"  - {area}: {dados.get('erros', 0)} erros, {dados.get('acuracia', 0):.2f}% acurácia\n"
    
    resumo_erros += f"\nPadrões de erro mais comuns:\n"
    for padrao, count in list(analise_erros.get('padroes_erro', {}).items())[:5]:
        resumo_erros += f"  - {padrao}: {count} vezes\n"
    
    # Preparar exemplos de erros
    exemplos = ""
    for i, amostra in enumerate(amostras[:5], 1):
        questao = amostra.get('questao', {})
        exemplos += f"""
EXEMPLO {i}:
Área: {amostra.get('area', 'desconhecida')}
Resposta Correta: {amostra.get('resposta_correta', 'N/A')}
Resposta da IA: {amostra.get('resposta_ia', 'N/A')}

Contexto: {questao.get('context', '')[:200]}...
Pergunta: {questao.get('question', '')[:200]}...
Alternativas:
"""
        for j, alt in enumerate(questao.get('alternatives', [])[:5], 1):
            letra = chr(64 + j)
            exemplos += f"  {letra}. {alt[:100]}...\n"
    
    prompt = f"""Você é um especialista em avaliações educacionais do ENEM (Exame Nacional do Ensino Médio).

Analisei o desempenho de uma IA (você mesma, Sabiá-3) em questões do ENEM e identifiquei os seguintes problemas:

{resumo_erros}

{exemplos}

Com base nessa análise, preciso da sua ajuda como especialista em ENEM para:

1. IDENTIFICAR OS PRINCIPAIS PROBLEMAS:
   - Por que a IA está errando principalmente em matemática (apenas 33.52% de acurácia)?
   - Por que há um padrão de escolher a alternativa B com muita frequência?
   - Quais são as características das questões que a IA mais erra?

2. SUGERIR MELHORIAS NO PROMPT:
   - Como melhorar o prompt para aumentar a acurácia em matemática?
   - Como evitar a tendência de escolher B por padrão?
   - Que instruções específicas devem ser adicionadas?
   - Como estruturar melhor o prompt para questões do ENEM?

3. RECOMENDAÇÕES ESPECÍFICAS:
   - Estratégias para análise de questões de matemática
   - Técnicas para eliminação de alternativas incorretas
   - Como usar melhor os campos semânticos
   - Metodologia de resolução passo a passo

Forneça uma análise detalhada e sugestões práticas e específicas para melhorar o prompt, focando especialmente em:
- Aumentar a acurácia de 73.79% para pelo menos 85-90%
- Resolver o problema de matemática (33.52% → pelo menos 70%)
- Eliminar a tendência de escolher B por padrão

Responda em formato estruturado e detalhado."""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            resposta = response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            resposta = response.choices[0].message.content
        
        return resposta
    except Exception as e:
        print(f"❌ Erro ao consultar Maritaca: {e}")
        return None

def preparar_analise_erros():
    """Prepara análise de erros para consulta"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "analises" / "avaliacao_acuracia_maritaca.json"
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    erros = []
    acertos = []
    erros_por_area = {}
    
    for ano, dados in data.items():
        if ano == '_geral':
            continue
        if isinstance(dados, dict) and 'avaliacoes' in dados:
            for aval in dados['avaliacoes']:
                if not aval.get('acerto', False):
                    erros.append(aval)
                    area = aval.get('area', 'desconhecida')
                    if area not in erros_por_area:
                        erros_por_area[area] = {'erros': 0, 'acertos': 0}
                    erros_por_area[area]['erros'] += 1
                else:
                    acertos.append(aval)
                    area = aval.get('area', 'desconhecida')
                    if area not in erros_por_area:
                        erros_por_area[area] = {'erros': 0, 'acertos': 0}
                    erros_por_area[area]['acertos'] += 1
    
    # Calcular acurácia por área
    for area, dados in erros_por_area.items():
        total = dados['erros'] + dados['acertos']
        dados['acuracia'] = (dados['acertos'] / total * 100) if total > 0 else 0
    
    # Padrões de erro
    padroes_erro = {}
    for erro in erros:
        correta = erro.get('resposta_correta', '')
        ia = erro.get('resposta_ia', '')
        if correta and ia:
            padrao = f"{correta}→{ia}"
            padroes_erro[padrao] = padroes_erro.get(padrao, 0) + 1
    
    geral = data.get('_geral', {})
    
    return {
        'total_erros': len(erros),
        'total_acertos': len(acertos),
        'acuracia_geral': geral.get('acuracia_geral', 0),
        'erros_por_area': erros_por_area,
        'padroes_erro': padroes_erro,
        'erros': erros
    }

def main():
    """Função principal"""
    print("=" * 70)
    print("🤖 ANÁLISE DE ERROS COM MARITACA (ESPECIALISTA ENEM)")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API Maritaca...")
    client, versao = configurar_api_maritaca()
    if not client:
        return
    
    print("✅ API configurada")
    print()
    
    # Preparar análise
    print("📊 Preparando análise de erros...")
    analise_erros = preparar_analise_erros()
    print(f"✅ {analise_erros['total_erros']} erros identificados")
    print()
    
    # Obter amostras
    print("📋 Obtendo amostra de erros...")
    amostras = obter_amostra_erros(analise_erros['erros'], {})
    print(f"✅ {len(amostras)} amostras preparadas")
    print()
    
    # Consultar Maritaca
    print("🤖 Consultando Maritaca (Sabiá-3) para análise e sugestões...")
    print("   Isso pode levar alguns minutos...")
    print()
    
    resposta = consultar_maritaca_sobre_erros(client, versao, analise_erros, amostras)
    
    if resposta:
        # Salvar resposta
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / "data" / "analises"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        arquivo = output_dir / "analise_erros_maritaca.json"
        resultado = {
            'analise_erros': analise_erros,
            'sugestoes_maritaca': resposta,
            'timestamp': time.time()
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print("=" * 70)
        print("✅ ANÁLISE DA MARITACA RECEBIDA")
        print("=" * 70)
        print()
        print("📝 SUGESTÕES DA MARITACA (ESPECIALISTA ENEM):")
        print("=" * 70)
        print(resposta)
        print()
        print("=" * 70)
        print(f"💾 Análise completa salva em: {arquivo}")
        print()
        print("💡 Use essas sugestões para melhorar o prompt em:")
        print("   scripts/analise_enem/21_avaliacao_acuracia_maritaca.py")
    else:
        print("❌ Não foi possível obter análise da Maritaca")

if __name__ == "__main__":
    main()


