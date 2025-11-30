#!/usr/bin/env python3
"""
AUDITORIA COMPLETA DO SISTEMA - Usando 100% Maritaca

Analisa o sistema atual e identifica oportunidades de melhoria usando
a expertise completa da Maritaca Sabiá 3.
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
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

def consultar_maritaca(client, versao: str, pergunta: str, contexto: str = "", max_tokens: int = 3000) -> Optional[str]:
    """Consulta Maritaca Sabiá 3"""
    prompt_completo = f"""Você é a Maritaca Sabiá 3, especialista em avaliações educacionais do ENEM.

{contexto}

{pergunta}

Forneça uma resposta detalhada, prática e específica."""
    
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

def auditoria_sistema_atual():
    """Analisa o sistema atual"""
    print("=" * 70)
    print("🔍 AUDITORIA DO SISTEMA ATUAL")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    
    # 1. Verificar embeddings
    print("1️⃣  EMBEDDINGS:")
    embeddings_dir = project_root / "data" / "embeddings"
    if embeddings_dir.exists():
        arquivos_emb = list(embeddings_dir.glob("*.npy"))
        print(f"   ✅ {len(arquivos_emb)} arquivos de embeddings encontrados")
        print(f"   📝 Modelo usado: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        print(f"   ⚠️  NÃO usa Maritaca para gerar embeddings")
    else:
        print(f"   ❌ Diretório de embeddings não encontrado")
    print()
    
    # 2. Verificar avaliações
    print("2️⃣  AVALIAÇÕES:")
    analises_dir = project_root / "data" / "analises"
    if analises_dir.exists():
        arquivos_aval = list(analises_dir.glob("*avaliacao*.json"))
        print(f"   ✅ {len(arquivos_aval)} arquivos de avaliação encontrados")
        for arquivo in arquivos_aval[-3:]:  # Últimos 3
            try:
                with open(arquivo) as f:
                    dados = json.load(f)
                    acuracia = dados.get('acuracia', 0)
                    total = dados.get('total', 0)
                    print(f"   📊 {arquivo.name}: {acuracia:.2f}% ({total} questões)")
            except:
                pass
    print()
    
    # 3. Verificar uso da Maritaca
    print("3️⃣  USO DA MARITACA:")
    print("   ✅ Usada para criar prompts otimizados")
    print("   ✅ Usada para analisar erros")
    print("   ⚠️  NÃO usada para gerar embeddings semânticos")
    print("   ⚠️  NÃO usada para encontrar questões similares")
    print("   ⚠️  NÃO usada para few-shot learning")
    print("   ⚠️  NÃO usada para análise semântica profunda")
    print()
    
    # 4. Verificar dados
    print("4️⃣  DADOS DISPONÍVEIS:")
    processed_dir = project_root / "data" / "processed"
    if processed_dir.exists():
        arquivos = list(processed_dir.glob("enem_*_completo.jsonl"))
        print(f"   ✅ {len(arquivos)} arquivos de dados processados")
        total_questoes = 0
        for arquivo in arquivos:
            with open(arquivo, 'r', encoding='utf-8') as f:
                total_questoes += sum(1 for line in f if line.strip())
        print(f"   📊 Total: ~{total_questoes} questões")
    print()

def consultar_maritaca_sobre_melhorias(client, versao: str):
    """Consulta Maritaca sobre como melhorar o sistema usando 100% dela"""
    print("=" * 70)
    print("🤖 CONSULTANDO MARITACA SOBRE MELHORIAS")
    print("=" * 70)
    print()
    
    contexto = """Você está analisando um sistema de avaliação de questões do ENEM que atualmente tem:
- Acurácia de 56% em matemática (objetivo: 90%)
- Usa embeddings de sentence-transformers (não usa Maritaca)
- Usa Maritaca apenas para criar prompts e analisar erros
- Tem acesso a ~2.800 questões do ENEM (2009-2025)
- Tem acesso ilimitado à API Maritaca Sabiá 3

O sistema precisa ser melhorado para usar 100% da expertise da Maritaca."""
    
    pergunta = """Como podemos melhorar este sistema para usar 100% da minha expertise (Maritaca Sabiá 3) e alcançar 90%+ de acurácia?

Considere:
1. Como usar a Maritaca para gerar embeddings semânticos melhores?
2. Como usar a Maritaca para análise semântica profunda antes de avaliar?
3. Como usar a Maritaca para encontrar questões similares e fazer few-shot learning?
4. Como usar a Maritaca para criar um sistema de "treinamento" adaptativo?
5. Como usar a Maritaca para análise de padrões e tendências nas questões?
6. Como usar a Maritaca para criar um sistema de validação cruzada?
7. Outras estratégias usando 100% da minha expertise?

Forneça um plano detalhado e prático, com priorização das melhorias mais impactantes."""
    
    print("🤖 Consultando Maritaca...")
    resposta = consultar_maritaca(client, versao, pergunta, contexto, max_tokens=4000)
    
    if resposta:
        print()
        print("=" * 70)
        print("📝 RESPOSTA DA MARITACA:")
        print("=" * 70)
        print()
        print(resposta)
        print()
        
        # Salvar resposta
        project_root = Path(__file__).parent.parent.parent
        arquivo = project_root / "data" / "analises" / "auditoria_maritaca_melhorias.json"
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': time.time(),
                'auditoria': resposta,
                'tipo': 'melhorias_sistema_100_maritaca'
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resposta salva em: {arquivo}")
    else:
        print("❌ Erro ao consultar Maritaca")

def main():
    """Função principal"""
    print("=" * 70)
    print("🔍 AUDITORIA COMPLETA DO SISTEMA")
    print("🎯 Objetivo: Usar 100% Maritaca para alcançar 90%+ acurácia")
    print("=" * 70)
    print()
    
    # Auditoria do sistema atual
    auditoria_sistema_atual()
    
    # Consultar Maritaca
    print("🤖 Configurando API Maritaca...")
    client, versao = configurar_api_maritaca()
    if not client:
        print("❌ API não configurada")
        return
    
    print("✅ API configurada")
    print()
    
    consultar_maritaca_sobre_melhorias(client, versao)
    
    print()
    print("=" * 70)
    print("✅ AUDITORIA CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()

