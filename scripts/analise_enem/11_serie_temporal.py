#!/usr/bin/env python3
"""
Análise de Série Temporal do ENEM (2009-2024)

Prepara dados para análise temporal e identifica padrões ao longo dos anos.
"""
import json
import sys
from pathlib import Path
from typing import Dict, List
import pandas as pd
import numpy as np
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_dados_processados(processed_dir: Path) -> Dict[int, List[Dict]]:
    """Carrega todos os dados processados"""
    dados = {}
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        dados[ano] = questoes
    return dados

def criar_serie_temporal_por_area(dados: Dict[int, List[Dict]]) -> pd.DataFrame:
    """Cria série temporal agregada por área de conhecimento"""
    series_data = []
    
    areas = ['languages', 'human-sciences', 'natural-sciences', 'mathematics']
    
    for ano in sorted(dados.keys()):
        questoes_ano = dados[ano]
        
        # Contar por área
        contagem_por_area = defaultdict(int)
        for questao in questoes_ano:
            area = questao.get('area', 'desconhecida')
            if area in areas:
                contagem_por_area[area] += 1
        
        # Adicionar ao DataFrame
        row = {'ano': ano, 'total': len(questoes_ano)}
        for area in areas:
            row[area] = contagem_por_area[area]
        series_data.append(row)
    
    return pd.DataFrame(series_data)

def calcular_metricas_temporais(dados: Dict[int, List[Dict]]) -> pd.DataFrame:
    """Calcula métricas temporais das questões"""
    metricas = []
    
    for ano in sorted(dados.keys()):
        questoes = dados[ano]
        
        if not questoes:
            continue
        
        # Métricas básicas
        tamanhos_questao = [len(q.get('question', '')) for q in questoes]
        tamanhos_contexto = [len(q.get('context', '')) for q in questoes]
        questoes_com_imagens = sum(1 for q in questoes if q.get('has_images') or q.get('context_images'))
        
        metricas.append({
            'ano': ano,
            'total_questoes': len(questoes),
            'tamanho_medio_questao': sum(tamanhos_questao) / len(tamanhos_questao) if tamanhos_questao else 0,
            'tamanho_medio_contexto': sum(tamanhos_contexto) / len(tamanhos_contexto) if tamanhos_contexto else 0,
            'percentual_imagens': (questoes_com_imagens / len(questoes) * 100) if questoes else 0,
            'questoes_com_imagens': questoes_com_imagens
        })
    
    return pd.DataFrame(metricas)

def identificar_tendencias(df: pd.DataFrame) -> Dict[str, any]:
    """Identifica tendências na série temporal"""
    tendencias = {}
    
    # Tendência de total de questões
    if 'total' in df.columns:
        df['total_diff'] = df['total'].diff()
        tendencias['total'] = {
            'media': df['total'].mean(),
            'tendencia': 'crescente' if df['total'].iloc[-1] > df['total'].iloc[0] else 'decrescente',
            'variacao_total': df['total'].iloc[-1] - df['total'].iloc[0],
            'variacao_percentual': ((df['total'].iloc[-1] - df['total'].iloc[0]) / df['total'].iloc[0] * 100) if df['total'].iloc[0] > 0 else 0
        }
    
    # Tendência por área
    areas = ['languages', 'human-sciences', 'natural-sciences', 'mathematics']
    for area in areas:
        if area in df.columns:
            tendencias[area] = {
                'media': df[area].mean(),
                'tendencia': 'crescente' if df[area].iloc[-1] > df[area].iloc[0] else 'decrescente',
                'variacao_total': df[area].iloc[-1] - df[area].iloc[0],
                'variacao_percentual': ((df[area].iloc[-1] - df[area].iloc[0]) / df[area].iloc[0] * 100) if df[area].iloc[0] > 0 else 0
            }
    
    return tendencias

def main():
    """Função principal"""
    print("=" * 70)
    print("📈 ANÁLISE DE SÉRIE TEMPORAL - ENEM (2009-2024)")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    analises_dir = project_root / "data" / "analises"
    analises_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Carregar dados
    print("📥 Carregando dados...")
    dados = carregar_dados_processados(processed_dir)
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # 2. Criar série temporal por área
    print("📊 Criando série temporal por área...")
    df_areas = criar_serie_temporal_por_area(dados)
    print("✅ Série temporal criada")
    print()
    
    # 3. Calcular métricas temporais
    print("📝 Calculando métricas temporais...")
    df_metricas = calcular_metricas_temporais(dados)
    print("✅ Métricas calculadas")
    print()
    
    # 4. Identificar tendências
    print("🔍 Identificando tendências...")
    tendencias = identificar_tendencias(df_areas)
    # Converter tipos numpy para Python nativos
    def converter_tipos(obj):
        if isinstance(obj, dict):
            return {k: converter_tipos(v) for k, v in obj.items()}
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    tendencias = converter_tipos(tendencias)
    print("✅ Tendências identificadas")
    print()
    
    # 5. Exibir resultados
    print("=" * 70)
    print("📊 SÉRIE TEMPORAL POR ÁREA")
    print("=" * 70)
    print(df_areas.to_string(index=False))
    print()
    
    print("=" * 70)
    print("📈 TENDÊNCIAS IDENTIFICADAS")
    print("=" * 70)
    for chave, valores in tendencias.items():
        if isinstance(valores, dict):
            print(f"\n{chave.upper()}:")
            print(f"  Média: {valores['media']:.1f}")
            print(f"  Tendência: {valores['tendencia']}")
            print(f"  Variação: {valores['variacao_total']:+.0f} ({valores['variacao_percentual']:+.1f}%)")
    print()
    
    # 6. Salvar resultados
    df_areas.to_csv(analises_dir / "serie_temporal_areas.csv", index=False)
    df_metricas.to_csv(analises_dir / "metricas_temporais.csv", index=False)
    
    with open(analises_dir / "tendencias.json", 'w', encoding='utf-8') as f:
        json.dump(tendencias, f, indent=2, ensure_ascii=False)
    
    print("💾 Resultados salvos em:")
    print(f"   - {analises_dir / 'serie_temporal_areas.csv'}")
    print(f"   - {analises_dir / 'metricas_temporais.csv'}")
    print(f"   - {analises_dir / 'tendencias.json'}")

if __name__ == "__main__":
    main()

