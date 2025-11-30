#!/usr/bin/env python3
"""
📊 Análise Detalhada de Similaridade Semântica - ENEM

Analisa similaridades semânticas:
- Dentro da mesma área (intra-área)
- Entre áreas correlatas (inter-área)
- Comparação entre diferentes tipos de similaridade
"""
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from typing import Dict, List, Tuple
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_embeddings(embeddings_dir: Path) -> Dict[int, np.ndarray]:
    """Carrega embeddings salvos"""
    embeddings_por_ano = {}
    
    for arquivo_emb in sorted(embeddings_dir.glob("embeddings_*.npy")):
        try:
            ano = int(arquivo_emb.stem.split('_')[1])
            embeddings_por_ano[ano] = np.load(arquivo_emb)
        except (ValueError, IndexError):
            continue
    
    return embeddings_por_ano

def carregar_questoes_por_ano_area(processed_dir: Path) -> Dict[int, Dict[str, List[Dict]]]:
    """Carrega questões agrupadas por ano e área"""
    questoes_por_ano_area = defaultdict(lambda: defaultdict(list))
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        
        for questao in questoes:
            area = questao.get('area', 'desconhecida')
            questoes_por_ano_area[ano][area].append(questao)
    
    return questoes_por_ano_area

def calcular_embedding_medio_por_area_ano(embeddings_por_ano: Dict[int, np.ndarray],
                                          questoes_por_ano_area: Dict[int, Dict[str, List[Dict]]]) -> Dict[int, Dict[str, np.ndarray]]:
    """Calcula embedding médio por área para cada ano"""
    embeddings_por_ano_area = {}
    
    areas_map = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    for ano in embeddings_por_ano.keys():
        if ano not in questoes_por_ano_area:
            continue
        
        embeddings_ano = embeddings_por_ano[ano]
        questoes_ano = questoes_por_ano_area[ano]
        
        embeddings_por_ano_area[ano] = {}
        
        # Índice para mapear questão -> embedding
        idx_questao = 0
        
        for area_codigo, area_nome in areas_map.items():
            questoes_area = questoes_ano.get(area_codigo, [])
            
            if questoes_area and idx_questao + len(questoes_area) <= len(embeddings_ano):
                embeddings_area = embeddings_ano[idx_questao:idx_questao + len(questoes_area)]
                
                if len(embeddings_area) > 0:
                    embedding_medio = np.mean(embeddings_area, axis=0)
                    embeddings_por_ano_area[ano][area_nome] = embedding_medio
                
                idx_questao += len(questoes_area)
    
    return embeddings_por_ano_area

def calcular_similaridade_intra_area(embeddings_por_ano_area: Dict[int, Dict[str, np.ndarray]],
                                     area: str) -> Dict[str, float]:
    """Calcula similaridade semântica dentro da mesma área entre diferentes anos"""
    anos_com_area = sorted([a for a in embeddings_por_ano_area.keys() 
                           if area in embeddings_por_ano_area[a]])
    
    if len(anos_com_area) < 2:
        return {}
    
    similaridades = {}
    
    for i, ano1 in enumerate(anos_com_area):
        for ano2 in anos_com_area[i+1:]:
            emb1 = embeddings_por_ano_area[ano1][area].reshape(1, -1)
            emb2 = embeddings_por_ano_area[ano2][area].reshape(1, -1)
            sim = cosine_similarity(emb1, emb2)[0][0]
            similaridades[f"{ano1}-{ano2}"] = float(sim)
    
    return similaridades

def calcular_similaridade_inter_area(embeddings_por_ano_area: Dict[int, Dict[str, np.ndarray]],
                                    area1: str, area2: str) -> Dict[str, float]:
    """Calcula similaridade semântica entre duas áreas diferentes"""
    anos_comum = sorted([a for a in embeddings_por_ano_area.keys()
                         if area1 in embeddings_por_ano_area[a] and 
                         area2 in embeddings_por_ano_area[a]])
    
    if len(anos_comum) == 0:
        return {}
    
    similaridades = {}
    
    for ano in anos_comum:
        emb1 = embeddings_por_ano_area[ano][area1].reshape(1, -1)
        emb2 = embeddings_por_ano_area[ano][area2].reshape(1, -1)
        sim = cosine_similarity(emb1, emb2)[0][0]
        similaridades[str(ano)] = float(sim)
    
    return similaridades

def gerar_analise_comparativa(embeddings_por_ano_area: Dict[int, Dict[str, np.ndarray]]):
    """Gera análise comparativa de similaridades"""
    
    areas = ['Linguagens', 'Humanas', 'Natureza', 'Matemática']
    
    print("=" * 70)
    print("📊 ANÁLISE DE SIMILARIDADE SEMÂNTICA DETALHADA")
    print("=" * 70)
    print()
    
    # 1. Similaridade intra-área (dentro da mesma área)
    print("🔍 1. SIMILARIDADE INTRA-ÁREA (dentro da mesma área)")
    print("-" * 70)
    
    similaridades_intra = {}
    for area in areas:
        sims = calcular_similaridade_intra_area(embeddings_por_ano_area, area)
        if sims:
            similaridades_intra[area] = sims
            media = np.mean(list(sims.values()))
            min_sim = np.min(list(sims.values()))
            max_sim = np.max(list(sims.values()))
            print(f"\n{area}:")
            print(f"  Média: {media:.3f}")
            print(f"  Min: {min_sim:.3f}, Max: {max_sim:.3f}")
            print(f"  Pares analisados: {len(sims)}")
    
    print()
    
    # 2. Similaridade inter-área (entre áreas diferentes)
    print("🔗 2. SIMILARIDADE INTER-ÁREA (entre áreas diferentes)")
    print("-" * 70)
    
    # Áreas correlatas (baseado na matriz de correlação)
    pares_correlatos = [
        ('Linguagens', 'Humanas'),      # 0.882 - MUITO ALTA
        ('Natureza', 'Matemática'),     # 0.701 - ALTA
        ('Humanas', 'Natureza'),        # 0.622 - MÉDIA-ALTA
        ('Humanas', 'Matemática'),      # 0.556 - MÉDIA
        ('Linguagens', 'Natureza'),    # 0.578 - MÉDIA
        ('Linguagens', 'Matemática'),  # 0.514 - BAIXA
    ]
    
    similaridades_inter = {}
    for area1, area2 in pares_correlatos:
        sims = calcular_similaridade_inter_area(embeddings_por_ano_area, area1, area2)
        if sims:
            similaridades_inter[f"{area1}-{area2}"] = sims
            media = np.mean(list(sims.values()))
            min_sim = np.min(list(sims.values()))
            max_sim = np.max(list(sims.values()))
            print(f"\n{area1} ↔ {area2}:")
            print(f"  Média: {media:.3f}")
            print(f"  Min: {min_sim:.3f}, Max: {max_sim:.3f}")
            print(f"  Anos analisados: {len(sims)}")
    
    print()
    
    # 3. Comparação: Intra-área vs Inter-área
    print("📊 3. COMPARAÇÃO: INTRA-ÁREA vs INTER-ÁREA")
    print("-" * 70)
    
    # Média de similaridade intra-área
    todas_sims_intra = []
    for area, sims in similaridades_intra.items():
        todas_sims_intra.extend(sims.values())
    
    media_intra = np.mean(todas_sims_intra) if todas_sims_intra else 0
    
    # Média de similaridade inter-área (correlatas)
    todas_sims_inter_correlatas = []
    for par, sims in similaridades_inter.items():
        todas_sims_inter_correlatas.extend(sims.values())
    
    media_inter_correlatas = np.mean(todas_sims_inter_correlatas) if todas_sims_inter_correlatas else 0
    
    print(f"\nSimilaridade Intra-Área (média): {media_intra:.3f}")
    print(f"  → Consistência temporal dentro da mesma área")
    print()
    print(f"Similaridade Inter-Área Correlatas (média): {media_inter_correlatas:.3f}")
    print(f"  → Similaridade entre áreas relacionadas")
    print()
    
    if media_intra > media_inter_correlatas:
        diferenca = media_intra - media_inter_correlatas
        print(f"✅ Similaridade intra-área é {diferenca:.3f} pontos MAIOR")
        print(f"   → Questões da mesma área são mais similares entre si")
        print(f"   → Cada área mantém identidade semântica própria")
    else:
        diferenca = media_inter_correlatas - media_intra
        print(f"⚠️  Similaridade inter-área correlatas é {diferenca:.3f} pontos MAIOR")
    
    print()
    
    # 4. Análise por área específica
    print("📋 4. ANÁLISE POR ÁREA")
    print("-" * 70)
    
    for area in areas:
        if area not in similaridades_intra:
            continue
        
        print(f"\n{area}:")
        
        # Similaridade intra-área
        sims_intra = list(similaridades_intra[area].values())
        media_intra_area = np.mean(sims_intra)
        print(f"  Intra-área: {media_intra_area:.3f} (consistência temporal)")
        
        # Similaridade com áreas correlatas
        for area_correlata in areas:
            if area_correlata == area:
                continue
            
            par_key1 = f"{area}-{area_correlata}"
            par_key2 = f"{area_correlata}-{area}"
            
            if par_key1 in similaridades_inter:
                sims = list(similaridades_inter[par_key1].values())
                media_inter = np.mean(sims)
                print(f"  ↔ {area_correlata}: {media_inter:.3f}")
            elif par_key2 in similaridades_inter:
                sims = list(similaridades_inter[par_key2].values())
                media_inter = np.mean(sims)
                print(f"  ↔ {area_correlata}: {media_inter:.3f}")
    
    print()
    
    # 5. Gerar visualizações comparativas
    print("🎨 Gerando visualizações comparativas...")
    
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: Comparação Intra vs Inter
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Preparar dados
    dados_comparacao = []
    
    # Intra-área
    for area, sims in similaridades_intra.items():
        media = np.mean(list(sims.values()))
        dados_comparacao.append({
            'Tipo': 'Intra-Área',
            'Área': area,
            'Similaridade': media
        })
    
    # Inter-área (apenas correlatas mais altas)
    pares_altos = [('Linguagens', 'Humanas'), ('Natureza', 'Matemática')]
    for area1, area2 in pares_altos:
        par_key1 = f"{area1}-{area2}"
        par_key2 = f"{area2}-{area1}"
        
        if par_key1 in similaridades_inter:
            sims = list(similaridades_inter[par_key1].values())
            media = np.mean(sims)
            dados_comparacao.append({
                'Tipo': f'Inter-Área ({area1}↔{area2})',
                'Área': f'{area1}-{area2}',
                'Similaridade': media
            })
        elif par_key2 in similaridades_inter:
            sims = list(similaridades_inter[par_key2].values())
            media = np.mean(sims)
            dados_comparacao.append({
                'Tipo': f'Inter-Área ({area1}↔{area2})',
                'Área': f'{area1}-{area2}',
                'Similaridade': media
            })
    
    df_comparacao = pd.DataFrame(dados_comparacao)
    
    # Criar gráfico de barras
    cores_intra = {'Linguagens': '#3498db', 'Humanas': '#e74c3c', 
                   'Natureza': '#27ae60', 'Matemática': '#f39c12'}
    cores_inter = {'Linguagens-Humanas': '#9b59b6', 'Natureza-Matemática': '#16a085'}
    
    tipos = df_comparacao['Tipo'].unique()
    x_pos = np.arange(len(df_comparacao))
    
    cores = []
    for _, row in df_comparacao.iterrows():
        if 'Intra-Área' in row['Tipo']:
            cores.append(cores_intra.get(row['Área'], '#95a5a6'))
        else:
            cores.append(cores_inter.get(row['Área'], '#95a5a6'))
    
    bars = ax.barh(x_pos, df_comparacao['Similaridade'], color=cores, alpha=0.8)
    ax.set_yticks(x_pos)
    ax.set_yticklabels(df_comparacao['Área'], fontsize=10)
    ax.set_xlabel('Similaridade Semântica', fontsize=12, fontweight='bold')
    ax.set_title('Comparação: Similaridade Intra-Área vs Inter-Área Correlatas', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(0.5, 1.0)
    
    # Adicionar valores nas barras
    for i, (bar, val) in enumerate(zip(bars, df_comparacao['Similaridade'])):
        ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=9)
    
    plt.tight_layout()
    arquivo1 = output_dir / "comparacao_intra_inter_area.png"
    plt.savefig(arquivo1, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ {arquivo1.name}")
    
    # Gráfico 2: Matriz de similaridade intra-área
    areas_com_dados = [a for a in areas if a in similaridades_intra]
    if len(areas_com_dados) > 1:
        # Criar matriz de similaridade média intra-área
        matriz_intra = np.eye(len(areas_com_dados))
        
        # Preencher com médias de similaridade intra-área
        for i, area in enumerate(areas_com_dados):
            sims = list(similaridades_intra[area].values())
            if sims:
                # Usar média como valor representativo
                matriz_intra[i][i] = np.mean(sims)
        
        # Para comparação, adicionar similaridade inter-área correlatas
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Criar matriz combinada
        matriz_combinada = np.zeros((len(areas_com_dados), len(areas_com_dados)))
        
        for i, area1 in enumerate(areas_com_dados):
            for j, area2 in enumerate(areas_com_dados):
                if i == j:
                    # Diagonal: similaridade intra-área
                    sims = list(similaridades_intra[area1].values())
                    matriz_combinada[i][j] = np.mean(sims) if sims else 0
                else:
                    # Fora da diagonal: similaridade inter-área
                    par_key1 = f"{area1}-{area2}"
                    par_key2 = f"{area2}-{area1}"
                    
                    if par_key1 in similaridades_inter:
                        sims = list(similaridades_inter[par_key1].values())
                        matriz_combinada[i][j] = np.mean(sims) if sims else 0
                    elif par_key2 in similaridades_inter:
                        sims = list(similaridades_inter[par_key2].values())
                        matriz_combinada[i][j] = np.mean(sims) if sims else 0
        
        df_matriz = pd.DataFrame(matriz_combinada, index=areas_com_dados, columns=areas_com_dados)
        
        sns.heatmap(df_matriz, annot=True, fmt='.3f', cmap='RdYlBu_r', 
                   center=0.7, square=True, linewidths=0.5, 
                   cbar_kws={"shrink": 0.8}, vmin=0.5, vmax=1.0, ax=ax)
        
        ax.set_title('Matriz de Similaridade Semântica\n(Diagonal: Intra-Área | Fora: Inter-Área)',
                    fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        arquivo2 = output_dir / "matriz_similaridade_intra_inter.png"
        plt.savefig(arquivo2, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ {arquivo2.name}")
    
    # Salvar dados
    dados_salvar = {
        'similaridade_intra_area': {
            area: {
                'media': float(np.mean(list(sims.values()))),
                'min': float(np.min(list(sims.values()))),
                'max': float(np.max(list(sims.values()))),
                'valores': sims
            }
            for area, sims in similaridades_intra.items()
        },
        'similaridade_inter_area': {
            par: {
                'media': float(np.mean(list(sims.values()))),
                'min': float(np.min(list(sims.values()))),
                'max': float(np.max(list(sims.values()))),
                'valores': sims
            }
            for par, sims in similaridades_inter.items()
        },
        'comparacao': {
            'media_intra_area': float(media_intra),
            'media_inter_area_correlatas': float(media_inter_correlatas),
            'diferenca': float(media_intra - media_inter_correlatas)
        }
    }
    
    arquivo_dados = output_dir / "analise_similaridade_detalhada.json"
    with open(arquivo_dados, 'w', encoding='utf-8') as f:
        json.dump(dados_salvar, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ {arquivo_dados.name}")
    print()
    
    return similaridades_intra, similaridades_inter

def main():
    """Função principal"""
    project_root = Path(__file__).parent.parent.parent
    embeddings_dir = project_root / "data" / "embeddings"
    processed_dir = project_root / "data" / "processed"
    
    # Carregar dados
    print("📥 Carregando embeddings...")
    embeddings_por_ano = carregar_embeddings(embeddings_dir)
    
    if not embeddings_por_ano:
        print("❌ Nenhum embedding encontrado")
        return
    
    print(f"✅ {len(embeddings_por_ano)} anos carregados")
    print()
    
    print("📥 Carregando questões...")
    questoes_por_ano_area = carregar_questoes_por_ano_area(processed_dir)
    print(f"✅ Questões carregadas")
    print()
    
    print("🔄 Calculando embeddings médios por área...")
    embeddings_por_ano_area = calcular_embedding_medio_por_area_ano(
        embeddings_por_ano, questoes_por_ano_area
    )
    print(f"✅ Embeddings médios calculados")
    print()
    
    # Gerar análise
    similaridades_intra, similaridades_inter = gerar_analise_comparativa(embeddings_por_ano_area)
    
    print("=" * 70)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()

