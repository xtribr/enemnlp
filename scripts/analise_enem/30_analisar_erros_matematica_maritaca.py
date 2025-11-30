#!/usr/bin/env python3
"""
Analisa erros de matemática consultando Maritaca
"""
import json
import sys
import os
from pathlib import Path

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

def consultar_maritaca(client, versao: str, pergunta: str, contexto: str = "") -> str:
    """Consulta Maritaca"""
    prompt = f"""Você é a Maritaca Sabiá 3, especialista em avaliações educacionais do ENEM.

{contexto}

{pergunta}"""
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            return response.choices[0].message.content
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"Erro: {e}"

def main():
    """Função principal"""
    print("=" * 70)
    print("🤖 ANÁLISE DE ERROS COM MARITACA - MATEMÁTICA")
    print("=" * 70)
    print()
    
    # Carregar resultados
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "analises" / "avaliacao_matematica_100_maritaca.json"
    
    if not arquivo.exists():
        print("❌ Arquivo de resultados não encontrado")
        print("   Execute primeiro: 29_avaliar_matematica_maritaca.py")
        return
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    erros = [r for r in dados['resultados'] if not r.get('acerto')]
    acuracia = dados.get('acuracia', 0)
    
    print(f"📊 Resultados atuais:")
    print(f"   Total: {dados.get('total', 0)} questões")
    print(f"   Acertos: {dados.get('acertos', 0)}")
    print(f"   Erros: {len(erros)}")
    print(f"   Acurácia: {acuracia:.2f}%")
    print()
    
    # Preparar análise
    erros_por_padrao = {}
    for erro in erros:
        correta = erro.get('resposta_correta', '')
        ia = erro.get('resposta_ia', '')
        if correta and ia:
            padrao = f"{correta}→{ia}"
            erros_por_padrao[padrao] = erros_por_padrao.get(padrao, 0) + 1
    
    resumo = f"""Avaliei 100 questões de matemática do ENEM e obtive {acuracia:.2f}% de acurácia.

Padrões de erro mais comuns:
"""
    for padrao, count in sorted(erros_por_padrao.items(), key=lambda x: x[1], reverse=True)[:10]:
        resumo += f"  - {padrao}: {count} vezes\n"
    
    resumo += f"""
Total de erros: {len(erros)}
Objetivo: 90% de acurácia (atualmente {acuracia:.2f}%)
"""
    
    # Consultar Maritaca
    print("🤖 Consultando Maritaca para análise detalhada...")
    print()
    
    client, versao = configurar_api_maritaca()
    if not client:
        print("❌ API não configurada")
        return
    
    pergunta = f"""Analise os seguintes resultados de avaliação de questões de matemática do ENEM:

{resumo}

Como especialista em ENEM, me ajude a:
1. Identificar as causas raízes desses erros
2. Entender por que a acurácia está em {acuracia:.2f}% (objetivo: 90%)
3. Sugerir melhorias específicas no prompt para matemática
4. Fornecer estratégias práticas para aumentar a acurácia
5. Focar especialmente nos padrões de erro mais comuns (C→B, A→B, etc.)

Forneça uma análise detalhada e sugestões práticas e específicas."""
    
    contexto = "Você está analisando erros em questões de matemática do ENEM para melhorar a acurácia de 36% para 90%."
    
    analise = consultar_maritaca(client, versao, pergunta, contexto)
    
    print("=" * 70)
    print("📝 ANÁLISE DA MARITACA:")
    print("=" * 70)
    print()
    print(analise)
    print()
    
    # Salvar análise
    dados['analise_maritaca_erros'] = analise
    dados['analise_maritaca_timestamp'] = time.time()
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print("=" * 70)
    print("💾 Análise salva no arquivo de resultados")
    print("=" * 70)

if __name__ == "__main__":
    import time
    main()


