#!/usr/bin/env python3
"""
📊 Status do Treinamento ENEM 2025
===================================

Mostra o status atual da integração e treinamento.

Uso:
    python 56_status_treinamento.py
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def main():
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    results_dir = project_root / "results"
    
    print("=" * 70)
    print("📊 STATUS DO TREINAMENTO - ENEM 2025")
    print("=" * 70)
    print()
    
    # ========================================================================
    # STATUS DA INTEGRAÇÃO
    # ========================================================================
    print("📥 STATUS DA INTEGRAÇÃO")
    print("-" * 70)
    
    arquivo_completo = processed_dir / "enem_2025_completo.jsonl"
    
    if arquivo_completo.exists():
        questoes = []
        with open(arquivo_completo, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        
        print(f"✅ Arquivo consolidado encontrado: {len(questoes)} questões")
        
        # Estatísticas por área
        stats_por_area = defaultdict(lambda: {
            'total': 0, 'com_label': 0, 'com_imagens': 0, 'incompletas': 0
        })
        
        for q in questoes:
            area = q.get('area', 'unknown')
            stats_por_area[area]['total'] += 1
            if q.get('label') and q['label'] != 'ANULADO':
                stats_por_area[area]['com_label'] += 1
            if q.get('has_images', False):
                stats_por_area[area]['com_imagens'] += 1
            if q.get('incomplete', False):
                stats_por_area[area]['incompletas'] += 1
        
        area_names = {
            'languages': 'Linguagens',
            'human-sciences': 'Humanas',
            'natural-sciences': 'Natureza',
            'mathematics': 'Matemática'
        }
        
        print("\n📋 Por Área:")
        for area in ['languages', 'human-sciences', 'natural-sciences', 'mathematics']:
            stats = stats_por_area[area]
            nome = area_names.get(area, area)
            print(f"  {nome:20s}: {stats['total']:3d} questões | "
                  f"Labels: {stats['com_label']:3d} | "
                  f"Imagens: {stats['com_imagens']:3d} | "
                  f"Incompletas: {stats['incompletas']:3d}")
        
        # Verificar cobertura
        ranges_esperados = {
            'languages': (1, 45),
            'human-sciences': (46, 90),
            'natural-sciences': (91, 135),
            'mathematics': (136, 180)
        }
        
        print("\n📋 Cobertura:")
        for area, (inicio, fim) in ranges_esperados.items():
            questoes_area = [q for q in questoes if q.get('area') == area]
            numeros = sorted([int(q['number']) for q in questoes_area if q.get('number', '').isdigit()])
            nome = area_names.get(area, area)
            
            if numeros:
                faltantes = [i for i in range(inicio, fim + 1) if i not in numeros]
                status = "✅" if not faltantes else "⚠️"
                print(f"  {status} {nome:20s}: {len(questoes_area):3d}/{fim-inicio+1:3d} questões "
                      f"({numeros[0]}-{numeros[-1]})")
                if faltantes:
                    print(f"     Faltantes: {len(faltantes)} questões")
            else:
                print(f"  ❌ {nome:20s}: 0 questões")
    else:
        print("❌ Arquivo consolidado não encontrado")
        print("   Execute: python 54_integrar_todas_questoes_2025.py")
    
    # ========================================================================
    # STATUS DAS AVALIAÇÕES
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 STATUS DAS AVALIAÇÕES")
    print("-" * 70)
    
    if results_dir.exists():
        resultados = list(results_dir.glob("avaliacao_enem_2025_*.json"))
        
        if resultados:
            # Ordenar por data de modificação (mais recente primeiro)
            resultados.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            print(f"✅ {len(resultados)} avaliação(ões) encontrada(s)")
            print()
            
            # Mostrar as 5 mais recentes
            for i, arquivo in enumerate(resultados[:5], 1):
                with open(arquivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                timestamp = data.get('timestamp', '')
                area = data.get('area', 'todas')
                total = data.get('total_questions', 0)
                correct = data.get('correct_answers', 0)
                accuracy = data.get('accuracy', 0)
                
                print(f"{i}. {arquivo.name}")
                print(f"   Área: {area.upper()} | Questões: {total} | "
                      f"Acertos: {correct} | Acurácia: {accuracy:.2f}%")
                
                # Estatísticas por área se disponíveis
                area_stats = data.get('area_stats', {})
                if area_stats:
                    print("   Por área:")
                    for area_name, stats in sorted(area_stats.items()):
                        acc = stats.get('accuracy', 0)
                        print(f"     {area_name:20s}: {stats.get('correct', 0):3d}/{stats.get('total', 0):3d} = {acc:5.1f}%")
                print()
        else:
            print("⚠️  Nenhuma avaliação encontrada")
            print("   Execute: python 55_iniciar_treinamento_2025.py")
    else:
        print("⚠️  Diretório de resultados não encontrado")
    
    # ========================================================================
    # PRÓXIMOS PASSOS
    # ========================================================================
    print("=" * 70)
    print("💡 PRÓXIMOS PASSOS")
    print("-" * 70)
    print()
    
    if not arquivo_completo.exists():
        print("1. Integrar todas as questões:")
        print("   python 54_integrar_todas_questoes_2025.py")
        print()
    
    print("2. Iniciar avaliação completa:")
    print("   python 55_iniciar_treinamento_2025.py --area todas")
    print()
    
    print("3. Iniciar avaliação por área:")
    print("   python 55_iniciar_treinamento_2025.py --area matematica")
    print("   python 55_iniciar_treinamento_2025.py --area natureza")
    print()
    
    print("4. Teste rápido (10 questões):")
    print("   python 55_iniciar_treinamento_2025.py --area matematica --limit 10")
    print()
    
    print("=" * 70)

if __name__ == "__main__":
    main()

