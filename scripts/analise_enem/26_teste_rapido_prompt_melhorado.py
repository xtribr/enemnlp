#!/usr/bin/env python3
"""
Teste rápido do prompt melhorado em amostra de questões

Compara o desempenho do prompt melhorado com o anterior.
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List
import time
import random

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

def formatar_questao_para_maritaca(questao: Dict, usar_campos_semanticos: bool = True) -> str:
    """Formata questão com prompt melhorado (baseado na análise da Maritaca)"""
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    area = questao.get('area', 'desconhecida')
    campos_semanticos = questao.get('campos_semanticos', [])
    
    area_nomes = {
        'languages': 'Linguagens, Códigos e suas Tecnologias',
        'human-sciences': 'Ciências Humanas e suas Tecnologias',
        'natural-sciences': 'Ciências da Natureza e suas Tecnologias',
        'mathematics': 'Matemática e suas Tecnologias'
    }
    area_nome = area_nomes.get(area, area)
    
    instrucoes_especificas = {
        'mathematics': """
ATENÇÃO CRÍTICA PARA MATEMÁTICA (área com maior dificuldade):
- Questões de matemática frequentemente envolvem múltiplos passos de resolução
- QUEBRE O PROBLEMA EM ETAPAS CLARAS e resolva cada uma individualmente
- Identifique e aplique fórmulas relevantes, mostrando cada substituição de variáveis
- Verifique todos os cálculos aritméticos e algébricos com cuidado
- Preste atenção EXTREMA a detalhes numéricos e unidades de medida
- Use CHECAGEM DIMENSIONAL: elimine alternativas com unidades incorretas
- Use ESTIMATIVAS RÁPIDAS para eliminar opções claramente desproporcionais
- Após resolver, VERIFIQUE se a resposta se encaixa nos dados fornecidos
- Traduza corretamente problemas de palavras em equações matemáticas
- NÃO escolha uma alternativa sem verificar os cálculos passo a passo
""",
    }
    
    prompt = f"""Você é um especialista em avaliações educacionais do ENEM (Exame Nacional do Ensino Médio).

ÁREA DE CONHECIMENTO: {area_nome}
"""
    
    if usar_campos_semanticos and campos_semanticos:
        prompt += f"CAMPOS SEMÂNTICOS IDENTIFICADOS: {', '.join(campos_semanticos)}\n"
        prompt += "Use esses campos para contextualizar melhor a questão.\n"
    
    prompt += instrucoes_especificas.get(area, "")
    
    prompt += f"""
METODOLOGIA DE RESOLUÇÃO OBRIGATÓRIA (siga estes passos em ordem):

PASSO 1 - INTERPRETAÇÃO DO PROBLEMA:
- Leia o contexto completo com atenção total
- Identifique EXATAMENTE o que a pergunta está pedindo
- Sublinhe ou liste mentalmente os dados fornecidos
- Identifique palavras-chave que indicam operações ou conceitos específicos

PASSO 2 - ESCOLHA DA ABORDAGEM:
- Decida qual método, fórmula ou conceito aplicar
- Para matemática: identifique as fórmulas relevantes
- Para ciências: identifique os princípios científicos envolvidos
- Para linguagens/humanas: identifique o tema central e intenção

PASSO 3 - RESOLUÇÃO PASSO A PASSO:
- Quebre o problema em etapas menores e resolva cada uma individualmente
- Para matemática: mostre cada substituição de variáveis e cálculo
- Execute a resolução de forma sistemática
- NÃO pule etapas

PASSO 4 - ELIMINAÇÃO DE ALTERNATIVAS:
Analise CADA alternativa individualmente e elimine as incorretas:
- Checagem Dimensional (matemática/ciências): Verifique se as unidades estão corretas
- Estimativas: Use estimativas rápidas para eliminar opções claramente desproporcionais
- Verificação Conceitual: A alternativa está correta do ponto de vista técnico/conceitual?
- Verificação Contextual: A alternativa faz sentido no contexto apresentado?
- Resposta Direta: A alternativa responde diretamente à pergunta feita?

PASSO 5 - VERIFICAÇÃO FINAL:
- Revise se a resposta faz sentido no contexto do problema
- Verifique se está em conformidade com as unidades de medida (se aplicável)
- Confirme que a resposta responde corretamente à pergunta feita
- NÃO escolha uma alternativa apenas porque parece plausível

PASSO 6 - ESCOLHA FINAL:
- Compare as alternativas restantes cuidadosamente
- Escolha a alternativa que melhor responde à pergunta
- Se não tiver certeza, analise novamente - NÃO escolha B por padrão
- Evite qualquer viés em direção a uma alternativa específica

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
RESPOSTA FINAL:
Após seguir TODOS os 6 passos da metodologia acima, responda APENAS com a letra da alternativa correta (A, B, C, D ou E).

IMPORTANTE:
- NÃO inclua explicações, apenas a letra
- NÃO escolha B por padrão em caso de incerteza
- Se não tiver certeza após seguir todos os passos, analise novamente
- A resposta deve ser baseada na resolução passo a passo, não em intuição"""
    
    return prompt

def avaliar_questao(client, questao: Dict, versao: str, usar_campos_semanticos: bool = True) -> Dict:
    """Avalia uma questão usando API Maritaca"""
    prompt = formatar_questao_para_maritaca(questao, usar_campos_semanticos)
    resposta_correta = questao.get('label', '').upper().strip()
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        
        resposta_ia = resposta_ia[0] if resposta_ia and resposta_ia[0] in ['A', 'B', 'C', 'D', 'E'] else None
        acerto = resposta_ia == resposta_correta if resposta_ia else False
        
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': resposta_ia,
            'acerto': acerto,
            'area': questao.get('area', 'desconhecida')
        }
    except Exception as e:
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': None,
            'acerto': False,
            'erro': str(e)
        }

def carregar_amostra_questoes(num_questoes: int = 100, focar_matematica: bool = True):
    """Carrega amostra de questões para teste"""
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    todas_questoes = []
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if questao.get('label', '').upper() not in ['ANULADO', '']:
                        todas_questoes.append(questao)
    
    if focar_matematica:
        questoes_matematica = [q for q in todas_questoes if q.get('area') == 'mathematics']
        questoes_outras = [q for q in todas_questoes if q.get('area') != 'mathematics']
        
        num_mat = min(int(num_questoes * 0.6), len(questoes_matematica))
        num_outras = num_questoes - num_mat
        
        amostra = random.sample(questoes_matematica, num_mat)
        amostra.extend(random.sample(questoes_outras, min(num_outras, len(questoes_outras))))
        random.shuffle(amostra)
    else:
        amostra = random.sample(todas_questoes, min(num_questoes, len(todas_questoes)))
    
    return amostra

def main():
    """Função principal"""
    print("=" * 70)
    print("🧪 TESTE RÁPIDO - PROMPT MELHORADO")
    print("=" * 70)
    print()
    print("📊 Testando prompt melhorado baseado na análise da Maritaca")
    print("   Foco: Matemática (área com maior dificuldade - 33.52%)")
    print()
    
    # Configurar API
    client, versao = configurar_api_maritaca()
    if not client:
        return
    
    # Carregar amostra
    print("📥 Carregando amostra de 100 questões (60% matemática)...")
    questoes = carregar_amostra_questoes(num_questoes=100, focar_matematica=True)
    print(f"✅ {len(questoes)} questões carregadas")
    print()
    
    # Avaliar
    print("🔄 Avaliando com prompt melhorado...")
    print()
    
    resultados = []
    acertos = 0
    
    for i, questao in enumerate(questoes, 1):
        print(f"  [{i}/{len(questoes)}] {questao.get('id', '')[:30]}...", end=' ')
        
        resultado = avaliar_questao(client, questao, versao, usar_campos_semanticos=True)
        resultados.append(resultado)
        
        if resultado.get('acerto'):
            acertos += 1
            print("✅")
        else:
            print(f"❌ (IA: {resultado.get('resposta_ia', 'N/A')}, Correta: {resultado.get('resposta_correta', 'N/A')})")
        
        time.sleep(0.5)
    
    acuracia = (acertos / len(questoes) * 100) if questoes else 0
    
    # Análise
    print()
    print("=" * 70)
    print("📊 RESULTADOS DO TESTE")
    print("=" * 70)
    print(f"Total: {len(questoes)} questões")
    print(f"Acertos: {acertos}")
    print(f"Erros: {len(questoes) - acertos}")
    print(f"Acurácia: {acuracia:.2f}%")
    print()
    
    # Por área
    resultados_por_area = {}
    for res in resultados:
        area = res.get('area', 'desconhecida')
        if area not in resultados_por_area:
            resultados_por_area[area] = {'total': 0, 'acertos': 0}
        resultados_por_area[area]['total'] += 1
        if res.get('acerto'):
            resultados_por_area[area]['acertos'] += 1
    
    print("📊 Acurácia por área:")
    for area, dados in sorted(resultados_por_area.items()):
        acuracia_area = (dados['acertos'] / dados['total'] * 100) if dados['total'] > 0 else 0
        print(f"   {area:20s}: {acuracia_area:5.2f}% ({dados['acertos']}/{dados['total']})")
    
    # Comparação
    print()
    print("📈 Comparação com resultado anterior:")
    print(f"   Acurácia anterior: 73.79%")
    print(f"   Acurácia atual:    {acuracia:.2f}%")
    diferenca = acuracia - 73.79
    if diferenca > 0:
        print(f"   ✅ Melhoria: +{diferenca:.2f}%")
    else:
        print(f"   ⚠️  Redução: {diferenca:.2f}%")
    
    if 'mathematics' in resultados_por_area:
        mat_atual = (resultados_por_area['mathematics']['acertos'] / 
                    resultados_por_area['mathematics']['total'] * 100)
        print()
        print("📊 Matemática (área crítica):")
        print(f"   Acurácia anterior: 33.52%")
        print(f"   Acurácia atual:    {mat_atual:.2f}%")
        diferenca_mat = mat_atual - 33.52
        if diferenca_mat > 0:
            print(f"   ✅ Melhoria: +{diferenca_mat:.2f}%")
        else:
            print(f"   ⚠️  Redução: {diferenca_mat:.2f}%")
    
    print()
    print("=" * 70)
    
    # Salvar
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "analises" / "teste_rapido_prompt_melhorado.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump({
            'resultados': resultados,
            'total': len(questoes),
            'acertos': acertos,
            'acuracia': acuracia,
            'por_area': resultados_por_area
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {arquivo}")

if __name__ == "__main__":
    main()
