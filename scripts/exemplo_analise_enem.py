#!/usr/bin/env python3
"""
Exemplo prático: Análise de resultados do ENEM com API Maritaca

Este script demonstra como usar os resultados da avaliação para análises educacionais.
"""
import json
import sys
import os
from pathlib import Path

def carregar_resultados(caminho_arquivo):
    """Carrega resultados de uma avaliação do ENEM"""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return None

def analisar_por_area(resultados):
    """Analisa resultados por área de conhecimento"""
    if not resultados or 'results' not in resultados:
        print("❌ Formato de resultados inválido")
        return None
    
    areas = {
        'languages': 'Linguagens e Códigos',
        'human-sciences': 'Ciências Humanas',
        'natural-sciences': 'Ciências da Natureza',
        'mathematics': 'Matemática'
    }
    
    analise = {}
    
    for task_name, task_results in resultados['results'].items():
        if 'acc' in task_results:
            analise[task_name] = {
                'acuracias_por_area': {},
                'acuracias_geral': task_results.get('acc', 0)
            }
            
            for area_key, area_name in areas.items():
                if area_key in task_results:
                    analise[task_name]['acuracias_por_area'][area_name] = task_results[area_key]
    
    return analise

def gerar_relatorio_texto(analise):
    """Gera relatório em texto formatado"""
    if not analise:
        return "Nenhum dado para relatório"
    
    relatorio = []
    relatorio.append("=" * 70)
    relatorio.append("📊 RELATÓRIO DE ANÁLISE - ENEM")
    relatorio.append("=" * 70)
    relatorio.append("")
    
    for task_name, dados in analise.items():
        relatorio.append(f"📋 Tarefa: {task_name}")
        relatorio.append(f"   Acurácia Geral: {dados['acuracias_geral']:.2%}")
        relatorio.append("")
        relatorio.append("   Acurácia por Área:")
        
        for area, acuracia in dados['acuracias_por_area'].items():
            barra = "█" * int(acuracia * 50)  # Barra visual
            relatorio.append(f"   • {area:30s}: {acuracia:6.2%} {barra}")
        
        relatorio.append("")
        relatorio.append("-" * 70)
        relatorio.append("")
    
    return "\n".join(relatorio)

def identificar_areas_fracas(analise, threshold=0.7):
    """Identifica áreas com acurácia abaixo do threshold"""
    areas_fracas = {}
    
    for task_name, dados in analise.items():
        areas_fracas[task_name] = []
        for area, acuracia in dados['acuracias_por_area'].items():
            if acuracia < threshold:
                areas_fracas[task_name].append({
                    'area': area,
                    'acuracia': acuracia,
                    'diferenca': threshold - acuracia
                })
    
    return areas_fracas

def main():
    """Função principal"""
    print("=" * 70)
    print("🔍 ANÁLISE DE RESULTADOS ENEM - API MARITACA")
    print("=" * 70)
    print()
    
    # Verifica argumentos
    if len(sys.argv) < 2:
        print("📋 Uso: python exemplo_analise_enem.py <caminho_arquivo_resultados.json>")
        print()
        print("💡 Exemplo:")
        print("   python exemplo_analise_enem.py reports/sabia3_enem2024.json")
        print()
        print("📁 Arquivos disponíveis em reports/:")
        reports_dir = Path("reports")
        if reports_dir.exists():
            for arquivo in sorted(reports_dir.glob("*.json")):
                print(f"   • {arquivo}")
        return
    
    caminho_arquivo = sys.argv[1]
    
    # Carrega resultados
    print(f"🔄 Carregando resultados de: {caminho_arquivo}")
    resultados = carregar_resultados(caminho_arquivo)
    
    if not resultados:
        return
    
    print("✅ Resultados carregados com sucesso!")
    print()
    
    # Analisa por área
    print("📊 Analisando resultados por área de conhecimento...")
    analise = analisar_por_area(resultados)
    
    if not analise:
        print("❌ Não foi possível analisar os resultados")
        return
    
    # Gera relatório
    relatorio = gerar_relatorio_texto(analise)
    print(relatorio)
    
    # Identifica áreas fracas
    print("🔍 Identificando áreas com acurácia < 70%...")
    areas_fracas = identificar_areas_fracas(analise, threshold=0.7)
    
    tem_areas_fracas = False
    for task_name, areas in areas_fracas.items():
        if areas:
            tem_areas_fracas = True
            print(f"\n⚠️  {task_name}:")
            for area_info in areas:
                print(f"   • {area_info['area']}: {area_info['acuracia']:.2%} "
                      f"(abaixo do esperado em {area_info['diferenca']:.2%})")
    
    if not tem_areas_fracas:
        print("✅ Todas as áreas estão acima de 70% de acurácia!")
    
    print()
    print("=" * 70)
    print("✅ Análise concluída!")
    print("=" * 70)
    
    # Salva relatório em arquivo
    output_file = Path(caminho_arquivo).stem + "_analise.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    print(f"💾 Relatório salvo em: {output_file}")

if __name__ == "__main__":
    main()


