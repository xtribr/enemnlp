#!/usr/bin/env python3
"""
Analisa resultados da avaliação oficial
"""
import json
import sys
from pathlib import Path

def analisar_resultados(arquivo_resultados: Path):
    """Analisa resultados da avaliação oficial"""
    
    print("=" * 70)
    print("📊 ANÁLISE DE RESULTADOS OFICIAL")
    print("=" * 70)
    print()
    
    if not arquivo_resultados.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_resultados}")
        return
    
    with open(arquivo_resultados, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Extrair resultados
    if 'results' in dados:
        resultados = dados['results']
    else:
        resultados = dados
    
    print("📈 Resultados por Área:")
    print()
    
    areas = {}
    total_por_area = {}
    
    # Processar resultados
    for task_name, task_data in resultados.items():
        if 'enem_cot_2024_captions' in task_name:
            # Extrair área se disponível
            if 'by_area' in task_data:
                for area, area_data in task_data['by_area'].items():
                    if area not in areas:
                        areas[area] = {'acertos': 0, 'total': 0}
                    areas[area]['acertos'] += area_data.get('acc', 0) * area_data.get('total', 0) / 100
                    areas[area]['total'] += area_data.get('total', 0)
            
            # Resultado geral
            if 'acc' in task_data:
                print(f"   Acurácia Geral: {task_data['acc']:.2f}%")
                if 'total' in task_data:
                    print(f"   Total de questões: {task_data['total']}")
    
    # Mostrar por área
    if areas:
        print()
        print("📊 Resultados Detalhados por Área:")
        print()
        for area, dados_area in areas.items():
            acuracia = (dados_area['acertos'] / dados_area['total'] * 100) if dados_area['total'] > 0 else 0
            print(f"   {area.capitalize()}: {acuracia:.2f}% ({dados_area['acertos']:.0f}/{dados_area['total']})")
    
    # Comparação
    print()
    print("=" * 70)
    print("📊 COMPARAÇÃO COM RESULTADOS ANTERIORES")
    print("=" * 70)
    print()
    print("Sistema Oficial (enem_cot_2024_captions + few-shot 3):")
    if areas.get('mathematics'):
        acuracia_math = (areas['mathematics']['acertos'] / areas['mathematics']['total'] * 100) if areas['mathematics']['total'] > 0 else 0
        print(f"   Matemática: {acuracia_math:.2f}%")
    print()
    print("Scripts Customizados:")
    print("   Matemática: 24-56% (média)")
    print()
    print("Esperado (do README):")
    print("   Matemática: 82-91% (Sabiá-3 com CoT + captions)")
    print()

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        # Procurar arquivo mais recente
        project_root = Path(__file__).parent.parent.parent
        results_dir = project_root / "results"
        arquivos = sorted(results_dir.glob("avaliacao_oficial*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        if arquivos:
            arquivo = arquivos[0]
            print(f"📁 Usando arquivo mais recente: {arquivo}")
            print()
        else:
            print("❌ Nenhum arquivo de resultados encontrado")
            print("   Execute primeiro: python scripts/analise_enem/36_avaliar_com_sistema_oficial.py")
            return
    else:
        arquivo = Path(sys.argv[1])
    
    analisar_resultados(arquivo)

if __name__ == "__main__":
    main()

