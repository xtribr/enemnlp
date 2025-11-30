#!/usr/bin/env python3
"""
Sistema de Treinamento Completo usando 100% Maritaca

Consulta a Maritaca para:
1. Definir estratégia de treinamento
2. Processar base de dados completa
3. Aplicar melhorias iterativas
4. Avaliar e ajustar
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import time
import hashlib
import random
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

def consultar_maritaca(client, versao: str, pergunta: str, contexto: str = "", max_tokens: int = 4000) -> Optional[str]:
    """Consulta Maritaca Sabiá 3"""
    prompt_completo = f"""Você é a Maritaca Sabiá 3, especialista em avaliações educacionais do ENEM.

{contexto}

{pergunta}

Forneça uma resposta detalhada, prática e específica, formatada de forma clara e estruturada."""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt_completo}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt_completo}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️  Erro ao consultar Maritaca: {e}")
        return None

def consultar_estrategia_treinamento(client, versao: str, num_questoes: int) -> Dict:
    """Consulta Maritaca sobre estratégia de treinamento"""
    print("🤖 Consultando Maritaca sobre estratégia de treinamento...")
    print()
    
    contexto = f"""Você está criando um sistema de treinamento para avaliar questões de matemática do ENEM.

Contexto:
- Base de dados: ~{num_questoes} questões de matemática (2009-2025)
- Objetivo: Alcançar 90%+ de acurácia
- API disponível: Maritaca Sabiá 3 (uso ilimitado)
- Resultados anteriores: 56% (sistema simples), 32% (sistema complexo)

O sistema complexo piorou a performance, sugerindo que menos é mais."""
    
    pergunta = """Crie uma estratégia de treinamento completa e eficaz para este sistema.

A estratégia deve incluir:

1. METODOLOGIA DE TREINAMENTO:
   - Como processar a base de dados?
   - Deve ser incremental (poucas questões por vez) ou em lote?
   - Como dividir entre treino e validação?

2. PROMPT OTIMIZADO:
   - Qual a estrutura ideal do prompt?
   - Quais instruções são essenciais?
   - O que evitar (baseado nos erros anteriores)?

3. SISTEMA DE APRENDIZADO:
   - Deve usar few-shot learning? Se sim, como selecionar exemplos?
   - Deve usar análise semântica? Se sim, como e quando?
   - Como evitar sobrecarga de informação?

4. ITERAÇÃO E MELHORIA:
   - Como avaliar o progresso?
   - Como identificar padrões de erro?
   - Como ajustar o sistema baseado nos resultados?

5. IMPLEMENTAÇÃO PRÁTICA:
   - Passos específicos a seguir
   - Ordem de execução
   - Critérios de parada

Forneça a estratégia completa, estruturada e pronta para implementação."""
    
    resposta = consultar_maritaca(client, versao, pergunta, contexto, max_tokens=4000)
    
    if resposta:
        # Tentar extrair estrutura JSON se possível
        import re
        json_match = re.search(r'\{.*\}', resposta, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Retornar como texto estruturado
        return {
            'estrategia_texto': resposta,
            'tipo': 'texto_completo'
        }
    
    return None

def criar_prompt_baseado_estrategia(client, versao: str, estrategia: Dict) -> str:
    """Cria prompt baseado na estratégia da Maritaca"""
    print("🤖 Consultando Maritaca para criar prompt otimizado...")
    print()
    
    contexto = f"""Baseado na estratégia de treinamento definida, crie um prompt otimizado para avaliar questões de matemática do ENEM.

Estratégia:
{json.dumps(estrategia, indent=2, ensure_ascii=False) if isinstance(estrategia, dict) else str(estrategia)}

Resultados anteriores:
- Sistema simples: 56% acurácia
- Sistema complexo: 32% acurácia (piorou)

Objetivo: 90%+ acurácia"""
    
    pergunta = """Crie um prompt otimizado para avaliar questões de matemática do ENEM que:

1. Seja claro e direto (evite complexidade excessiva)
2. Inclua metodologia passo a passo eficaz
3. Evite os erros que levaram o sistema complexo a piorar
4. Foque em precisão matemática
5. Seja eficaz para alcançar 90%+ de acurácia

Forneça o prompt completo, pronto para uso, sem placeholders."""
    
    resposta = consultar_maritaca(client, versao, pergunta, contexto, max_tokens=3000)
    
    if resposta:
        return resposta
    
    # Fallback: prompt baseado em melhores práticas
    return """Você é a Maritaca Sabiá 3, especialista em questões de MATEMÁTICA do ENEM.

Sua tarefa é resolver questões de matemática do ENEM com MÁXIMA PRECISÃO.

METODOLOGIA OBRIGATÓRIA:

1. LEIA ATENTAMENTE: Leia o contexto e a pergunta com cuidado total
2. IDENTIFIQUE: Identifique o tipo de problema e os dados fornecidos
3. PLANEJE: Planeje os passos de resolução
4. RESOLVA: Resolva passo a passo, mostrando todos os cálculos
5. VALIDE: Verifique se sua resposta faz sentido
6. RESPONDA: Responda APENAS com a letra (A, B, C, D ou E)

IMPORTANTE:
- Seja preciso nos cálculos
- Verifique unidades de medida
- Elimine alternativas claramente incorretas
- Não escolha por intuição, use cálculo

Agora, resolva a questão abaixo:"""

def avaliar_questao_com_prompt(client, versao: str, questao: Dict, prompt_template: str) -> Dict:
    """Avalia questão usando prompt otimizado"""
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    
    prompt = f"""{prompt_template}

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)
        prompt += f"{letra}. {alt}\n"
    
    prompt += "\nRESPOSTA: (responda apenas com A, B, C, D ou E)"
    
    resposta_correta = questao.get('label', '').upper().strip()
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
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
            'area': questao.get('area', 'mathematics')
        }
    except Exception as e:
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': None,
            'acerto': False,
            'erro': str(e)
        }

def analisar_erros_com_maritaca(client, versao: str, erros: List[Dict], acuracia: float) -> Dict:
    """Analisa erros e solicita melhorias à Maritaca"""
    print("🤖 Consultando Maritaca para análise de erros e melhorias...")
    print()
    
    # Preparar resumo de erros
    padroes = defaultdict(int)
    for erro in erros:
        correta = erro.get('resposta_correta', '')
        ia = erro.get('resposta_ia', '')
        if correta and ia:
            padrao = f"{correta}→{ia}"
            padroes[padrao] += 1
    
    resumo_erros = "\n".join([f"  - {padrao}: {count} vezes" 
                              for padrao, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True)[:10]])
    
    contexto = f"""Você está analisando os resultados de um sistema de avaliação de questões de matemática do ENEM.

Resultados:
- Total de questões: {len(erros) + (100 - len(erros))} (estimado)
- Erros: {len(erros)}
- Acurácia atual: {acuracia:.2f}%
- Objetivo: 90%+

Padrões de erro mais comuns:
{resumo_erros}"""
    
    pergunta = """Analise esses erros e forneça:

1. ANÁLISE DOS PADRÕES:
   - O que esses padrões de erro indicam?
   - Quais são as causas raízes?

2. MELHORIAS NO PROMPT:
   - O que deve ser ajustado no prompt?
   - Quais instruções adicionar ou remover?
   - Como evitar esses erros específicos?

3. AJUSTES NO SISTEMA:
   - Mudanças na metodologia
   - Melhorias na abordagem
   - Estratégias específicas

Forneça recomendações práticas e específicas, prontas para implementação."""
    
    resposta = consultar_maritaca(client, versao, pergunta, contexto, max_tokens=3000)
    
    if resposta:
        return {
            'analise': resposta,
            'padroes_erro': dict(padroes)
        }
    
    return None

def treinar_iterativo(client, versao: str, questoes: List[Dict], 
                     num_iteracoes: int = 3, questoes_por_iteracao: int = 50) -> Dict:
    """Treinamento iterativo com feedback da Maritaca"""
    print("=" * 70)
    print("🔄 TREINAMENTO ITERATIVO COM MARITACA")
    print("=" * 70)
    print()
    
    # Consultar estratégia inicial
    estrategia = consultar_estrategia_treinamento(client, versao, len(questoes))
    
    if estrategia:
        print("✅ Estratégia de treinamento recebida da Maritaca")
        print()
        # Salvar estratégia
        project_root = Path(__file__).parent.parent.parent
        arquivo_estrategia = project_root / "data" / "analises" / "estrategia_treinamento_maritaca.json"
        with open(arquivo_estrategia, 'w', encoding='utf-8') as f:
            json.dump(estrategia, f, indent=2, ensure_ascii=False)
        print(f"💾 Estratégia salva em: {arquivo_estrategia}")
        print()
    
    # Criar prompt inicial
    prompt_template = criar_prompt_baseado_estrategia(client, versao, estrategia)
    
    # Salvar prompt inicial
    project_root = Path(__file__).parent.parent.parent
    arquivo_prompt = project_root / "data" / "analises" / "prompt_treinamento_v1.txt"
    with open(arquivo_prompt, 'w', encoding='utf-8') as f:
        f.write(prompt_template)
    print(f"💾 Prompt inicial salvo em: {arquivo_prompt}")
    print()
    
    resultados_iteracoes = []
    
    for iteracao in range(1, num_iteracoes + 1):
        print("=" * 70)
        print(f"🔄 ITERAÇÃO {iteracao}/{num_iteracoes}")
        print("=" * 70)
        print()
        
        # Selecionar questões para esta iteração
        questoes_iteracao = random.sample(questoes, min(questoes_por_iteracao, len(questoes)))
        
        print(f"📊 Avaliando {len(questoes_iteracao)} questões...")
        print()
        
        resultados = []
        inicio = time.time()
        
        for i, questao in enumerate(questoes_iteracao, 1):
            print(f"  [{i}/{len(questoes_iteracao)}] {questao.get('id', '')[:40]}...", end=' ', flush=True)
            
            resultado = avaliar_questao_com_prompt(client, versao, questao, prompt_template)
            resultados.append(resultado)
            
            if resultado.get('acerto'):
                print("✅")
            else:
                print(f"❌ (IA: {resultado.get('resposta_ia', 'N/A')}, Correta: {resultado.get('resposta_correta', 'N/A')})")
            
            time.sleep(0.3)  # Rate limiting
        
        tempo_total = time.time() - inicio
        acertos = sum(1 for r in resultados if r.get('acerto'))
        acuracia = (acertos / len(resultados) * 100) if resultados else 0
        
        print()
        print(f"📊 Resultados da Iteração {iteracao}:")
        print(f"   Acertos: {acertos}/{len(resultados)}")
        print(f"   Acurácia: {acuracia:.2f}%")
        print(f"   Tempo: {tempo_total:.1f}s")
        print()
        
        # Analisar erros e obter melhorias
        erros = [r for r in resultados if not r.get('acerto')]
        if erros and iteracao < num_iteracoes:  # Não analisar na última iteração
            analise = analisar_erros_com_maritaca(client, versao, erros, acuracia)
            
            if analise:
                print("📝 Melhorias sugeridas pela Maritaca:")
                print(analise['analise'][:500] + "...")
                print()
                
                # Tentar melhorar prompt baseado na análise
                print("🔄 Aplicando melhorias ao prompt...")
                prompt_melhorado = consultar_maritaca(
                    client, versao,
                    f"""Baseado nesta análise de erros, melhore o prompt atual:

ANÁLISE:
{analise['analise']}

PROMPT ATUAL:
{prompt_template[:1000]}...

Forneça o prompt melhorado, pronto para uso.""",
                    "Melhore o prompt baseado na análise de erros.",
                    max_tokens=3000
                )
                
                if prompt_melhorado:
                    prompt_template = prompt_melhorado
                    print("✅ Prompt atualizado")
                    print()
        
        resultados_iteracoes.append({
            'iteracao': iteracao,
            'resultados': resultados,
            'acertos': acertos,
            'total': len(resultados),
            'acuracia': acuracia,
            'tempo': tempo_total
        })
        
        # Salvar resultados da iteração
        arquivo_iteracao = project_root / "data" / "analises" / f"treinamento_iteracao_{iteracao}.json"
        with open(arquivo_iteracao, 'w', encoding='utf-8') as f:
            json.dump(resultados_iteracoes[-1], f, indent=2, ensure_ascii=False)
    
    # Resultado final
    print("=" * 70)
    print("📊 RESULTADOS FINAIS DO TREINAMENTO")
    print("=" * 70)
    print()
    
    for iteracao in resultados_iteracoes:
        print(f"Iteração {iteracao['iteracao']}: {iteracao['acuracia']:.2f}% ({iteracao['acertos']}/{iteracao['total']})")
    
    melhor_iteracao = max(resultados_iteracoes, key=lambda x: x['acuracia'])
    print()
    print(f"🏆 Melhor iteração: {melhor_iteracao['iteracao']} com {melhor_iteracao['acuracia']:.2f}%")
    print()
    
    # Salvar resultado final
    arquivo_final = project_root / "data" / "analises" / "treinamento_completo_maritaca.json"
    with open(arquivo_final, 'w', encoding='utf-8') as f:
        json.dump({
            'estrategia': estrategia,
            'iteracoes': resultados_iteracoes,
            'melhor_iteracao': melhor_iteracao,
            'prompt_final': prompt_template
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados completos salvos em: {arquivo_final}")
    
    return {
        'estrategia': estrategia,
        'iteracoes': resultados_iteracoes,
        'melhor_iteracao': melhor_iteracao,
        'prompt_final': prompt_template
    }

def main():
    """Função principal"""
    print("=" * 70)
    print("🚀 SISTEMA DE TREINAMENTO COMPLETO COM MARITACA")
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
    
    print("📥 Carregando base de dados completa...")
    questoes = []
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if (questao.get('area') == 'mathematics' and 
                        questao.get('label', '').upper() not in ['ANULADO', '']):
                        questoes.append(questao)
    
    print(f"✅ {len(questoes)} questões de matemática carregadas")
    print()
    
    # Executar treinamento iterativo
    resultado = treinar_iterativo(
        client, versao, questoes,
        num_iteracoes=3,
        questoes_por_iteracao=50
    )
    
    print()
    print("=" * 70)
    print("✅ TREINAMENTO CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    main()

