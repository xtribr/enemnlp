#!/usr/bin/env python3
"""
📊 Processa dados TRI históricos do Google Sheets e integra ao sistema

Fonte: https://docs.google.com/spreadsheets/d/1aCR6Q9LBd5-byvzyFAECuwkTZc8bmRtwZxZ_m4U1FA8/edit
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List

# Mapeamento de áreas
AREA_MAP = {
    'CH': 'human-sciences',  # Ciências Humanas (questões 46-90)
    'CN': 'natural-sciences',  # Ciências da Natureza (questões 91-135)
    'LC': 'languages',  # Linguagens (questões 1-45)
    'MT': 'mathematics'  # Matemática (questões 136-180)
}

# Mapeamento de número de questão por área (ENEM padrão)
QUESTAO_OFFSET = {
    'languages': 1,      # Questões 1-45
    'human-sciences': 46,  # Questões 46-90
    'natural-sciences': 91,  # Questões 91-135
    'mathematics': 136    # Questões 136-180
}

def carregar_dados_tri() -> pd.DataFrame:
    """Carrega dados TRI da planilha do Google Sheets"""
    sheet_id = "1aCR6Q9LBd5-byvzyFAECuwkTZc8bmRtwZxZ_m4U1FA8"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    
    print(f"📥 Baixando dados TRI...")
    df = pd.read_csv(csv_url)
    
    # Converter valores numéricos (podem estar com vírgula como separador decimal)
    for col in ['min', 'max', 'media', 'mediana']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)
    
    print(f"✅ Carregados {len(df)} registros")
    print(f"   Anos: {sorted(df['ano'].unique())}")
    print(f"   Áreas: {df['area'].unique()}")
    
    return df

def processar_tri_por_questao(df: pd.DataFrame, ano: int = 2024) -> Dict:
    """
    Processa dados TRI e organiza por número de questão
    
    Args:
        df: DataFrame com dados TRI
        ano: Ano para processar (se 2024, usa dados mais recentes disponíveis)
    
    Returns:
        Dict: {numero_questao: {"TRI": valor, "area": area, "ano": ano}}
    """
    tri_por_questao = {}
    
    # Se ano 2024, usar dados mais recentes disponíveis
    anos_disponiveis = sorted(df['ano'].unique(), reverse=True)
    ano_usar = ano if ano in anos_disponiveis else anos_disponiveis[0]
    
    print(f"\n📊 Processando dados do ano {ano_usar}...")
    
    df_ano = df[df['ano'] == ano_usar].copy()
    
    for _, row in df_ano.iterrows():
        area_codigo = row['area']
        area = AREA_MAP.get(area_codigo)
        
        if not area:
            continue
        
        # "acertos" na planilha = número da questão dentro da área (0-indexed)
        # Converter para número global da questão no ENEM
        questao_na_area = int(row['acertos']) + 1  # 1-indexed dentro da área
        questao_global = QUESTAO_OFFSET[area] + questao_na_area - 1
        
        # Usar média TRI como valor principal
        tri_value = float(row['media'])
        
        tri_por_questao[questao_global] = {
            'TRI': tri_value,
            'TRI_min': float(row['min']),
            'TRI_max': float(row['max']),
            'TRI_mediana': float(row['mediana']),
            'area': area,
            'area_codigo': area_codigo,
            'ano': int(ano_usar),
            'questao_na_area': questao_na_area
        }
    
    return tri_por_questao

def formatar_para_tri_data(tri_por_questao: Dict) -> str:
    """
    Formata dados TRI no formato usado em 70_prompts_adaptativos_por_tri.py
    
    Returns:
        String Python com dicionário TRI_DATA formatado
    """
    linhas = []
    
    # Agrupar por área para melhor organização
    por_area = {
        'languages': [],
        'human-sciences': [],
        'natural-sciences': [],
        'mathematics': []
    }
    
    for num, dados in sorted(tri_por_questao.items()):
        area = dados['area']
        por_area[area].append((num, dados))
    
    # Gerar código Python
    linhas.append("# Dados TRI completos do ENEM (todas as áreas)")
    linhas.append("# Fonte: Google Sheets - ENEM 2009-2022")
    linhas.append("# Última atualização: dados mais recentes disponíveis")
    linhas.append("")
    linhas.append("TRI_DATA = {")
    
    for area_nome in ['languages', 'human-sciences', 'natural-sciences', 'mathematics']:
        if por_area[area_nome]:
            linhas.append(f"    # {area_nome.upper().replace('-', ' ')} ({len(por_area[area_nome])} questões)")
            for num, dados in sorted(por_area[area_nome]):
                tri = dados['TRI']
                nivel = classificar_nivel_tri(tri)
                tema = "N/A"  # Não temos tema nos dados históricos
                gab = "N/A"   # Não temos gabarito nos dados históricos
                
                linhas.append(f"    {num}: {{'TRI': {tri:.1f}, 'H': 'N/A', 'Nivel': '{nivel}', 'Tema': '{tema}', 'Gab': '{gab}'}},")
            linhas.append("")
    
    linhas.append("}")
    
    return "\n".join(linhas)

def classificar_nivel_tri(tri_value: float) -> str:
    """Classifica nível TRI segundo régua oficial ENEM"""
    if tri_value < 200:
        return "Muito Fácil"
    elif tri_value < 590:
        return "Fácil"
    elif tri_value < 690:
        return "Intermediário"
    elif tri_value < 700:
        return "Difícil"
    else:
        return "Muito Difícil"

def main():
    print("=" * 70)
    print("📊 PROCESSADOR DE DADOS TRI HISTÓRICOS")
    print("=" * 70)
    print()
    
    # Carregar dados
    df = carregar_dados_tri()
    
    # Processar para ENEM 2024 (ou ano mais recente disponível)
    tri_por_questao = processar_tri_por_questao(df, ano=2024)
    
    print(f"\n✅ Processadas {len(tri_por_questao)} questões")
    
    # Estatísticas por área
    print("\n📊 Questões por área:")
    por_area = {}
    for num, dados in tri_por_questao.items():
        area = dados['area']
        if area not in por_area:
            por_area[area] = []
        por_area[area].append(num)
    
    for area, questoes in sorted(por_area.items()):
        print(f"   {area}: {len(questoes)} questões ({min(questoes)}-{max(questoes)})")
    
    # Salvar JSON
    output_json = Path("data/analises/tri_enem_completo.json")
    output_json.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(tri_por_questao, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Dados salvos em: {output_json}")
    
    # Gerar código Python formatado
    codigo_python = formatar_para_tri_data(tri_por_questao)
    
    output_py = Path("data/analises/tri_data_formatado.py")
    with open(output_py, 'w', encoding='utf-8') as f:
        f.write(codigo_python)
    
    print(f"✅ Código Python formatado salvo em: {output_py}")
    
    # Mostrar amostra
    print("\n📋 Amostra de dados (primeiras 10 questões):")
    for num in sorted(tri_por_questao.keys())[:10]:
        dados = tri_por_questao[num]
        print(f"   Q{num:3d} ({dados['area']:15s}): TRI={dados['TRI']:6.1f} ({classificar_nivel_tri(dados['TRI'])})")
    
    print("\n💡 Próximos passos:")
    print("   1. Revisar dados gerados")
    print("   2. Integrar TRI_DATA em 70_prompts_adaptativos_por_tri.py")
    print("   3. Testar sistema com dados completos")

if __name__ == "__main__":
    main()

