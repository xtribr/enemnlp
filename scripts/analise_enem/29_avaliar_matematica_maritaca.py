#!/usr/bin/env python3
"""
Avaliar 100 questões de matemática usando sistema integrado com Maritaca

Sempre consulta Maritaca para otimizar prompts e análises.
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

def carregar_questoes_matematica(num_questoes: int = 100):
    """Carrega questões de matemática"""
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    todas_matematica = []
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if (questao.get('area') == 'mathematics' and 
                        questao.get('label', '').upper() not in ['ANULADO', '']):
                        todas_matematica.append(questao)
    
    # Amostrar
    if len(todas_matematica) > num_questoes:
        amostra = random.sample(todas_matematica, num_questoes)
    else:
        amostra = todas_matematica
    
    return amostra

def criar_prompt_com_maritaca(client, versao: str, exemplo_questao: Dict = None) -> str:
    """Sempre consulta Maritaca para criar prompt otimizado para matemática"""
    import importlib.util
    
    modulo_path = Path(__file__).parent / "28_sistema_maritaca_integrado.py"
    spec = importlib.util.spec_from_file_location("sistema_maritaca", modulo_path)
    if spec and spec.loader:
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        prompt_base = modulo.criar_prompt_com_maritaca(client, versao, "mathematics", exemplo_questao)
        
        if prompt_base and exemplo_questao:
            # Adicionar questão específica
            contexto = exemplo_questao.get('context', '').strip()
            pergunta = exemplo_questao.get('question', '').strip()
            alternativas = exemplo_questao.get('alternatives', [])
            
            prompt_completo = f"""{prompt_base}

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
            for i, alt in enumerate(alternativas, 1):
                letra = chr(64 + i)
                prompt_completo += f"{letra}. {alt}\n"
            
            prompt_completo += """
RESPOSTA FINAL:
Após seguir TODOS os passos da metodologia acima, responda APENAS com a letra da alternativa correta (A, B, C, D ou E).
NÃO inclua explicações, apenas a letra."""
            
            return prompt_completo
    
    return None

def criar_prompt_template_com_maritaca(client, versao: str, usar_maritaca: bool = True) -> str:
    """Cria template de prompt otimizado"""
    if usar_maritaca:
        # Consultar Maritaca para criar template
        import importlib.util
        
        modulo_path = Path(__file__).parent / "28_sistema_maritaca_integrado.py"
        spec = importlib.util.spec_from_file_location("sistema_maritaca", modulo_path)
        if spec and spec.loader:
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            prompt_template = modulo.criar_prompt_com_maritaca(client, versao, "mathematics", None)
            if prompt_template:
                return prompt_template
    
    # Fallback: usar prompt melhorado baseado na análise
    import importlib.util
    modulo_path = Path(__file__).parent / "31_prompt_melhorado_matematica.py"
    spec = importlib.util.spec_from_file_location("prompt_melhorado", modulo_path)
    if spec and spec.loader:
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo.criar_prompt_melhorado_matematica()
    
    return None

def avaliar_questao(client, questao: Dict, versao: str, prompt_template: str = None) -> Dict:
    """Avalia uma questão usando prompt otimizado pela Maritaca"""
    # Usar template criado pela Maritaca (reutilizar)
    if not prompt_template:
        # Fallback se não tiver template
        return {
            'id': questao.get('id', ''),
            'resposta_correta': questao.get('label', '').upper().strip(),
            'resposta_ia': None,
            'acerto': False,
            'erro': 'Template de prompt não disponível'
        }
    
    # Adicionar questão específica ao template
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
    
    prompt += """
RESPOSTA FINAL:
Após seguir TODOS os passos da metodologia acima, mostre seu raciocínio completo e, no final, responda com:
RESPOSTA: [A/B/C/D/E]

Siga TODOS os 8 passos antes de dar sua resposta final."""
    
    resposta_correta = questao.get('label', '').upper().strip()
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,  # Permitir raciocínio detalhado
                temperature=0.0
            )
            resposta_completa = response.choices[0].message.content.strip()
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,  # Permitir raciocínio detalhado
                temperature=0.0
            )
            resposta_completa = response.choices[0].message.content.strip()
        
        # Extrair resposta (procurar por "RESPOSTA:" ou última letra A-E)
        resposta_ia = None
        resposta_upper = resposta_completa.upper()
        
        # Procurar por "RESPOSTA: X" ou "RESPOSTA X"
        import re
        match = re.search(r'RESPOSTA[:\s]+([A-E])', resposta_upper)
        if match:
            resposta_ia = match.group(1)
        else:
            # Procurar última ocorrência de A, B, C, D ou E isolada
            matches = re.findall(r'\b([A-E])\b', resposta_upper)
            if matches:
                resposta_ia = matches[-1]  # Última letra encontrada
        acerto = resposta_ia == resposta_correta if resposta_ia else False
        
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': resposta_ia,
            'acerto': acerto,
            'area': 'mathematics'
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
    """Função principal"""
    print("=" * 70)
    print("🧮 AVALIAÇÃO DE 100 QUESTÕES DE MATEMÁTICA")
    print("🤖 Usando Sistema Integrado com Maritaca Sabiá 3")
    print("=" * 70)
    print()
    
    # Configurar API
    print("🔧 Configurando API Maritaca...")
    client, versao = configurar_api_maritaca()
    if not client:
        return
    
    print("✅ API configurada")
    print()
    
    # Carregar questões (aceita argumento de linha de comando)
    import sys
    num_questoes = 100
    if len(sys.argv) > 1:
        try:
            num_questoes = int(sys.argv[1])
        except ValueError:
            pass
    
    print(f"📥 Carregando {num_questoes} questões de matemática...")
    questoes = carregar_questoes_matematica(num_questoes=num_questoes)
    print(f"✅ {len(questoes)} questões carregadas")
    print()
    
    # Criar template otimizado (com consulta Maritaca + melhorias baseadas em análise)
    print("🤖 Criando prompt otimizado...")
    print("   (Baseado na análise de erros da Maritaca)")
    print()
    
    prompt_template = criar_prompt_template_com_maritaca(client, versao, usar_maritaca=True)
    
    if prompt_template:
        print("✅ Prompt otimizado criado!")
        print(f"   Template: {len(prompt_template)} caracteres")
        print("   Inclui: metodologia 8 passos, validação, eliminação de vieses")
    else:
        print("⚠️  Não foi possível criar template")
        print("   Usando prompt melhorado padrão...")
        # Fallback direto
        import importlib.util
        modulo_path = Path(__file__).parent / "31_prompt_melhorado_matematica.py"
        spec = importlib.util.spec_from_file_location("prompt_melhorado", modulo_path)
        if spec and spec.loader:
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            prompt_template = modulo.criar_prompt_melhorado_matematica()
    print()
    
    # Avaliar
    print("🚀 Iniciando avaliação...")
    tempo_estimado = len(questoes) * 2  # ~2s por questão (com raciocínio detalhado)
    print(f"   ⏱️  Estimativa: ~{tempo_estimado} segundos ({len(questoes)} questões × ~2s)")
    print()
    
    resultados = []
    acertos = 0
    
    for i, questao in enumerate(questoes, 1):
        print(f"  [{i}/{len(questoes)}] {questao.get('id', '')[:40]}...", end=' ', flush=True)
        
        resultado = avaliar_questao(client, questao, versao, prompt_template)
        resultados.append(resultado)
        
        if resultado.get('acerto'):
            acertos += 1
            print("✅")
        else:
            print(f"❌ (IA: {resultado.get('resposta_ia', 'N/A')}, Correta: {resultado.get('resposta_correta', 'N/A')})")
        
        time.sleep(0.3)  # Rate limiting (reduzido para acelerar)
    
    acuracia = (acertos / len(questoes) * 100) if questoes else 0
    
    # Resultados
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print(f"Total de questões: {len(questoes)}")
    print(f"Acertos: {acertos}")
    print(f"Erros: {len(questoes) - acertos}")
    print(f"Acurácia: {acuracia:.2f}%")
    print()
    
    # Comparação
    print("📈 Comparação com resultado anterior:")
    print(f"   Acurácia anterior (matemática): 33.52%")
    print(f"   Acurácia atual:                  {acuracia:.2f}%")
    diferenca = acuracia - 33.52
    if diferenca > 0:
        print(f"   ✅ Melhoria: +{diferenca:.2f}%")
    else:
        print(f"   ⚠️  Redução: {diferenca:.2f}%")
    
    # Padrões de erro
    erros = [r for r in resultados if not r.get('acerto')]
    if erros:
        print()
        print("📊 Padrões de erro:")
        padroes = {}
        for erro in erros:
            correta = erro.get('resposta_correta', '')
            ia = erro.get('resposta_ia', '')
            if correta and ia:
                padrao = f"{correta}→{ia}"
                padroes[padrao] = padroes.get(padrao, 0) + 1
        
        for padrao, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {padrao:10s}: {count:2d} vezes")
    
    print()
    print("=" * 70)
    
    if acuracia >= 90:
        print("🎉 OBJETIVO ALCANÇADO! Acurácia >= 90%")
    elif acuracia >= 70:
        print("✅ Boa melhoria! Acurácia >= 70%")
        print(f"   Faltam {90 - acuracia:.2f}% para 90%")
    else:
        print(f"📈 Acurácia: {acuracia:.2f}%")
        print(f"   Faltam {90 - acuracia:.2f}% para 90%")
        print("   Continue otimizando com ajuda da Maritaca")
    
    # Salvar resultados
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "analises" / f"avaliacao_matematica_{len(questoes)}_maritaca.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump({
            'resultados': resultados,
            'total': len(questoes),
            'acertos': acertos,
            'erros': len(questoes) - acertos,
            'acuracia': acuracia,
            'usou_maritaca': True
        }, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"💾 Resultados salvos em: {arquivo}")

if __name__ == "__main__":
    main()

