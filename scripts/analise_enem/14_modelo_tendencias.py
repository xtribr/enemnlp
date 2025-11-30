#!/usr/bin/env python3
"""
Modelo Preditivo de Tendências do ENEM

Usa série temporal completa (2009-2024) para prever tendências futuras.
"""
import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_serie_temporal(analises_dir: Path) -> pd.DataFrame:
    """Carrega série temporal processada"""
    csv_file = analises_dir / "serie_temporal_areas.csv"
    if not csv_file.exists():
        raise FileNotFoundError(f"Execute primeiro: 11_serie_temporal.py")
    return pd.read_csv(csv_file)

def modelo_regressao_linear(df: pd.DataFrame, coluna: str, anos_futuros: int = 3) -> Dict:
    """Modelo de regressão linear simples para prever tendências"""
    from sklearn.linear_model import LinearRegression
    
    # Preparar dados
    X = df[['ano']].values
    y = df[coluna].values
    
    # Treinar modelo
    model = LinearRegression()
    model.fit(X, y)
    
    # Prever anos futuros
    anos_futuros_array = np.array([[ano] for ano in range(df['ano'].max() + 1, df['ano'].max() + 1 + anos_futuros)])
    predicoes = model.predict(anos_futuros_array)
    
    # Calcular métricas
    y_pred = model.predict(X)
    r2 = model.score(X, y)
    mae = np.mean(np.abs(y - y_pred))
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    
    return {
        'modelo': 'Regressão Linear',
        'coeficiente': float(model.coef_[0]),
        'intercepto': float(model.intercept_),
        'r2': float(r2),
        'mae': float(mae),
        'rmse': float(rmse),
        'predicoes': {
            int(ano): float(pred) for ano, pred in zip(anos_futuros_array.flatten(), predicoes)
        }
    }

def modelo_media_movel(df: pd.DataFrame, coluna: str, window: int = 3, anos_futuros: int = 3) -> Dict:
    """Modelo de média móvel para prever tendências"""
    # Calcular média móvel
    df['media_movel'] = df[coluna].rolling(window=window, center=True).mean()
    
    # Prever usando última média móvel
    ultima_media = df['media_movel'].dropna().iloc[-1]
    tendencia = df[coluna].diff().mean()  # Tendência média
    
    predicoes = {}
    for i in range(1, anos_futuros + 1):
        ano = df['ano'].max() + i
        predicoes[int(ano)] = float(ultima_media + (tendencia * i))
    
    return {
        'modelo': 'Média Móvel',
        'window': window,
        'ultima_media': float(ultima_media),
        'tendencia_media': float(tendencia),
        'predicoes': predicoes
    }

def validar_modelo(df: pd.DataFrame, coluna: str, modelo_func, train_size: float = 0.8) -> Dict:
    """Valida modelo usando split temporal"""
    # Split temporal (não aleatório!)
    split_idx = int(len(df) * train_size)
    df_train = df.iloc[:split_idx].copy()
    df_test = df.iloc[split_idx:].copy()
    
    # Treinar no conjunto de treino
    if modelo_func == modelo_regressao_linear:
        resultado = modelo_func(df_train, coluna, anos_futuros=len(df_test))
    else:
        resultado = modelo_func(df_train, coluna, anos_futuros=len(df_test))
    
    # Avaliar no conjunto de teste
    predicoes = list(resultado['predicoes'].values())
    valores_reais = df_test[coluna].values
    
    if len(predicoes) == len(valores_reais):
        mae = np.mean(np.abs(valores_reais - predicoes))
        rmse = np.sqrt(np.mean((valores_reais - predicoes) ** 2))
        mape = np.mean(np.abs((valores_reais - predicoes) / valores_reais)) * 100
        
        resultado['validacao'] = {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape),
            'anos_teste': [int(ano) for ano in df_test['ano'].values]
        }
    
    return resultado

def gerar_predicoes_completas(df: pd.DataFrame, anos_futuros: int = 3) -> Dict:
    """Gera predições para todas as áreas"""
    predicoes = {}
    
    colunas = ['total', 'languages', 'human-sciences', 'natural-sciences', 'mathematics']
    
    for coluna in colunas:
        if coluna not in df.columns:
            continue
        
        print(f"  📊 Modelando {coluna}...")
        
        # Regressão Linear
        modelo_lr = validar_modelo(df, coluna, modelo_regressao_linear)
        
        # Média Móvel
        modelo_mm = validar_modelo(df, coluna, modelo_media_movel)
        
        # Predições futuras
        pred_lr = modelo_regressao_linear(df, coluna, anos_futuros)
        pred_mm = modelo_media_movel(df, coluna, window=3, anos_futuros=anos_futuros)
        
        predicoes[coluna] = {
            'regressao_linear': {
                'validacao': modelo_lr.get('validacao', {}),
                'r2': modelo_lr.get('r2', 0),
                'predicoes_futuras': pred_lr['predicoes']
            },
            'media_movel': {
                'validacao': modelo_mm.get('validacao', {}),
                'predicoes_futuras': pred_mm['predicoes']
            }
        }
    
    return predicoes

def main():
    """Função principal"""
    print("=" * 70)
    print("🔮 MODELO PREDITIVO DE TENDÊNCIAS - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    analises_dir = project_root / "data" / "analises"
    analises_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Carregar série temporal
    print("📥 Carregando série temporal...")
    df = carregar_serie_temporal(analises_dir)
    print(f"✅ {len(df)} anos carregados ({df['ano'].min()}-{df['ano'].max()})")
    print()
    
    # 2. Gerar predições
    print("🔮 Gerando predições (2025-2027)...")
    predicoes = gerar_predicoes_completas(df, anos_futuros=3)
    print("✅ Predições geradas")
    print()
    
    # 3. Exibir resultados
    print("=" * 70)
    print("📊 PREDIÇÕES PARA 2025-2027")
    print("=" * 70)
    
    for coluna, modelos in predicoes.items():
        print(f"\n{coluna.upper()}:")
        print(f"  Regressão Linear (R² = {modelos['regressao_linear']['r2']:.3f}):")
        for ano, valor in modelos['regressao_linear']['predicoes_futuras'].items():
            print(f"    {ano}: {valor:.1f}")
        print(f"  Média Móvel:")
        for ano, valor in modelos['media_movel']['predicoes_futuras'].items():
            print(f"    {ano}: {valor:.1f}")
    
    print()
    
    # 4. Salvar resultados
    output_file = analises_dir / "predicoes_tendencias.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(predicoes, f, indent=2, ensure_ascii=False)
    
    print("💾 Predições salvas em:")
    print(f"   {output_file}")
    print()
    print("⚠️  IMPORTANTE: Predições são estimativas baseadas em tendências históricas.")
    print("   Use com cautela e sempre valide com dados reais quando disponíveis.")

if __name__ == "__main__":
    main()


