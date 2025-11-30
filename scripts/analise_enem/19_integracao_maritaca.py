#!/usr/bin/env python3
"""
Integração com API Maritaca para Análise de Complexidade Semântica

Usa a API Maritaca (Sabiá-3) para análise avançada de complexidade semântica.
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
        print("   Configure: CURSORMINIMAC, MARITALK_API_SECRET_KEY ou MARITACA_API_KEY")
        return None, None
    
    openai.api_base = "https://chat.maritaca.ai/api"
    
    # Detectar versão do openai
    openai_version = openai.__version__
    major_version = int(openai_version.split('.')[0])
    
    if major_version >= 1:
        client = openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")
        return client, 'v1'
    else:
        openai.api_key = api_key
        return openai, 'v0'

def analisar_complexidade_semantica(client, texto: str, versao: str) -> Dict:
    """Analisa complexidade semântica usando API Maritaca"""
    prompt = f"""Analise a complexidade semântica do seguinte texto de questão do ENEM.

Texto:
{texto}

Forneça uma análise em formato JSON com:
- nivel_complexidade: "muito_facil", "facil", "medio", "dificil" ou "muito_dificil"
- score_complexidade: número de 0 a 100
- conceitos_principais: lista de 3-5 conceitos principais
- justificativa: breve explicação

Responda APENAS com o JSON, sem texto adicional."""

    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            resposta = response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            resposta = response.choices[0].message.content
        
        # Tentar extrair JSON da resposta
        try:
            # Remover markdown code blocks se houver
            resposta = resposta.strip()
            if resposta.startswith('```'):
                resposta = resposta.split('```')[1]
                if resposta.startswith('json'):
                    resposta = resposta[4:]
            resposta = resposta.strip()
            
            analise = json.loads(resposta)
            return analise
        except json.JSONDecodeError:
            # Se não conseguir parsear, retornar estrutura básica
            return {
                'nivel_complexidade': 'medio',
                'score_complexidade': 50,
                'conceitos_principais': [],
                'justificativa': 'Análise não disponível',
                'resposta_raw': resposta
            }
    
    except Exception as e:
        print(f"    ⚠️  Erro na análise: {e}")
        return None

def processar_questoes_com_maritaca(dados: Dict[int, List[Dict]], 
                                   limite: int = None,
                                   amostra_por_ano: int = None) -> Dict:
    """Processa questões usando API Maritaca"""
    client, versao = configurar_api_maritaca()
    
    if not client:
        return {}
    
    print("🤖 Usando API Maritaca (Sabiá-3) para análise de complexidade semântica")
    print()
    
    resultados = {}
    total_processadas = 0
    
    for ano in sorted(dados.keys()):
        questoes = dados[ano]
        
        # Amostrar questões se especificado (None = todas)
        if amostra_por_ano is not None and len(questoes) > amostra_por_ano:
            import random
            questoes = random.sample(questoes, amostra_por_ano)
        
        print(f"📊 Processando {ano} ({len(questoes)} questões)...")
        
        analises_ano = []
        for i, questao in enumerate(questoes, 1):
            contexto = questao.get('context', '')
            pergunta = questao.get('question', '')
            texto = f"{contexto} {pergunta}".strip()
            
            if not texto:
                continue
            
            print(f"  [{i}/{len(questoes)}] Analisando questão {questao.get('id', '')}...", end=' ')
            
            analise = analisar_complexidade_semantica(client, texto, versao)
            
            if analise:
                analise['id'] = questao.get('id', '')
                analise['area'] = questao.get('area', 'desconhecida')
                analises_ano.append(analise)
                print("✅")
            else:
                print("❌")
            
            # Rate limiting
            time.sleep(0.5)  # Evitar rate limit
            
            total_processadas += 1
            if limite and total_processadas >= limite:
                print(f"\n⚠️  Limite de {limite} questões atingido")
                break
        
        if analises_ano:
            resultados[ano] = {
                'analises': analises_ano,
                'estatisticas': {
                    'total_analisadas': len(analises_ano),
                    'media_score': sum(a.get('score_complexidade', 50) for a in analises_ano) / len(analises_ano)
                }
            }
        
        print()
        
        if limite and total_processadas >= limite:
            break
    
    return resultados

def salvar_resultados(resultados: Dict, output_dir: Path):
    """Salva resultados da análise com Maritaca"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "analise_complexidade_maritaca.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {arquivo}")

def main():
    """Função principal"""
    print("=" * 70)
    print("🤖 ANÁLISE DE COMPLEXIDADE SEMÂNTICA - API MARITACA")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    analises_dir = project_root / "data" / "analises"
    
    # Carregar dados
    print("📥 Carregando dados...")
    # Usar função local ao invés de import
    dados = {}
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        dados[ano] = questoes
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # Processar com API Maritaca
    # ✅ API com uso ilimitado - processar TODAS as questões
    print("✅ Processando TODAS as questões (API ilimitada)")
    print(f"   - {len(dados)} anos disponíveis")
    print(f"   - Total de questões: {sum(len(q) for q in dados.values())}")
    print()
    
    resultados = processar_questoes_com_maritaca(
        dados,
        amostra_por_ano=None,  # Todas as questões por ano
        limite=None  # Sem limite
    )
    
    if resultados:
        salvar_resultados(resultados, analises_dir)
        
        # Estatísticas
        print()
        print("=" * 70)
        print("📊 ESTATÍSTICAS DA ANÁLISE")
        print("=" * 70)
        
        for ano, dados_ano in resultados.items():
            stats = dados_ano['estatisticas']
            print(f"\n{ano}:")
            print(f"  Questões analisadas: {stats['total_analisadas']}")
            print(f"  Score médio: {stats['media_score']:.2f}")
    
    print()
    print("=" * 70)
    print("✅ ANÁLISE COM API MARITACA CONCLUÍDA")
    print("=" * 70)
    print("\n💡 Para análise completa, execute novamente com mais questões")
    print("   (monitore uso de créditos da API)")

if __name__ == "__main__":
    main()

