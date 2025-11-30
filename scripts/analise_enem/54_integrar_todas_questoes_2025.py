#!/usr/bin/env python3
"""
🔄 Integrar Todas as 180 Questões do ENEM 2025
===============================================

Este script consolida todas as questões extraídas das imagens e integra ao sistema.

Uso:
    python 54_integrar_todas_questoes_2025.py
"""

import json
import sys
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_questoes_jsonl(arquivo: Path) -> List[Dict]:
    """Carrega questões de um arquivo JSONL."""
    questoes = []
    if arquivo.exists():
        with open(arquivo, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
    return questoes

def validar_questao(questao: Dict) -> bool:
    """Valida se uma questão está completa."""
    # Verificar campos obrigatórios
    if not questao.get('id'):
        return False
    if not questao.get('question') and not questao.get('context'):
        return False
    if not questao.get('alternatives') or len(questao.get('alternatives', [])) < 2:
        return False
    if questao.get('label') == 'ANULADO' and not questao.get('incomplete', False):
        # Questões sem label são válidas se não estiverem marcadas como incompletas
        pass
    return True

def normalizar_questao(questao: Dict) -> Dict:
    """Normaliza uma questão para garantir formato consistente."""
    # Garantir que number é string
    if 'number' in questao:
        questao['number'] = str(questao['number'])
    
    # Garantir que exam é string
    if 'exam' in questao:
        questao['exam'] = str(questao['exam'])
    
    # Garantir que label é maiúscula
    if 'label' in questao:
        questao['label'] = str(questao['label']).upper().strip()
    
    # Garantir 5 alternativas
    if 'alternatives' in questao:
        while len(questao['alternatives']) < 5:
            questao['alternatives'].append('')
        questao['alternatives'] = questao['alternatives'][:5]
    
    # Garantir campos padrão
    if 'has_images' not in questao:
        questao['has_images'] = False
    
    if 'incomplete' not in questao:
        questao['incomplete'] = False
    
    return questao

def main():
    """Função principal."""
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "enem"
    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("🔄 INTEGRAÇÃO COMPLETA - ENEM 2025 (180 QUESTÕES)")
    print("=" * 70)
    print()
    
    # ========================================================================
    # CARREGAR TODAS AS QUESTÕES
    # ========================================================================
    print("📥 Carregando questões de todas as áreas...")
    
    arquivos_por_area = {
        'languages': data_dir / "enem_2025_linguagens_imagens.jsonl",
        'human-sciences': data_dir / "enem_2025_humanas_imagens.jsonl",
        'natural-sciences': data_dir / "enem_2025_natureza_imagens.jsonl",
        'mathematics': data_dir / "enem_2025_matematica_imagens.jsonl"
    }
    
    todas_questoes = []
    stats_por_area = defaultdict(lambda: {'total': 0, 'validas': 0, 'com_label': 0, 'com_imagens': 0})
    
    for area, arquivo in arquivos_por_area.items():
        print(f"\n  📂 {area}:")
        questoes_area = carregar_questoes_jsonl(arquivo)
        print(f"    Carregadas: {len(questoes_area)} questões")
        
        for questao in questoes_area:
            questao_norm = normalizar_questao(questao)
            todas_questoes.append(questao_norm)
            
            stats_por_area[area]['total'] += 1
            if validar_questao(questao_norm):
                stats_por_area[area]['validas'] += 1
            if questao_norm.get('label') and questao_norm['label'] != 'ANULADO':
                stats_por_area[area]['com_label'] += 1
            if questao_norm.get('has_images', False):
                stats_por_area[area]['com_imagens'] += 1
        
        print(f"    Válidas: {stats_por_area[area]['validas']}/{stats_por_area[area]['total']}")
        print(f"    Com label: {stats_por_area[area]['com_label']}/{stats_por_area[area]['total']}")
        print(f"    Com imagens: {stats_por_area[area]['com_imagens']}/{stats_por_area[area]['total']}")
    
    # Ordenar por número
    todas_questoes.sort(key=lambda x: (
        x.get('area', ''),
        int(x.get('number', 0)) if x.get('number', '').isdigit() else 0
    ))
    
    print(f"\n✅ Total carregado: {len(todas_questoes)} questões")
    
    # ========================================================================
    # VALIDAÇÃO E ESTATÍSTICAS
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 VALIDAÇÃO E ESTATÍSTICAS")
    print("=" * 70)
    
    questoes_validas = [q for q in todas_questoes if validar_questao(q)]
    questoes_com_label = [q for q in todas_questoes if q.get('label') and q['label'] != 'ANULADO']
    questoes_incompletas = [q for q in todas_questoes if q.get('incomplete', False)]
    questoes_com_imagens = [q for q in todas_questoes if q.get('has_images', False)]
    
    print(f"\n📋 Estatísticas Gerais:")
    print(f"  Total de questões: {len(todas_questoes)}")
    print(f"  Questões válidas: {len(questoes_validas)} ({len(questoes_validas)/len(todas_questoes)*100:.1f}%)")
    print(f"  Questões com label: {len(questoes_com_label)} ({len(questoes_com_label)/len(todas_questoes)*100:.1f}%)")
    print(f"  Questões com imagens: {len(questoes_com_imagens)} ({len(questoes_com_imagens)/len(todas_questoes)*100:.1f}%)")
    print(f"  Questões incompletas: {len(questoes_incompletas)}")
    
    # Verificar cobertura
    print(f"\n📋 Cobertura por Área:")
    ranges_esperados = {
        'languages': (1, 45),
        'human-sciences': (46, 90),
        'natural-sciences': (91, 135),
        'mathematics': (136, 180)
    }
    
    area_names = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    for area, (inicio, fim) in ranges_esperados.items():
        questoes_area = [q for q in todas_questoes if q.get('area') == area]
        numeros = sorted([int(q['number']) for q in questoes_area if q.get('number', '').isdigit()])
        nome = area_names.get(area, area)
        
        print(f"\n  {nome} ({inicio}-{fim}):")
        print(f"    Extraídas: {len(questoes_area)} questões")
        if numeros:
            print(f"    Range: {numeros[0]}-{numeros[-1]}")
            faltantes = [i for i in range(inicio, fim + 1) if i not in numeros]
            if faltantes:
                print(f"    ⚠️  Faltantes: {len(faltantes)} questões")
            else:
                print(f"    ✅ Completo!")
        else:
            print(f"    ⚠️  Nenhuma questão extraída")
    
    # ========================================================================
    # SALVAR ARQUIVO CONSOLIDADO
    # ========================================================================
    print("\n" + "=" * 70)
    print("💾 SALVANDO ARQUIVO CONSOLIDADO")
    print("=" * 70)
    
    arquivo_consolidado = processed_dir / "enem_2025_completo.jsonl"
    with open(arquivo_consolidado, 'w', encoding='utf-8') as f:
        for questao in todas_questoes:
            f.write(json.dumps(questao, ensure_ascii=False) + '\n')
    
    print(f"\n✅ {len(todas_questoes)} questões salvas em:")
    print(f"   {arquivo_consolidado}")
    
    # Salvar também por área
    for area in ['languages', 'human-sciences', 'natural-sciences', 'mathematics']:
        questoes_area = [q for q in todas_questoes if q.get('area') == area]
        if questoes_area:
            arquivo_area = processed_dir / f"enem_2025_{area}.jsonl"
            with open(arquivo_area, 'w', encoding='utf-8') as f:
                for questao in questoes_area:
                    f.write(json.dumps(questao, ensure_ascii=False) + '\n')
            print(f"   {arquivo_area.name}: {len(questoes_area)} questões")
    
    # ========================================================================
    # RESUMO FINAL
    # ========================================================================
    print("\n" + "=" * 70)
    print("✅ INTEGRAÇÃO CONCLUÍDA")
    print("=" * 70)
    
    print(f"\n📊 Resumo Final:")
    print(f"  Total de questões: {len(todas_questoes)}")
    print(f"  Questões válidas: {len(questoes_validas)}")
    print(f"  Questões com label: {len(questoes_com_label)}")
    print(f"  Questões com imagens: {len(questoes_com_imagens)}")
    
    if questoes_incompletas:
        print(f"\n⚠️  Questões incompletas ({len(questoes_incompletas)}):")
        for q in questoes_incompletas[:5]:
            print(f"    - {q.get('id')} ({q.get('area')})")
        if len(questoes_incompletas) > 5:
            print(f"    ... e mais {len(questoes_incompletas) - 5} questões")
    
    print(f"\n💡 Próximos passos:")
    print(f"   1. Executar avaliação com Maritaca Sabiá-3")
    print(f"   2. Gerar análises de acurácia por área")
    print(f"   3. Comparar com resultados históricos")
    
    return len(todas_questoes), len(questoes_validas), len(questoes_com_label)

if __name__ == "__main__":
    main()

