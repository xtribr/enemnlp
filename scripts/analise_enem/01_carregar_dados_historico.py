#!/usr/bin/env python3
"""
Carregar dados históricos do ENEM (2009-2023) do repositório extract-enem-data

Este script integra os dados históricos com os dados já existentes (2022, 2023, 2024)
para criar uma série temporal completa.
"""
import json
import csv
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import subprocess

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def clonar_repositorio_historico(dest_dir: Path) -> Path:
    """Clona o repositório extract-enem-data se não existir"""
    repo_dir = dest_dir / "extract-enem-data"
    
    if not repo_dir.exists():
        print("📥 Clonando repositório extract-enem-data...")
        try:
            subprocess.run(
                ["git", "clone", "https://github.com/gabriel-antonelli/extract-enem-data.git", str(repo_dir)],
                check=True,
                capture_output=True
            )
            print("✅ Repositório clonado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao clonar repositório: {e}")
            return None
    else:
        print("✅ Repositório já existe")
    
    return repo_dir

def carregar_csv_enem(csv_path: Path, ano: int, area: str) -> List[Dict[str, Any]]:
    """Carrega questões de um arquivo CSV do ENEM"""
    questoes = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalizar estrutura
                questao = {
                    'id': f"enem_{ano}_{area}_{row.get('number', '')}",
                    'exam': str(ano),
                    'area': area,
                    'number': row.get('number', ''),
                    'context': row.get('context', '').strip(),
                    'question': row.get('question', '').strip(),
                    'alternatives': [
                        row.get('A', '').strip(),
                        row.get('B', '').strip(),
                        row.get('C', '').strip(),
                        row.get('D', '').strip(),
                        row.get('E', '').strip()
                    ],
                    'label': row.get('answer', '').upper().strip(),
                    'context_images': row.get('context-images', '').strip(),
                    'has_images': bool(row.get('context-images', '').strip())
                }
                
                # Validar questão
                if questao['question'] and questao['label'] in ['A', 'B', 'C', 'D', 'E']:
                    questoes.append(questao)
    
    except Exception as e:
        print(f"⚠️  Erro ao carregar {csv_path}: {e}")
    
    return questoes

def carregar_dados_historicos(repo_dir: Path, anos: List[int] = None) -> Dict[int, Dict[str, List[Dict]]]:
    """Carrega todos os dados históricos do ENEM"""
    if anos is None:
        # Carregar todos os anos disponíveis (2009-2023)
        anos = list(range(2009, 2024))
    
    areas = {
        'linguagens': 'languages',
        'ciencias-humanas': 'human-sciences',
        'ciencias-natureza': 'natural-sciences',
        'matematica': 'mathematics'
    }
    
    dados_historicos = {}
    enem_data_dir = repo_dir / "enem-data"
    
    if not enem_data_dir.exists():
        print(f"❌ Diretório não encontrado: {enem_data_dir}")
        return dados_historicos
    
    print(f"📊 Carregando dados históricos (2009-2023)...")
    
    for ano in anos:
        ano_dir = enem_data_dir / f"enem-{ano}"
        
        if not ano_dir.exists():
            print(f"⚠️  Ano {ano} não encontrado")
            continue
        
        dados_historicos[ano] = {}
        total_questoes = 0
        
        for area_csv, area_norm in areas.items():
            csv_path = ano_dir / f"{area_csv}.csv"
            
            if csv_path.exists():
                questoes = carregar_csv_enem(csv_path, ano, area_norm)
                dados_historicos[ano][area_norm] = questoes
                total_questoes += len(questoes)
                print(f"   {ano} - {area_norm}: {len(questoes)} questões")
            else:
                dados_historicos[ano][area_norm] = []
                print(f"   {ano} - {area_norm}: arquivo não encontrado")
        
        print(f"   {ano}: {total_questoes} questões totais")
    
    return dados_historicos

def carregar_dados_existentes(data_dir: Path) -> Dict[int, List[Dict]]:
    """Carrega dados já existentes no projeto (2022, 2023, 2024)"""
    dados_existentes = {}
    
    # 2024 - JSONL
    jsonl_2024 = data_dir / "2024.jsonl"
    if jsonl_2024.exists():
        dados_existentes[2024] = []
        with open(jsonl_2024, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    dados_existentes[2024].append(json.loads(line))
        print(f"✅ 2024: {len(dados_existentes[2024])} questões (JSONL)")
    
    # 2022 - JSON (deprecated, mas pode ter dados úteis)
    json_2022 = data_dir / "2022.json"
    if json_2022.exists():
        with open(json_2022, 'r', encoding='utf-8') as f:
            dados_2022 = json.load(f)
            dados_existentes[2022] = dados_2022
            print(f"✅ 2022: {len(dados_2022)} questões (JSON)")
    
    return dados_existentes

def normalizar_e_combinar_dados(dados_historicos: Dict, dados_existentes: Dict) -> Dict[int, List[Dict]]:
    """Normaliza e combina dados históricos e existentes"""
    dados_combinados = {}
    
    # Processar dados históricos (2009-2023)
    for ano, areas in dados_historicos.items():
        dados_combinados[ano] = []
        for area, questoes in areas.items():
            dados_combinados[ano].extend(questoes)
    
    # Adicionar/sobrescrever com dados existentes (mais recentes e completos)
    for ano, questoes in dados_existentes.items():
        if ano in dados_combinados:
            print(f"⚠️  Ano {ano} já existe nos dados históricos, usando dados existentes (mais completos)")
        dados_combinados[ano] = questoes
    
    return dados_combinados

def salvar_dados_combinados(dados: Dict[int, List[Dict]], output_dir: Path):
    """Salva dados combinados em formato JSONL"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar por ano
    for ano, questoes in dados.items():
        output_file = output_dir / f"enem_{ano}_completo.jsonl"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for questao in questoes:
                f.write(json.dumps(questao, ensure_ascii=False) + '\n')
        
        print(f"💾 {ano}: {len(questoes)} questões salvas em {output_file.name}")
    
    # Estatísticas gerais
    total_questoes = sum(len(questoes) for questoes in dados.values())
    anos_disponiveis = sorted(dados.keys())
    
    print(f"\n📊 Estatísticas Gerais:")
    print(f"   Total de anos: {len(anos_disponiveis)}")
    print(f"   Período: {min(anos_disponiveis)} - {max(anos_disponiveis)}")
    print(f"   Total de questões: {total_questoes}")
    print(f"   Média por ano: {total_questoes / len(anos_disponiveis):.0f} questões")

def main():
    """Função principal"""
    print("=" * 70)
    print("📚 CARREGAMENTO DE DADOS HISTÓRICOS DO ENEM")
    print("=" * 70)
    print()
    
    # Diretórios
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "enem"
    processed_dir = project_root / "data" / "processed"
    temp_dir = project_root / "data" / "temp"
    
    # Criar diretórios
    processed_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Clonar repositório histórico
    repo_dir = clonar_repositorio_historico(temp_dir)
    if not repo_dir:
        print("❌ Não foi possível acessar dados históricos")
        return
    
    # 2. Carregar dados históricos (2009-2023)
    dados_historicos = carregar_dados_historicos(repo_dir)
    
    if not dados_historicos:
        print("❌ Nenhum dado histórico carregado")
        return
    
    # 3. Carregar dados existentes (2022, 2023, 2024)
    dados_existentes = carregar_dados_existentes(data_dir)
    
    # 4. Combinar e normalizar
    print("\n🔄 Combinando e normalizando dados...")
    dados_combinados = normalizar_e_combinar_dados(dados_historicos, dados_existentes)
    
    # 5. Salvar dados combinados
    print("\n💾 Salvando dados combinados...")
    salvar_dados_combinados(dados_combinados, processed_dir)
    
    print("\n" + "=" * 70)
    print("✅ CARREGAMENTO CONCLUÍDO!")
    print("=" * 70)
    print(f"\n📁 Dados salvos em: {processed_dir}")
    print("\n💡 Próximos passos:")
    print("   1. Executar: 02_preprocessar_texto.py")
    print("   2. Executar: 03_validar_dados.py")

if __name__ == "__main__":
    main()


