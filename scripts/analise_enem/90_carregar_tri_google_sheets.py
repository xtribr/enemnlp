#!/usr/bin/env python3
"""
📊 Carrega dados TRI do Google Sheets (ENEM 2009-2022)

Fonte: https://docs.google.com/spreadsheets/d/1aCR6Q9LBd5-byvzyFAECuwkTZc8bmRtwZxZ_m4U1FA8/edit
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import gspread
    from google.oauth2.service_account import Credentials
    HAS_GSPREAD = True
except ImportError:
    HAS_GSPREAD = False
    print("⚠️  gspread não instalado. Instale com: pip install gspread google-auth")

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️  pandas não instalado. Instale com: pip install pandas")

# Mapeamento de áreas
AREA_MAP = {
    'CH': 'human-sciences',  # Ciências Humanas
    'CN': 'natural-sciences',  # Ciências da Natureza
    'LC': 'languages',  # Linguagens
    'MT': 'mathematics'  # Matemática
}

def carregar_tri_via_pandas(url: str) -> Dict:
    """
    Carrega dados TRI da planilha do Google Sheets usando pandas
    
    Args:
        url: URL da planilha do Google Sheets
        
    Returns:
        Dict com dados TRI organizados por ano, área e questão
    """
    if not HAS_PANDAS:
        raise ImportError("pandas é necessário para carregar dados")
    
    # Converter URL do Google Sheets para formato CSV
    sheet_id = url.split('/d/')[1].split('/')[0]
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    print(f"📥 Baixando dados TRI de: {csv_url}")
    
    try:
        df = pd.read_csv(csv_url)
        print(f"✅ Dados carregados: {len(df)} linhas")
        print(f"   Colunas: {list(df.columns)}")
        
        # Analisar estrutura
        print("\n📊 Primeiras linhas:")
        print(df.head(10))
        
        return df.to_dict('records')
    except Exception as e:
        print(f"❌ Erro ao carregar: {e}")
        return {}

def processar_dados_tri(dados_raw: List[Dict]) -> Dict:
    """
    Processa dados TRI brutos e organiza por questão
    
    Args:
        dados_raw: Lista de dicionários com dados brutos da planilha
        
    Returns:
        Dict organizado: {ano: {area: {questao_num: tri_value}}}
    """
    tri_organizado = {}
    
    for linha in dados_raw:
        area_codigo = linha.get('area', '')
        ano = linha.get('ano', '')
        acertos = linha.get('acertos', 0)
        media = linha.get('media', 0)
        min_val = linha.get('min', 0)
        max_val = linha.get('max', 0)
        
        # Mapear área
        area = AREA_MAP.get(area_codigo, area_codigo.lower())
        
        if not ano or not area:
            continue
        
        if ano not in tri_organizado:
            tri_organizado[ano] = {}
        
        if area not in tri_organizado[ano]:
            tri_organizado[ano][area] = {}
        
        # O número de acertos corresponde ao número da questão (0-indexed ou 1-indexed?)
        # Assumindo que acertos=0 é questão 1, acertos=1 é questão 2, etc.
        questao_num = int(acertos) + 1  # Converter para 1-indexed
        
        # Usar média TRI como valor principal
        tri_organizado[ano][area][questao_num] = {
            'TRI': float(media),
            'TRI_min': float(min_val),
            'TRI_max': float(max_val),
            'acertos': int(acertos)
        }
    
    return tri_organizado

def salvar_tri_json(tri_data: Dict, output_file: Path):
    """Salva dados TRI em arquivo JSON"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tri_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dados TRI salvos em: {output_file}")

def main():
    url = "https://docs.google.com/spreadsheets/d/1aCR6Q9LBd5-byvzyFAECuwkTZc8bmRtwZxZ_m4U1FA8/edit?usp=sharing"
    
    print("=" * 70)
    print("📊 CARREGADOR DE DADOS TRI - ENEM 2009-2022")
    print("=" * 70)
    print()
    
    # Carregar dados
    dados_raw = carregar_tri_via_pandas(url)
    
    if not dados_raw:
        print("❌ Não foi possível carregar dados")
        return
    
    # Processar
    print("\n🔄 Processando dados...")
    tri_organizado = processar_dados_tri(dados_raw)
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    for ano in sorted(tri_organizado.keys()):
        print(f"   {ano}:")
        for area, questoes in tri_organizado[ano].items():
            print(f"      {area}: {len(questoes)} questões")
    
    # Salvar
    output_file = Path("data/analises/tri_enem_2009_2022.json")
    salvar_tri_json(tri_organizado, output_file)
    
    # Também criar formato para uso direto no código
    print("\n💡 Próximos passos:")
    print("   1. Revisar dados carregados")
    print("   2. Integrar em 70_prompts_adaptativos_por_tri.py")
    print("   3. Mapear questões específicas do ENEM 2024")

if __name__ == "__main__":
    main()

