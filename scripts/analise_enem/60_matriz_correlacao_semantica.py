#!/usr/bin/env python3
"""
📊 Matriz de Correlação Semântica - ENEM

Gera matrizes de correlação semântica entre áreas, anos e combinações.
Usa embeddings semânticos para calcular similaridade.
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
    
    # Carregar índice
    indice_file = embeddings_dir / "indice_embeddings.json"
    if indice_file.exists():
        with open(indice_file, 'r', encoding='utf-8') as f:
            indice = json.load(f)
        
        for ano_str, info in indice.items():
            # Pular chaves que não são anos
            if not ano_str.isdigit():
                continue
            try:
                ano = int(ano_str)
                arquivo_emb = embeddings_dir / info['arquivo']
                if arquivo_emb.exists():
                    embeddings_por_ano[ano] = np.load(arquivo_emb)
                    print(f"  ✅ {ano}: {embeddings_por_ano[ano].shape}")
            except (ValueError, KeyError) as e:
                continue
    
    # Também tentar carregar diretamente dos arquivos .npy
    for arquivo_emb in sorted(embeddings_dir.glob("embeddings_*.npy")):
        try:
            ano = int(arquivo_emb.stem.split('_')[1])
            if ano not in embeddings_por_ano:
                embeddings_por_ano[ano] = np.load(arquivo_emb)
                print(f"  ✅ {ano}: {embeddings_por_ano[ano].shape} (carregado diretamente)")
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
        
        # Agrupar por área
        for questao in questoes:
            area = questao.get('area', 'desconhecida')
            questoes_por_ano_area[ano][area].append(questao)
    
    return questoes_por_ano_area

def calcular_embedding_medio_por_area(embeddings_por_ano: Dict[int, np.ndarray],
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
                # Extrair embeddings das questões desta área
                embeddings_area = embeddings_ano[idx_questao:idx_questao + len(questoes_area)]
                
                # Calcular embedding médio
                if len(embeddings_area) > 0:
                    embedding_medio = np.mean(embeddings_area, axis=0)
                    embeddings_por_ano_area[ano][area_nome] = embedding_medio
                
                idx_questao += len(questoes_area)
    
    return embeddings_por_ano_area

def calcular_correlacao_entre_areas(embeddings_por_ano_area: Dict[int, Dict[str, np.ndarray]]) -> pd.DataFrame:
    """Calcula correlação semântica entre áreas ao longo dos anos"""
    areas = ['Linguagens', 'Humanas', 'Natureza', 'Matemática']
    
    # Calcular embedding médio por área (média de todos os anos)
    embeddings_medio_por_area = {}
    for area in areas:
        embeddings_area = []
        for ano in embeddings_por_ano_area.keys():
            if area in embeddings_por_ano_area[ano]:
                embeddings_area.append(embeddings_por_ano_area[ano][area])
        
        if embeddings_area:
            embeddings_medio_por_area[area] = np.mean(embeddings_area, axis=0)
    
    # Calcular matriz de correlação (similaridade cosseno)
    matriz_correlacao = np.zeros((len(areas), len(areas)))
    
    for i, area1 in enumerate(areas):
        for j, area2 in enumerate(areas):
            if area1 in embeddings_medio_por_area and area2 in embeddings_medio_por_area:
                # Similaridade cosseno
                emb1 = embeddings_medio_por_area[area1].reshape(1, -1)
                emb2 = embeddings_medio_por_area[area2].reshape(1, -1)
                similaridade = cosine_similarity(emb1, emb2)[0][0]
                matriz_correlacao[i][j] = similaridade
    
    df = pd.DataFrame(matriz_correlacao, index=areas, columns=areas)
    return df

def calcular_correlacao_entre_anos(embeddings_por_ano: Dict[int, np.ndarray]) -> pd.DataFrame:
    """Calcula correlação semântica entre anos"""
    anos = sorted(embeddings_por_ano.keys())
    
    # Calcular embedding médio por ano
    embeddings_medio_por_ano = {}
    for ano in anos:
        embeddings_ano = embeddings_por_ano[ano]
        embeddings_medio_por_ano[ano] = np.mean(embeddings_ano, axis=0)
    
    # Calcular matriz de correlação
    matriz_correlacao = np.zeros((len(anos), len(anos)))
    
    for i, ano1 in enumerate(anos):
        for j, ano2 in enumerate(anos):
            emb1 = embeddings_medio_por_ano[ano1].reshape(1, -1)
            emb2 = embeddings_medio_por_ano[ano2].reshape(1, -1)
            similaridade = cosine_similarity(emb1, emb2)[0][0]
            matriz_correlacao[i][j] = similaridade
    
    df = pd.DataFrame(matriz_correlacao, index=anos, columns=anos)
    return df

def calcular_correlacao_area_ano(embeddings_por_ano_area: Dict[int, Dict[str, np.ndarray]],
                                 area: str) -> pd.DataFrame:
    """Calcula correlação semântica de uma área específica entre anos"""
    anos = sorted([a for a in embeddings_por_ano_area.keys() if area in embeddings_por_ano_area[a]])
    
    if len(anos) < 2:
        return None
    
    # Calcular matriz de correlação
    matriz_correlacao = np.zeros((len(anos), len(anos)))
    
    for i, ano1 in enumerate(anos):
        for j, ano2 in enumerate(anos):
            emb1 = embeddings_por_ano_area[ano1][area].reshape(1, -1)
            emb2 = embeddings_por_ano_area[ano2][area].reshape(1, -1)
            similaridade = cosine_similarity(emb1, emb2)[0][0]
            matriz_correlacao[i][j] = similaridade
    
    df = pd.DataFrame(matriz_correlacao, index=anos, columns=anos)
    return df

def gerar_heatmap(df: pd.DataFrame, titulo: str, arquivo: Path, 
                 cmap: str = 'RdYlBu_r', vmin: float = None, vmax: float = None):
    """Gera heatmap de correlação"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Calcular limites se não fornecidos
    if vmin is None:
        vmin = df.values.min()
    if vmax is None:
        vmax = df.values.max()
    
    # Criar heatmap
    sns.heatmap(df, annot=True, fmt='.3f', cmap=cmap, center=0.5,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                vmin=vmin, vmax=vmax, ax=ax)
    
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Heatmap salvo: {arquivo}")

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 MATRIZ DE CORRELAÇÃO SEMÂNTICA - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    embeddings_dir = project_root / "data" / "embeddings"
    processed_dir = project_root / "data" / "processed"
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Carregar embeddings
    print("📥 Carregando embeddings...")
    if not embeddings_dir.exists():
        print("❌ Diretório de embeddings não encontrado")
        print("   Execute primeiro: python scripts/analise_enem/04_gerar_embeddings.py")
        return
    
    embeddings_por_ano = carregar_embeddings(embeddings_dir)
    
    if not embeddings_por_ano:
        print("❌ Nenhum embedding encontrado")
        print("   Execute primeiro: python scripts/analise_enem/04_gerar_embeddings.py")
        return
    
    print(f"✅ {len(embeddings_por_ano)} anos com embeddings carregados")
    print()
    
    # 2. Carregar questões
    print("📥 Carregando questões...")
    questoes_por_ano_area = carregar_questoes_por_ano_area(processed_dir)
    print(f"✅ Questões carregadas para {len(questoes_por_ano_area)} anos")
    print()
    
    # 3. Calcular embeddings médios por área
    print("🔄 Calculando embeddings médios por área...")
    embeddings_por_ano_area = calcular_embedding_medio_por_area(
        embeddings_por_ano, questoes_por_ano_area
    )
    print(f"✅ Embeddings médios calculados para {len(embeddings_por_ano_area)} anos")
    print()
    
    # 4. Matriz de correlação entre áreas
    print("📊 Calculando correlação entre áreas...")
    df_areas = calcular_correlacao_entre_areas(embeddings_por_ano_area)
    print("✅ Matriz de correlação entre áreas calculada")
    print()
    print("Matriz de Correlação Semântica entre Áreas:")
    print(df_areas.to_string())
    print()
    
    # 5. Matriz de correlação entre anos
    print("📊 Calculando correlação entre anos...")
    df_anos = calcular_correlacao_entre_anos(embeddings_por_ano)
    print("✅ Matriz de correlação entre anos calculada")
    print()
    
    # 6. Matriz de correlação por área entre anos
    print("📊 Calculando correlação por área entre anos...")
    areas = ['Linguagens', 'Humanas', 'Natureza', 'Matemática']
    dfs_area_ano = {}
    
    for area in areas:
        df_area = calcular_correlacao_area_ano(embeddings_por_ano_area, area)
        if df_area is not None:
            dfs_area_ano[area] = df_area
            print(f"  ✅ {area}: {len(df_area)} anos")
    
    print()
    
    # 7. Gerar visualizações
    print("🎨 Gerando visualizações...")
    
    # Heatmap 1: Correlação entre áreas
    arquivo1 = output_dir / "matriz_correlacao_areas.png"
    gerar_heatmap(df_areas, 
                 "Matriz de Correlação Semântica entre Áreas - ENEM",
                 arquivo1, cmap='RdYlBu_r', vmin=0.5, vmax=1.0)
    
    # Heatmap 2: Correlação entre anos
    arquivo2 = output_dir / "matriz_correlacao_anos.png"
    gerar_heatmap(df_anos,
                 "Matriz de Correlação Semântica entre Anos - ENEM (2009-2025)",
                 arquivo2, cmap='RdYlBu_r', vmin=0.7, vmax=1.0)
    
    # Heatmap 3: Correlação por área entre anos
    for area, df_area in dfs_area_ano.items():
        arquivo3 = output_dir / f"matriz_correlacao_{area.lower()}_anos.png"
        gerar_heatmap(df_area,
                     f"Matriz de Correlação Semântica - {area} entre Anos",
                     arquivo3, cmap='RdYlBu_r', vmin=0.7, vmax=1.0)
    
    # 8. Salvar dados
    print("\n💾 Salvando dados...")
    dados_file = output_dir / "matrizes_correlacao_semantica.json"
    
    dados_salvar = {
        'correlacao_entre_areas': df_areas.to_dict(),
        'correlacao_entre_anos': df_anos.to_dict(),
        'correlacao_por_area_anos': {
            area: df.to_dict() for area, df in dfs_area_ano.items()
        }
    }
    
    with open(dados_file, 'w', encoding='utf-8') as f:
        json.dump(dados_salvar, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ Dados salvos: {dados_file}")
    print()
    
    # 9. Estatísticas
    print("=" * 70)
    print("📊 ESTATÍSTICAS DE CORRELAÇÃO")
    print("=" * 70)
    print()
    
    print("Correlação entre Áreas (média):")
    # Calcular média (excluindo diagonal)
    mask = ~np.eye(len(df_areas), dtype=bool)
    media_areas = df_areas.values[mask].mean()
    print(f"  Média: {media_areas:.3f}")
    print(f"  Min: {df_areas.values[mask].min():.3f}")
    print(f"  Max: {df_areas.values[mask].max():.3f}")
    print()
    
    print("Correlação entre Anos (média):")
    mask_anos = ~np.eye(len(df_anos), dtype=bool)
    media_anos = df_anos.values[mask_anos].mean()
    print(f"  Média: {media_anos:.3f}")
    print(f"  Min: {df_anos.values[mask_anos].min():.3f}")
    print(f"  Max: {df_anos.values[mask_anos].max():.3f}")
    print()
    
    print("=" * 70)
    print("✅ MATRIZES DE CORRELAÇÃO GERADAS")
    print("=" * 70)
    print()
    print("📁 Arquivos gerados:")
    print(f"   {arquivo1.name}")
    print(f"   {arquivo2.name}")
    for area in dfs_area_ano.keys():
        print(f"   matriz_correlacao_{area.lower()}_anos.png")
    print(f"   {dados_file.name}")

if __name__ == "__main__":
    main()

