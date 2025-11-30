#!/usr/bin/env python3
"""
Sistema Integrado com Maritaca Sabiá 3

Sempre consulta a Maritaca antes de:
- Criar prompts
- Analisar erros
- Melhorar metodologias
- Interpretar resultados
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
    prompt_completo = f"""Você é a Maritaca Sabiá 3, especialista em avaliações educacionais do ENEM (Exame Nacional do Ensino Médio).

{contexto}

{pergunta}

Forneça uma resposta detalhada, prática e específica baseada na sua expertise em ENEM."""
    
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

def criar_prompt_com_maritaca(client, versao: str, area: str, exemplo_questao: Dict = None) -> Optional[str]:
    """Sempre consulta Maritaca para criar prompt otimizado"""
    contexto = f"""Você está criando um prompt para avaliar questões do ENEM na área de {area}.

O prompt será usado pela própria Maritaca Sabiá 3 para avaliar questões do ENEM.
O objetivo é alcançar 90%+ de acurácia."""
    
    if exemplo_questao:
        contexto += f"""

Exemplo de questão:
Contexto: {exemplo_questao.get('context', '')[:200]}...
Pergunta: {exemplo_questao.get('question', '')[:200]}...
Alternativas: {len(exemplo_questao.get('alternatives', []))} alternativas"""
    
    pergunta = f"""Crie um prompt otimizado para avaliar questões do ENEM na área de {area}.

O prompt deve:
1. Ser específico para questões de {area} do ENEM
2. Maximizar a acurácia (objetivo: 90%+)
3. Usar metodologia passo a passo clara e obrigatória
4. Eliminar vieses na escolha de alternativas (especialmente evitar escolher B por padrão)
5. Incluir instruções específicas para {area}
6. Ser eficaz para questões do ENEM

Forneça o prompt completo, pronto para uso, sem placeholders."""
    
    return consultar_maritaca(client, versao, pergunta, contexto, max_tokens=3000)

def melhorar_prompt_existente_com_maritaca(client, versao: str, prompt_atual: str, 
                                          resultados: Dict = None) -> Optional[str]:
    """Consulta Maritaca para melhorar prompt existente"""
    contexto = "Você está analisando e melhorando um prompt usado para avaliar questões do ENEM."
    
    if resultados:
        contexto += f"""

Resultados atuais:
- Acurácia: {resultados.get('acuracia', 0):.2f}%
- Objetivo: 90%+
"""
    
    pergunta = f"""Analise o seguinte prompt:

{prompt_atual}

Como especialista em ENEM, como posso melhorar este prompt para:
1. Aumentar a acurácia para 90%+
2. Melhorar especialmente matemática (atualmente 33-35%)
3. Eliminar vieses na escolha de alternativas
4. Tornar mais eficaz para questões do ENEM

Forneça:
- Análise do prompt atual
- Sugestões específicas de melhoria
- Versão melhorada completa do prompt
- Justificativas baseadas em sua experiência com ENEM"""
    
    return consultar_maritaca(client, versao, pergunta, contexto, max_tokens=3000)

def analisar_erros_com_maritaca(client, versao: str, erros: List[Dict]) -> Optional[str]:
    """Sempre consulta Maritaca para analisar erros"""
    # Preparar resumo
    erros_por_area = {}
    padroes = {}
    
    for erro in erros:
        area = erro.get('area', 'desconhecida')
        erros_por_area[area] = erros_por_area.get(area, 0) + 1
        
        correta = erro.get('resposta_correta', '')
        ia = erro.get('resposta_ia', '')
        if correta and ia:
            padroes[f"{correta}→{ia}"] = padroes.get(f"{correta}→{ia}", 0) + 1
    
    resumo = f"""Total de erros: {len(erros)}

Erros por área:
"""
    for area, count in sorted(erros_por_area.items(), key=lambda x: x[1], reverse=True):
        resumo += f"  - {area}: {count} erros\n"
    
    resumo += "\nPadrões de erro mais comuns:\n"
    for padrao, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True)[:5]:
        resumo += f"  - {padrao}: {count} vezes\n"
    
    pergunta = f"""Analisei os seguintes erros:

{resumo}

Como especialista em ENEM, me ajude a:
1. Identificar causas raízes
2. Sugerir melhorias específicas no prompt
3. Fornecer estratégias para aumentar acurácia
4. Focar especialmente em matemática (área com maior dificuldade)

Forneça análise detalhada e sugestões práticas."""
    
    return consultar_maritaca(client, versao, pergunta, 
                             contexto="Você está analisando erros em questões do ENEM para melhorar a acurácia.")

def interpretar_resultados_com_maritaca(client, versao: str, resultados: Dict) -> Optional[str]:
    """Sempre consulta Maritaca para interpretar resultados"""
    resumo = f"""Resultados da avaliação:
- Total: {resultados.get('total', 0)} questões
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

Forneça análise detalhada e recomendações práticas."""
    
    return consultar_maritaca(client, versao, pergunta,
                             contexto="Você está interpretando resultados de avaliação de questões do ENEM.")

# Exportar funções principais
__all__ = [
    'configurar_api_maritaca',
    'consultar_maritaca',
    'criar_prompt_com_maritaca',
    'melhorar_prompt_existente_com_maritaca',
    'analisar_erros_com_maritaca',
    'interpretar_resultados_com_maritaca'
]


