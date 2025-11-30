#!/usr/bin/env python3
"""
📊 Gráfico de Evolução do Projeto - Acurácia ENEM Matemática

Gera visualização da evolução da acurácia de 24% para 82%
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def gerar_grafico_evolucao():
    """Gera gráfico de evolução da acurácia do projeto"""
    
    # Dados da evolução
    etapas = [
        "Scripts\nCustomizados",
        "Sistema\nOficial (v1)",
        "Sistema\nOficial (v2)",
        "Meta\n90%"
    ]
    
    acuracias = [24, 71.11, 82.22, 90]
    cores = ['#e74c3c', '#f39c12', '#27ae60', '#3498db']
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Criar barras
    bars = ax.bar(etapas, acuracias, color=cores, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Adicionar valores nas barras
    for i, (bar, acc) in enumerate(zip(bars, acuracias)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc:.2f}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Adicionar linha de evolução
        if i > 0:
            x1 = bars[i-1].get_x() + bars[i-1].get_width()/2
            y1 = acuracias[i-1]
            x2 = bar.get_x() + bar.get_width()/2
            y2 = acuracias[i]
            ax.plot([x1, x2], [y1, y2], 'k--', linewidth=2, alpha=0.5, zorder=0)
    
    # Destacar benchmark atingido
    ax.axhline(y=82.22, color='#27ae60', linestyle='--', linewidth=2, 
               label='Benchmark Atingido (82.22%)', zorder=0)
    
    # Configurar eixos
    ax.set_ylabel('Acurácia (%)', fontsize=14, fontweight='bold')
    ax.set_title('📈 Evolução da Acurácia - ENEM Matemática 2024', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Adicionar anotações
    ax.annotate('+47.11 pp', xy=(1, 71.11), xytext=(1, 85),
                arrowprops=dict(arrowstyle='->', color='#f39c12', lw=2),
                fontsize=12, fontweight='bold', color='#f39c12')
    
    ax.annotate('+11.11 pp', xy=(2, 82.22), xytext=(2, 95),
                arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2),
                fontsize=12, fontweight='bold', color='#27ae60')
    
    ax.annotate('+58 pp total', xy=(2, 82.22), xytext=(0.5, 50),
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2),
                fontsize=14, fontweight='bold', color='#e74c3c',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))
    
    # Legenda
    ax.legend(loc='upper left', fontsize=12)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "evolucao_acuracia_projeto.png"
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico salvo em: {arquivo}")
    return arquivo

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 GERAÇÃO DE GRÁFICO DE EVOLUÇÃO DO PROJETO")
    print("=" * 70)
    print()
    
    print("🎨 Gerando gráfico...")
    arquivo = gerar_grafico_evolucao()
    
    print()
    print("=" * 70)
    print("✅ GRÁFICO GERADO COM SUCESSO")
    print("=" * 70)
    print(f"📁 Arquivo: {arquivo}")

if __name__ == "__main__":
    main()

