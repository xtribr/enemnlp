#!/usr/bin/env python3
"""
Gera gráfico de evolução da dificuldade incluindo 2025
"""
import json
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_dificuldade():
    """Carrega dados de dificuldade"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "analises" / "dificuldade_estatisticas.json"
    
    if not arquivo.exists():
        print("❌ Arquivo de dificuldade não encontrado")
        print("   Execute primeiro: 08_heuristica_dificuldade.py")
        return None
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Converter para DataFrame
    anos = []
    medias = []
    
    for ano, stats in sorted(dados.items()):
        anos.append(int(ano))
        medias.append(stats.get('media_dificuldade', 0))
    
    # Adicionar 2025 se disponível
    arquivo_2025 = project_root / "data" / "processed" / "enem_2025_completo.jsonl"
    if arquivo_2025.exists():
        # Calcular dificuldade média de 2025
        questoes_2025 = []
        with open(arquivo_2025, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes_2025.append(json.loads(line))
        
        if questoes_2025:
            # Calcular dificuldade média simples (baseado em comprimento)
            dificuldades_2025 = []
            for q in questoes_2025:
                texto = f"{q.get('context', '')} {q.get('question', '')}"
                comprimento = len(texto)
                # Normalizar para escala similar (0-100)
                dificuldade = min(comprimento / 50, 100)
                dificuldades_2025.append(dificuldade)
            
            if dificuldades_2025:
                media_2025 = sum(dificuldades_2025) / len(dificuldades_2025)
                anos.append(2025)
                medias.append(media_2025)
                print(f"✅ Dificuldade 2025 calculada: {media_2025:.2f}")
    
    df = pd.DataFrame({'ano': anos, 'dificuldade_media': medias})
    return df

def gerar_grafico(df):
    """Gera gráfico de evolução da dificuldade"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        
        plt.figure(figsize=(14, 8))
        
        # Plotar linha
        plt.plot(df['ano'], df['dificuldade_media'], 
                marker='o', linewidth=2.5, markersize=8, 
                color='#2c3e50', label='Dificuldade Média')
        
        # Preencher área
        plt.fill_between(df['ano'], df['dificuldade_media'], 
                        alpha=0.3, color='#3498db')
        
        # Destacar 2025
        if 2025 in df['ano'].values:
            idx_2025 = df[df['ano'] == 2025].index[0]
            plt.plot(df.loc[idx_2025, 'ano'], df.loc[idx_2025, 'dificuldade_media'],
                    marker='s', markersize=12, color='#e74c3c', 
                    label='2025 (Novo)', zorder=5)
        
        plt.xlabel('Ano', fontsize=14, fontweight='bold')
        plt.ylabel('Dificuldade Média', fontsize=14, fontweight='bold')
        plt.title('Evolução da Dificuldade Média das Questões do ENEM (2009-2025)', 
                 fontsize=16, fontweight='bold', pad=20)
        
        # Ajustar eixos
        plt.xlim(df['ano'].min() - 0.5, df['ano'].max() + 0.5)
        plt.ylim(0, max(df['dificuldade_media']) * 1.1)
        
        # Grid
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Legenda
        plt.legend(loc='best', fontsize=12)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Salvar
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / "reports" / "visualizacoes"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        arquivo = output_dir / "dificuldade_temporal_2009_2025.png"
        plt.savefig(arquivo, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Gráfico salvo em: {arquivo}")
        return True
    
    except ImportError:
        print("❌ matplotlib não instalado")
        print("   Instale com: pip install matplotlib")
        return False
    except Exception as e:
        print(f"❌ Erro ao gerar gráfico: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 GERAÇÃO DE GRÁFICO DE DIFICULDADE (2009-2025)")
    print("=" * 70)
    print()
    
    # Carregar dados
    print("📥 Carregando dados de dificuldade...")
    df = carregar_dificuldade()
    
    if df is None:
        return
    
    print(f"✅ {len(df)} anos carregados")
    print()
    
    # Estatísticas
    print("📊 Estatísticas:")
    print(f"   Período: {df['ano'].min()} - {df['ano'].max()}")
    print(f"   Dificuldade média geral: {df['dificuldade_media'].mean():.2f}")
    print(f"   Dificuldade mínima: {df['dificuldade_media'].min():.2f} ({df.loc[df['dificuldade_media'].idxmin(), 'ano']})")
    print(f"   Dificuldade máxima: {df['dificuldade_media'].max():.2f} ({df.loc[df['dificuldade_media'].idxmax(), 'ano']})")
    print()
    
    # Gerar gráfico
    print("🎨 Gerando gráfico...")
    if gerar_grafico(df):
        print()
        print("=" * 70)
        print("✅ GRÁFICO GERADO COM SUCESSO")
        print("=" * 70)

if __name__ == "__main__":
    main()


