#!/usr/bin/env python3
"""
Sistema Completo usando 100% Maritaca Sabiá 3

Implementa:
1. Embeddings semânticos via Maritaca
2. Análise semântica profunda
3. Few-shot learning com questões similares
4. Sistema adaptativo de treinamento
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time
import numpy as np
from collections import defaultdict

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

def gerar_embedding_maritaca(client, versao: str, texto: str) -> Optional[List[float]]:
    """Gera embedding semântico usando Maritaca"""
    prompt = f"""Você é a Maritaca Sabiá 3. 

Analise o seguinte texto de uma questão do ENEM e forneça uma representação semântica estruturada:

TEXTO:
{texto}

Forneça uma análise semântica detalhada incluindo:
1. Conceitos-chave principais
2. Contexto e domínio
3. Tipo de problema/questão
4. Complexidade estimada
5. Palavras-chave importantes

Formate como JSON com essas chaves."""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.1
            )
            resposta = response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.1
            )
            resposta = response.choices[0].message.content
        
        # Extrair JSON da resposta
        import re
        json_match = re.search(r'\{.*\}', resposta, re.DOTALL)
        if json_match:
            analise = json.loads(json_match.group())
            # Converter análise em vetor (simplificado - pode ser melhorado)
            # Por enquanto, retornamos a análise estruturada
            return analise
        
        return None
    except Exception as e:
        print(f"⚠️  Erro ao gerar embedding: {e}")
        return None

def analise_semantica_profunda_maritaca(client, versao: str, questao: Dict) -> Optional[Dict]:
    """Análise semântica profunda da questão usando Maritaca"""
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    area = questao.get('area', 'desconhecida')
    
    texto_completo = f"{contexto}\n\n{pergunta}"
    
    prompt = f"""Você é a Maritaca Sabiá 3, especialista em ENEM.

Realize uma ANÁLISE SEMÂNTICA PROFUNDA da seguinte questão do ENEM:

ÁREA: {area}

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)
        prompt += f"{letra}. {alt}\n"
    
    prompt += """
ANÁLISE REQUERIDA:
1. Identifique os CONCEITOS-CHAVE principais necessários para resolver
2. Identifique o TIPO DE PROBLEMA (cálculo, interpretação, aplicação, etc.)
3. Identifique ARMADILHAS COMUNS que podem levar a erros
4. Identifique o NÍVEL DE DIFICULDADE (fácil, médio, difícil)
5. Identifique CONHECIMENTOS PRÉVIOS necessários
6. Analise cada alternativa e identifique por que cada uma pode ser correta ou incorreta
7. Forneça uma ESTRATÉGIA DE RESOLUÇÃO passo a passo

Formate como JSON estruturado."""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.2
            )
            resposta = response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.2
            )
            resposta = response.choices[0].message.content
        
        # Extrair JSON
        import re
        json_match = re.search(r'\{.*\}', resposta, re.DOTALL)
        if json_match:
            analise = json.loads(json_match.group())
            return analise
        
        # Se não conseguir extrair JSON, retornar texto
        return {'analise_texto': resposta}
    except Exception as e:
        print(f"⚠️  Erro na análise semântica: {e}")
        return None

def encontrar_questoes_similares_maritaca(client, versao: str, questao_atual: Dict, 
                                          banco_questoes: List[Dict], num_similares: int = 3) -> List[Dict]:
    """Encontra questões similares usando análise semântica da Maritaca"""
    print(f"  🔍 Buscando {num_similares} questões similares...")
    
    # Análise semântica da questão atual
    analise_atual = analise_semantica_profunda_maritaca(client, versao, questao_atual)
    if not analise_atual:
        return []
    
    # Extrair conceitos-chave da questão atual
    conceitos_atual = analise_atual.get('conceitos_chave', [])
    if isinstance(conceitos_atual, str):
        conceitos_atual = [conceitos_atual]
    
    # Comparar com outras questões
    questoes_com_similaridade = []
    
    for questao in banco_questoes[:50]:  # Limitar busca para performance
        if questao.get('id') == questao_atual.get('id'):
            continue
        
        # Análise rápida de similaridade (pode ser otimizado)
        contexto_outra = questao.get('context', '').strip()
        pergunta_outra = questao.get('question', '').strip()
        texto_outra = f"{contexto_outra} {pergunta_outra}"
        
        # Verificar similaridade básica (mesma área, conceitos similares)
        if questao.get('area') == questao_atual.get('area'):
            # Contar palavras-chave em comum
            palavras_comuns = sum(1 for conceito in conceitos_atual 
                                if conceito.lower() in texto_outra.lower())
            
            if palavras_comuns > 0:
                questoes_com_similaridade.append({
                    'questao': questao,
                    'similaridade': palavras_comuns,
                    'resposta_correta': questao.get('label', '')
                })
    
    # Ordenar por similaridade e retornar top N
    questoes_com_similaridade.sort(key=lambda x: x['similaridade'], reverse=True)
    
    return [item['questao'] for item in questoes_com_similaridade[:num_similares]]

def criar_prompt_few_shot_maritaca(client, versao: str, questao: Dict, 
                                    questoes_similares: List[Dict]) -> str:
    """Cria prompt com few-shot learning usando questões similares"""
    
    # Análise semântica profunda da questão atual
    analise = analise_semantica_profunda_maritaca(client, versao, questao)
    
    prompt = """Você é a Maritaca Sabiá 3, especialista em ENEM.

Vou apresentar algumas questões similares já resolvidas corretamente, e depois a questão que você deve resolver.

"""
    
    # Adicionar exemplos similares (few-shot)
    for i, questao_similar in enumerate(questoes_similares, 1):
        contexto_sim = questao_similar.get('context', '').strip()
        pergunta_sim = questao_similar.get('question', '').strip()
        alternativas_sim = questao_similar.get('alternatives', [])
        resposta_sim = questao_similar.get('label', '').upper()
        
        prompt += f"""EXEMPLO {i} (Questão Similar Resolvida):

CONTEXTO:
{contexto_sim}

PERGUNTA:
{pergunta_sim}

ALTERNATIVAS:
"""
        for j, alt in enumerate(alternativas_sim, 1):
            letra = chr(64 + j)
            prompt += f"{letra}. {alt}\n"
        
        prompt += f"RESPOSTA CORRETA: {resposta_sim}\n\n"
    
    # Adicionar análise semântica
    if analise:
        prompt += f"""ANÁLISE SEMÂNTICA DA QUESTÃO ATUAL:
{json.dumps(analise, indent=2, ensure_ascii=False)}

"""
    
    # Adicionar questão atual
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    
    prompt += f"""QUESTÃO A RESOLVER:

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)
        prompt += f"{letra}. {alt}\n"
    
    prompt += """
INSTRUÇÕES:
1. Use os exemplos similares como referência
2. Aplique a análise semântica fornecida
3. Siga a mesma metodologia dos exemplos
4. Resolva passo a passo
5. Responda APENAS com a letra (A, B, C, D ou E)"""
    
    return prompt

def avaliar_questao_com_sistema_completo(client, versao: str, questao: Dict, 
                                          banco_questoes: List[Dict]) -> Dict:
    """Avalia questão usando sistema completo 100% Maritaca"""
    
    # 1. Encontrar questões similares
    questoes_similares = encontrar_questoes_similares_maritaca(
        client, versao, questao, banco_questoes, num_similares=3
    )
    
    # 2. Criar prompt com few-shot learning
    if questoes_similares:
        prompt = criar_prompt_few_shot_maritaca(client, versao, questao, questoes_similares)
    else:
        # Fallback: análise semântica profunda sem exemplos
        analise = analise_semantica_profunda_maritaca(client, versao, questao)
        # Criar prompt básico com análise
        contexto = questao.get('context', '').strip()
        pergunta = questao.get('question', '').strip()
        alternativas = questao.get('alternatives', [])
        
        prompt = f"""Você é a Maritaca Sabiá 3, especialista em ENEM.

ANÁLISE SEMÂNTICA:
{json.dumps(analise, indent=2, ensure_ascii=False) if analise else 'N/A'}

QUESTÃO:

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
        for i, alt in enumerate(alternativas, 1):
            letra = chr(64 + i)
            prompt += f"{letra}. {alt}\n"
        
        prompt += "\nResolva passo a passo e responda APENAS com a letra (A, B, C, D ou E)."
    
    # 3. Avaliar questão
    resposta_correta = questao.get('label', '').upper().strip()
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        
        # Extrair letra
        import re
        match = re.search(r'\b([A-E])\b', resposta_ia)
        resposta_ia = match.group(1) if match else None
        
        acerto = resposta_ia == resposta_correta if resposta_ia else False
        
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': resposta_ia,
            'acerto': acerto,
            'usou_few_shot': len(questoes_similares) > 0,
            'num_exemplos': len(questoes_similares)
        }
    except Exception as e:
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': None,
            'acerto': False,
            'erro': str(e)
        }

def main():
    """Teste do sistema completo"""
    print("=" * 70)
    print("🚀 SISTEMA COMPLETO 100% MARITACA")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API...")
    client, versao = configurar_api_maritaca()
    if not client:
        print("❌ API não configurada")
        return
    
    print("✅ API configurada")
    print()
    
    # Carregar questões
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    print("📥 Carregando questões...")
    banco_questoes = []
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if questao.get('area') == 'mathematics':
                        banco_questoes.append(questao)
    
    print(f"✅ {len(banco_questoes)} questões de matemática carregadas")
    print()
    
    # Testar com algumas questões
    print("🧪 Testando sistema completo...")
    print("   (Isso pode demorar - cada questão faz múltiplas consultas à Maritaca)")
    print()
    
    import random
    questoes_teste = random.sample(banco_questoes, min(10, len(banco_questoes)))
    
    resultados = []
    for i, questao in enumerate(questoes_teste, 1):
        print(f"  [{i}/{len(questoes_teste)}] {questao.get('id', '')[:40]}...", end=' ', flush=True)
        
        resultado = avaliar_questao_com_sistema_completo(client, versao, questao, banco_questoes)
        resultados.append(resultado)
        
        if resultado.get('acerto'):
            print("✅")
        else:
            print(f"❌ (IA: {resultado.get('resposta_ia', 'N/A')}, Correta: {resultado.get('resposta_correta', 'N/A')})")
        
        time.sleep(1)  # Rate limiting
    
    # Resultados
    acertos = sum(1 for r in resultados if r.get('acerto'))
    acuracia = (acertos / len(resultados) * 100) if resultados else 0
    
    print()
    print("=" * 70)
    print("📊 RESULTADOS")
    print("=" * 70)
    print(f"Total: {len(resultados)} questões")
    print(f"Acertos: {acertos}")
    print(f"Acurácia: {acuracia:.2f}%")
    print()
    
    # Salvar
    arquivo = project_root / "data" / "analises" / "sistema_completo_maritaca.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump({
            'resultados': resultados,
            'total': len(resultados),
            'acertos': acertos,
            'acuracia': acuracia,
            'sistema': '100%_maritaca_completo'
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {arquivo}")

if __name__ == "__main__":
    main()

