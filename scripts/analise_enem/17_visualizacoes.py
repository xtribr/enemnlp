#!/usr/bin/env python3
"""
Visualizações Interativas para Análises do ENEM

Cria gráficos e dashboards para visualizar resultados das análises.
"""
import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_dados_analises(analises_dir: Path) -> Dict:
    """Carrega todos os dados de análises"""
    dados = {}
    
    # Série temporal
    arquivo_serie = analises_dir / "serie_temporal_areas.csv"
    if arquivo_serie.exists():
        dados['serie_temporal'] = pd.read_csv(arquivo_serie)
    
    # Dificuldade
    arquivo_dificuldade = analises_dir / "dificuldade_estatisticas.json"
    if arquivo_dificuldade.exists():
        with open(arquivo_dificuldade, 'r', encoding='utf-8') as f:
            dados['dificuldade'] = json.load(f)
    
    # Similaridade
    arquivo_similaridade = analises_dir / "similaridade_provas.json"
    if arquivo_similaridade.exists():
        with open(arquivo_similaridade, 'r', encoding='utf-8') as f:
            dados['similaridade'] = json.load(f)
    
    # Predições
    arquivo_predicoes = analises_dir / "predicoes_tendencias.json"
    if arquivo_predicoes.exists():
        with open(arquivo_predicoes, 'r', encoding='utf-8') as f:
            dados['predicoes'] = json.load(f)
    
    return dados

def criar_grafico_serie_temporal(df: pd.DataFrame, output_dir: Path):
    """Cria gráfico de série temporal"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Para não precisar de display
        
        plt.figure(figsize=(14, 8))
        
        areas = ['languages', 'human-sciences', 'natural-sciences', 'mathematics']
        cores = {'languages': '#1f77b4', 'human-sciences': '#ff7f0e', 
                 'natural-sciences': '#2ca02c', 'mathematics': '#d62728'}
        nomes = {'languages': 'Linguagens', 'human-sciences': 'Humanas',
                 'natural-sciences': 'Natureza', 'mathematics': 'Matemática'}
        
        for area in areas:
            if area in df.columns:
                plt.plot(df['ano'], df[area], marker='o', label=nomes[area], 
                        color=cores[area], linewidth=2, markersize=6)
        
        plt.plot(df['ano'], df['total'], marker='s', label='Total', 
                color='black', linewidth=2.5, markersize=8, linestyle='--')
        
        plt.xlabel('Ano', fontsize=12, fontweight='bold')
        plt.ylabel('Número de Questões', fontsize=12, fontweight='bold')
        plt.title('Série Temporal do ENEM por Área de Conhecimento (2009-2024)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        arquivo = output_dir / "serie_temporal_areas.png"
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✅ Gráfico salvo: {arquivo.name}")
        return True
    
    except ImportError:
        print("  ⚠️  matplotlib não instalado. Instale com: pip install matplotlib")
        return False
    except Exception as e:
        print(f"  ❌ Erro ao criar gráfico: {e}")
        return False

def criar_grafico_dificuldade(dados_dificuldade: Dict, output_dir: Path):
    """Cria gráfico de dificuldade ao longo dos anos"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        
        anos = sorted([int(ano) for ano in dados_dificuldade.keys()])
        medias = [dados_dificuldade[str(ano)]['media_dificuldade'] for ano in anos]
        
        plt.figure(figsize=(12, 6))
        plt.plot(anos, medias, marker='o', linewidth=2, markersize=8, color='#2c3e50')
        plt.fill_between(anos, medias, alpha=0.3, color='#3498db')
        
        plt.xlabel('Ano', fontsize=12, fontweight='bold')
        plt.ylabel('Dificuldade Média', fontsize=12, fontweight='bold')
        plt.title('Evolução da Dificuldade Média das Questões do ENEM (2009-2024)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        arquivo = output_dir / "dificuldade_temporal.png"
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✅ Gráfico salvo: {arquivo.name}")
        return True
    
    except Exception as e:
        print(f"  ❌ Erro ao criar gráfico: {e}")
        return False

def criar_heatmap_similaridade(dados_similaridade: Dict, output_dir: Path):
    """Cria heatmap de similaridade entre provas"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import matplotlib
        matplotlib.use('Agg')
        
        # Extrair anos e criar matriz
        tipos = ['similaridade_lexical_cosseno', 'similaridade_semantica']
        
        for tipo in tipos:
            if tipo not in dados_similaridade or not dados_similaridade[tipo]:
                continue
            
            # Extrair anos
            anos = sorted(set(
                int(ano) for par in dados_similaridade[tipo].keys()
                for ano in par.split('-')
            ))
            
            # Criar matriz
            matriz = np.zeros((len(anos), len(anos)))
            for i, ano1 in enumerate(anos):
                for j, ano2 in enumerate(anos):
                    if i == j:
                        matriz[i, j] = 1.0
                    else:
                        chave = f"{min(ano1, ano2)}-{max(ano1, ano2)}"
                        matriz[i, j] = dados_similaridade[tipo].get(chave, 0.0)
            
            # Criar heatmap
            plt.figure(figsize=(14, 12))
            sns.heatmap(matriz, annot=True, fmt='.2f', cmap='YlOrRd', 
                       xticklabels=anos, yticklabels=anos,
                       cbar_kws={'label': 'Similaridade'})
            
            nome_tipo = tipo.replace('similaridade_', '').replace('_', ' ').title()
            plt.title(f'Matriz de Similaridade entre Provas - {nome_tipo}', 
                     fontsize=14, fontweight='bold', pad=20)
            plt.xlabel('Ano', fontsize=12, fontweight='bold')
            plt.ylabel('Ano', fontsize=12, fontweight='bold')
            plt.tight_layout()
            
            arquivo = output_dir / f"heatmap_similaridade_{tipo.split('_')[-1]}.png"
            plt.savefig(arquivo, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"  ✅ Heatmap salvo: {arquivo.name}")
    
    except ImportError:
        print("  ⚠️  seaborn não instalado. Instale com: pip install seaborn")
    except Exception as e:
        print(f"  ❌ Erro ao criar heatmap: {e}")

def criar_dashboard_html(dados: Dict, output_dir: Path):
    """Cria dashboard HTML interativo"""
    try:
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard ENEM - Análises</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-value { font-size: 2em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.9; }
        img { max-width: 100%; height: auto; margin: 20px 0; border: 1px solid #ddd; border-radius: 4px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #3498db; color: white; }
        tr:hover { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard ENEM - Análises (2009-2024)</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">16</div>
                <div class="stat-label">Anos de Dados</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">2,779</div>
                <div class="stat-label">Questões Totais</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">2009-2024</div>
                <div class="stat-label">Período</div>
            </div>
        </div>
        
        <h2>📈 Série Temporal</h2>
        <p>Evolução do número de questões por área de conhecimento ao longo dos anos.</p>
        <img src="serie_temporal_areas.png" alt="Série Temporal">
        
        <h2>📊 Dificuldade</h2>
        <p>Evolução da dificuldade média das questões ao longo dos anos.</p>
        <img src="dificuldade_temporal.png" alt="Dificuldade Temporal">
        
        <h2>🔗 Similaridade entre Provas</h2>
        <p>Matriz de similaridade entre provas de diferentes anos.</p>
        <img src="heatmap_similaridade_cosseno.png" alt="Similaridade">
        
        <h2>📝 Notas</h2>
        <ul>
            <li>Dados históricos de 2009 a 2024</li>
            <li>Análises semânticas e lexicais</li>
            <li>Modelos preditivos implementados</li>
            <li>Validação com dados reais recomendada</li>
        </ul>
    </div>
</body>
</html>
"""
        
        arquivo = output_dir / "dashboard.html"
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✅ Dashboard HTML salvo: {arquivo.name}")
        return True
    
    except Exception as e:
        print(f"  ❌ Erro ao criar dashboard: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 GERAÇÃO DE VISUALIZAÇÕES - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    analises_dir = project_root / "data" / "analises"
    visualizacoes_dir = project_root / "reports" / "visualizacoes"
    visualizacoes_dir.mkdir(parents=True, exist_ok=True)
    
    # Carregar dados
    print("📥 Carregando dados de análises...")
    dados = carregar_dados_analises(analises_dir)
    
    if not dados:
        print("❌ Nenhum dado de análise encontrado")
        print("   Execute primeiro as análises anteriores")
        return
    
    print("✅ Dados carregados")
    print()
    
    # Criar visualizações
    print("🎨 Criando visualizações...")
    
    # Série temporal
    if 'serie_temporal' in dados:
        print("  📈 Criando gráfico de série temporal...")
        criar_grafico_serie_temporal(dados['serie_temporal'], visualizacoes_dir)
    
    # Dificuldade
    if 'dificuldade' in dados:
        print("  📊 Criando gráfico de dificuldade...")
        criar_grafico_dificuldade(dados['dificuldade'], visualizacoes_dir)
    
    # Similaridade
    if 'similaridade' in dados:
        print("  🔗 Criando heatmap de similaridade...")
        criar_heatmap_similaridade(dados['similaridade'], visualizacoes_dir)
    
    # Dashboard HTML
    print("  🌐 Criando dashboard HTML...")
    criar_dashboard_html(dados, visualizacoes_dir)
    
    print()
    print("=" * 70)
    print("✅ VISUALIZAÇÕES GERADAS")
    print("=" * 70)
    print(f"\n📁 Visualizações salvas em: {visualizacoes_dir}")
    print(f"\n💡 Abra dashboard.html no navegador para ver o dashboard completo")

if __name__ == "__main__":
    main()


