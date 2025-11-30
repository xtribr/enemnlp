#!/usr/bin/env python3
"""
Script para verificar progresso do Passo 1
"""
import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
arquivo = project_root / "data" / "analises" / "avaliacao_acuracia_maritaca.json"

if arquivo.exists():
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total = 0
        acertos = 0
        anos_processados = []
        
        for ano, dados in data.items():
            if ano == '_geral':
                continue
            if isinstance(dados, dict) and 'estatisticas' in dados:
                stats = dados['estatisticas']
                total += stats.get('total', 0)
                acertos += stats.get('acertos', 0)
                anos_processados.append(ano)
        
        if total > 0:
            acuracia = (acertos / total) * 100
            print("=" * 70)
            print("📊 PROGRESSO DO PASSO 1")
            print("=" * 70)
            print(f"\n✅ Anos processados: {len(anos_processados)}")
            print(f"   {sorted(anos_processados)}")
            print(f"\n📊 Questões processadas: {total} de 2891")
            print(f"   Progresso: {(total/2891)*100:.1f}%")
            print(f"\n🎯 Acertos: {acertos}")
            print(f"   Acurácia parcial: {acuracia:.2f}%")
            
            if '_geral' in data:
                geral = data['_geral']
                print(f"\n📈 Acurácia geral: {geral.get('acuracia_geral', 0):.2f}%")
            
            print("\n" + "=" * 70)
        else:
            print("📊 Arquivo existe mas ainda processando...")
    except Exception as e:
        print(f"⚠️  Erro ao ler arquivo: {e}")
else:
    print("📊 Passo 1 ainda não gerou arquivo de resultados")
    print("   O script está processando...")


