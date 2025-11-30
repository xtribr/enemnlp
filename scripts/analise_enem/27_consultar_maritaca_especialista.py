#!/usr/bin/env python3
"""
Sistema de Consulta à Maritaca Sabiá 3 (Especialista ENEM)

Sempre consulta a Maritaca antes de análises, criação de prompts, etc.
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

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

def consultar_maritaca(client, versao: str, pergunta: str, contexto: str = "", max_tokens: int = 2000) -> Optional[str]:
    """Consulta Maritaca Sabiá 3 como especialista ENEM"""
    prompt = f"""Você é a Maritaca Sabiá 3, especialista em avaliações educacionais do ENEM (Exame Nacional do Ensino Médio).

{contexto}

{pergunta}

Forneça uma resposta detalhada, prática e específica baseada na sua expertise em ENEM."""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️  Erro ao consultar Maritaca: {e}")
        return None

def melhorar_prompt_com_maritaca(client, versao: str, prompt_atual: str, contexto: str = "") -> Optional[str]:
    """Consulta Maritaca para melhorar um prompt"""
    pergunta = f"""Analise o seguinte prompt que estou usando para avaliar questões do ENEM:

{prompt_atual}

Com base na sua expertise em ENEM, como posso melhorar este prompt para:
1. Aumentar a acurácia (objetivo: 90%)
2. Melhorar especialmente o desempenho em matemática (atualmente 33-35%)
3. Eliminar vieses na escolha de alternativas
4. Tornar o prompt mais eficaz para questões do ENEM

Forneça:
- Análise do prompt atual
- Sugestões específicas de melhoria
- Versão melhorada do prompt (se possível)
- Justificativas baseadas em sua experiência com ENEM"""
    
    return consultar_maritaca(client, versao, pergunta, contexto)

def analisar_erros_com_maritaca(client, versao: str, erros: List[Dict], contexto: str = "") -> Optional[str]:
    """Consulta Maritaca para analisar erros"""
    # Preparar resumo dos erros
    resumo = f"""
Total de erros: {len(erros)}

Erros por área:
"""
    erros_por_area = {}
    for erro in erros:
        area = erro.get('area', 'desconhecida')
        erros_por_area[area] = erros_por_area.get(area, 0) + 1
    
    for area, count in sorted(erros_por_area.items(), key=lambda x: x[1], reverse=True):
        resumo += f"  - {area}: {count} erros\n"
    
    # Padrões de erro
    padroes = {}
    for erro in erros:
        correta = erro.get('resposta_correta', '')
        ia = erro.get('resposta_ia', '')
        if correta and ia:
            padrao = f"{correta}→{ia}"
            padroes[padrao] = padroes.get(padrao, 0) + 1
    
    resumo += "\nPadrões de erro mais comuns:\n"
    for padrao, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True)[:5]:
        resumo += f"  - {padrao}: {count} vezes\n"
    
    pergunta = f"""Analisei os seguintes erros em questões do ENEM:

{resumo}

Como especialista em ENEM, me ajude a:
1. Identificar as causas raízes desses erros
2. Sugerir melhorias específicas no prompt
3. Fornecer estratégias para aumentar a acurácia
4. Focar especialmente em matemática (área com maior dificuldade)

Forneça uma análise detalhada e sugestões práticas."""
    
    return consultar_maritaca(client, versao, pergunta, contexto)

def criar_prompt_otimizado_com_maritaca(client, versao: str, area: str, contexto_questao: str = "") -> Optional[str]:
    """Consulta Maritaca para criar prompt otimizado para uma área específica"""
    pergunta = f"""Preciso criar um prompt otimizado para avaliar questões do ENEM na área de {area}.

{contexto_questao}

Como especialista em ENEM, crie um prompt que:
1. Seja específico para questões de {area}
2. Maximize a acurácia (objetivo: 90%+)
3. Use metodologia passo a passo
4. Elimine vieses na escolha de alternativas
5. Seja eficaz para questões do ENEM

Forneça o prompt completo e otimizado."""
    
    return consultar_maritaca(client, versao, pergunta)

def analisar_resultados_com_maritaca(client, versao: str, resultados: Dict, contexto: str = "") -> Optional[str]:
    """Consulta Maritaca para analisar resultados"""
    resumo = f"""
Resultados da avaliação:
- Total de questões: {resultados.get('total', 0)}
- Acertos: {resultados.get('acertos', 0)}
- Erros: {resultados.get('erros', 0)}
- Acurácia: {resultados.get('acuracia', 0):.2f}%

Acurácia por área:
"""
    for area, dados in resultados.get('por_area', {}).items():
        acuracia = (dados['acertos'] / dados['total'] * 100) if dados['total'] > 0 else 0
        resumo += f"  - {area}: {acuracia:.2f}% ({dados['acertos']}/{dados['total']})\n"
    
    pergunta = f"""Analisei os seguintes resultados:

{resumo}

Como especialista em ENEM, me ajude a:
1. Interpretar esses resultados
2. Identificar pontos fortes e fracos
3. Sugerir melhorias específicas
4. Ajustar estratégias para alcançar 90% de acurácia

Forneça uma análise detalhada e recomendações práticas."""
    
    return consultar_maritaca(client, versao, pergunta, contexto)

def main():
    """Exemplo de uso"""
    print("=" * 70)
    print("🤖 SISTEMA DE CONSULTA À MARITACA SABIÁ 3")
    print("=" * 70)
    print()
    
    client, versao = configurar_api_maritaca()
    if not client:
        print("❌ API não configurada")
        return
    
    print("✅ API configurada")
    print()
    print("💡 Este módulo fornece funções para sempre consultar a Maritaca")
    print("   antes de análises, criação de prompts, etc.")
    print()
    print("Funções disponíveis:")
    print("  - melhorar_prompt_com_maritaca()")
    print("  - analisar_erros_com_maritaca()")
    print("  - criar_prompt_otimizado_com_maritaca()")
    print("  - analisar_resultados_com_maritaca()")
    print("  - consultar_maritaca() (genérico)")

if __name__ == "__main__":
    main()


