#!/usr/bin/env python3
"""
📊 Gráfico Temporal de Dificuldade - ENEM 2009-2025

Gera visualização da evolução temporal da dificuldade média geral e por área
"""
import json
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_dificuldade_temporal():
    """Carrega dados de dificuldade para análise temporal"""
    project_root = Path(__file__).parent.parent.parent
    
    # Carregar dados completos
    arquivo_completo = project_root / "data" / "analises" / "dificuldade_completo.json"
    
    if not arquivo_completo.exists():
        print("❌ Arquivo de dificuldade completo não encontrado")
        print("   Execute primeiro: 08_heuristica_dificuldade.py")
        return None
    
    with open(arquivo_completo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Extrair dados temporais
    anos = []
    dificuldade_geral = []
    dificuldade_por_area = {
        'Linguagens': [],
        'Humanas': [],
        'Natureza': [],
        'Matemática': []
    }
    
    areas_map = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    for ano_str in sorted(dados.keys(), key=int):
        ano = int(ano_str)
        dados_ano = dados[ano_str]
        questoes = dados_ano.get('questoes', [])
        
        if not questoes:
            continue
        
        # Dificuldade geral (média de todas as questões)
        scores_geral = [q.get('score_dificuldade', 0) for q in questoes]
        media_geral = np.mean(scores_geral) if scores_geral else 0
        
        anos.append(ano)
        dificuldade_geral.append(media_geral)
        
        # Dificuldade por área
        por_area = {}
        for questao in questoes:
            area = questao.get('area', 'desconhecida')
            score = questao.get('score_dificuldade', 0)
            
            if area in areas_map:
                area_nome = areas_map[area]
                if area_nome not in por_area:
                    por_area[area_nome] = []
                por_area[area_nome].append(score)
        
        # Calcular média por área
        for area_nome in dificuldade_por_area.keys():
            if area_nome in por_area:
                media_area = np.mean(por_area[area_nome])
            else:
                media_area = np.nan
            dificuldade_por_area[area_nome].append(media_area)
    
    # Criar DataFrame
    df = pd.DataFrame({
        'ano': anos,
        'Dificuldade Geral': dificuldade_geral,
        'Linguagens': dificuldade_por_area['Linguagens'],
        'Humanas': dificuldade_por_area['Humanas'],
        'Natureza': dificuldade_por_area['Natureza'],
        'Matemática': dificuldade_por_area['Matemática']
    })
    
    return df

def gerar_grafico_temporal(df):
    """Gera gráfico temporal da evolução da dificuldade"""
    
    # Criar figura com subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    
    # ========================================================================
    # GRÁFICO 1: Evolução Geral
    # ========================================================================
    ax1.plot(df['ano'], df['Dificuldade Geral'],
            marker='o', linewidth=3, markersize=10,
            color='#2c3e50', label='Dificuldade Média Geral', alpha=0.9)
    
    # Preencher área
    ax1.fill_between(df['ano'], df['Dificuldade Geral'],
                    alpha=0.3, color='#2c3e50')
    
    # Destacar 2025
    if 2025 in df['ano'].values:
        idx_2025 = df[df['ano'] == 2025].index[0]
        ax1.scatter([2025], [df.loc[idx_2025, 'Dificuldade Geral']],
                   s=200, color='red', zorder=5, edgecolors='black', linewidth=2)
        ax1.annotate('2025', xy=(2025, df.loc[idx_2025, 'Dificuldade Geral']),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=12, fontweight='bold', color='red',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # Linha de tendência
    z = np.polyfit(df['ano'], df['Dificuldade Geral'], 1)
    p = np.poly1d(z)
    ax1.plot(df['ano'], p(df['ano']), "--", alpha=0.5, color='gray',
            linewidth=2, label=f'Tendência (inclinação: {z[0]:.2f})')
    
    ax1.set_xlabel('Ano', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Dificuldade Média', fontsize=14, fontweight='bold')
    ax1.set_title('📈 Evolução Temporal da Dificuldade Média Geral - ENEM (2009-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='best', fontsize=12, framealpha=0.9)
    ax1.set_xlim(df['ano'].min() - 0.5, df['ano'].max() + 0.5)
    
    # ========================================================================
    # GRÁFICO 2: Evolução por Área
    # ========================================================================
    cores = {
        'Linguagens': '#3498db',
        'Humanas': '#e74c3c',
        'Natureza': '#27ae60',
        'Matemática': '#f39c12'
    }
    
    for area in ['Linguagens', 'Humanas', 'Natureza', 'Matemática']:
        dados_area = df[['ano', area]].dropna()
        if len(dados_area) > 0:
            ax2.plot(dados_area['ano'], dados_area[area],
                    marker='o', linewidth=2.5, markersize=7,
                    label=area, color=cores[area], alpha=0.8)
            
            # Preencher área sob a linha
            ax2.fill_between(dados_area['ano'], dados_area[area],
                           alpha=0.15, color=cores[area])
    
    # Destacar 2025
    if 2025 in df['ano'].values:
        ax2.axvline(x=2025, color='red', linestyle='--', linewidth=2,
                   alpha=0.5, label='2025 (Novo)', zorder=0)
    
    ax2.set_xlabel('Ano', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Dificuldade Média', fontsize=14, fontweight='bold')
    ax2.set_title('📊 Evolução Temporal da Dificuldade por Área - ENEM (2009-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax2.grid(True, alpha=0.2, linestyle='--', axis='x')
    ax2.legend(loc='best', fontsize=12, framealpha=0.9, ncol=2)
    ax2.set_xlim(df['ano'].min() - 0.5, df['ano'].max() + 0.5)
    
    # Rotacionar labels do eixo X
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "dificuldade_temporal_2009_2025.png"
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico temporal salvo em: {arquivo}")
    return arquivo

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 GERAÇÃO DE GRÁFICO TEMPORAL DE DIFICULDADE (2009-2025)")
    print("=" * 70)
    print()
    
    # Carregar dados
    print("📥 Carregando dados de dificuldade temporal...")
    df = carregar_dificuldade_temporal()
    
    if df is None:
        return
    
    print(f"✅ Dados carregados: {len(df)} anos")
    print()
    
    # Estatísticas
    print("📊 Estatísticas Temporais:")
    print(f"   Dificuldade Geral:")
    print(f"     Média: {df['Dificuldade Geral'].mean():6.2f}")
    print(f"     Mín: {df['Dificuldade Geral'].min():6.2f}")
    print(f"     Máx: {df['Dificuldade Geral'].max():6.2f}")
    print(f"     Primeiro ano (2009): {df[df['ano'] == 2009]['Dificuldade Geral'].values[0]:6.2f}")
    if 2025 in df['ano'].values:
        print(f"     Último ano (2025): {df[df['ano'] == 2025]['Dificuldade Geral'].values[0]:6.2f}")
    print()
    
    # Gerar gráfico
    print("🎨 Gerando gráfico temporal...")
    arquivo = gerar_grafico_temporal(df)
    
    print()
    print("=" * 70)
    print("✅ GRÁFICO TEMPORAL GERADO COM SUCESSO")
    print("=" * 70)
    print(f"📁 Arquivo: {arquivo}")

if __name__ == "__main__":
    main()

