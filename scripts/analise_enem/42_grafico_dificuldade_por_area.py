#!/usr/bin/env python3
"""
📊 Gráfico de Dificuldade por Área - ENEM 2009-2025

Gera visualização cronológica da dificuldade média por área de conhecimento
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

def carregar_dificuldade_por_area():
    """Carrega dados de dificuldade agrupados por área e ano"""
    project_root = Path(__file__).parent.parent.parent
    
    # Carregar dados completos
    arquivo_completo = project_root / "data" / "analises" / "dificuldade_completo.json"
    
    if not arquivo_completo.exists():
        print("❌ Arquivo de dificuldade completo não encontrado")
        print("   Execute primeiro: 08_heuristica_dificuldade.py")
        return None
    
    with open(arquivo_completo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Estrutura: {ano: {questoes: [...], estatisticas: {...}}}
    # Cada questão tem: area, score_dificuldade
    
    # Agrupar por área e ano
    dificuldade_por_area_ano = {}
    
    areas_map = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    for ano_str, dados_ano in dados.items():
        ano = int(ano_str)
        questoes = dados_ano.get('questoes', [])
        
        # Agrupar por área
        por_area = {}
        for questao in questoes:
            area = questao.get('area', 'desconhecida')
            score = questao.get('score_dificuldade', 0)
            
            if area not in por_area:
                por_area[area] = []
            por_area[area].append(score)
        
        # Calcular média por área
        for area, scores in por_area.items():
            if area in areas_map:
                area_nome = areas_map[area]
                if area_nome not in dificuldade_por_area_ano:
                    dificuldade_por_area_ano[area_nome] = {}
                dificuldade_por_area_ano[area_nome][ano] = np.mean(scores)
    
    # 2025 já deve estar incluído nos dados acima se foi processado corretamente
    # Não precisamos recalcular com metodologia simplificada
    
    # Converter para DataFrame
    todas_areas = sorted(dificuldade_por_area_ano.keys())
    todos_anos = sorted(set(ano for area_data in dificuldade_por_area_ano.values() 
                            for ano in area_data.keys()))
    
    df_data = {'ano': todos_anos}
    for area in todas_areas:
        df_data[area] = [dificuldade_por_area_ano[area].get(ano, np.nan) 
                        for ano in todos_anos]
    
    df = pd.DataFrame(df_data)
    return df

def gerar_grafico(df):
    """Gera gráfico de evolução da dificuldade por área"""
    
    # Cores para cada área
    cores = {
        'Linguagens': '#3498db',
        'Humanas': '#e74c3c',
        'Natureza': '#27ae60',
        'Matemática': '#f39c12'
    }
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Plotar linha para cada área
    for area in df.columns[1:]:  # Pular coluna 'ano'
        if area in cores:
            dados_area = df[['ano', area]].dropna()
            ax.plot(dados_area['ano'], dados_area[area],
                   marker='o', linewidth=2.5, markersize=8,
                   label=area, color=cores[area], alpha=0.8)
            
            # Preencher área sob a linha
            ax.fill_between(dados_area['ano'], dados_area[area],
                           alpha=0.2, color=cores[area])
    
    # Destacar 2025 se disponível
    if 2025 in df['ano'].values:
        ax.axvline(x=2025, color='red', linestyle='--', linewidth=2,
                  alpha=0.5, label='2025 (Novo)', zorder=0)
    
    # Configurar eixos
    ax.set_xlabel('Ano', fontsize=14, fontweight='bold')
    ax.set_ylabel('Dificuldade Média', fontsize=14, fontweight='bold')
    ax.set_title('📊 Evolução da Dificuldade Média por Área - ENEM (2009-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    
    # Ajustar eixos
    ax.set_xlim(df['ano'].min() - 0.5, df['ano'].max() + 0.5)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.grid(True, alpha=0.2, linestyle='--', axis='x')
    
    # Legenda
    ax.legend(loc='best', fontsize=12, framealpha=0.9)
    
    # Rotacionar labels do eixo X
    plt.xticks(rotation=45, ha='right')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "dificuldade_por_area_2009_2025.png"
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico salvo em: {arquivo}")
    return arquivo

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 GERAÇÃO DE GRÁFICO DE DIFICULDADE POR ÁREA (2009-2025)")
    print("=" * 70)
    print()
    
    # Carregar dados
    print("📥 Carregando dados de dificuldade por área...")
    df = carregar_dificuldade_por_area()
    
    if df is None:
        return
    
    print(f"✅ Dados carregados: {len(df)} anos, {len(df.columns)-1} áreas")
    print()
    
    # Estatísticas
    print("📊 Estatísticas por Área:")
    for area in df.columns[1:]:  # Pular coluna 'ano'
        dados_area = df[area].dropna()
        if len(dados_area) > 0:
            print(f"   {area:15} | Média: {dados_area.mean():6.2f} | "
                  f"Min: {dados_area.min():6.2f} | Max: {dados_area.max():6.2f}")
    print()
    
    # Gerar gráfico
    print("🎨 Gerando gráfico...")
    arquivo = gerar_grafico(df)
    
    print()
    print("=" * 70)
    print("✅ GRÁFICO GERADO COM SUCESSO")
    print("=" * 70)
    print(f"📁 Arquivo: {arquivo}")

if __name__ == "__main__":
    main()

