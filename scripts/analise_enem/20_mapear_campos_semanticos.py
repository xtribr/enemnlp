#!/usr/bin/env python3
"""
Mapeamento de Campos Semânticos do ENEM

Mapeia todas as questões para campos semânticos baseados em vocabulário específico.
"""
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Definição dos campos semânticos por área do ENEM
SEMANTIC_FIELDS = {
    "linguagens": [
        "arte", "artes", "educação física", "educacao fisica", "inglês", "ingles", "espanhol",
        "interpretação de texto", "interpretacao de texto", "generos textuais", "gêneros textuais",
        "literatura", "literatura brasileira", "comunicação", "linguagem", "gramática", "gramatica"
    ],
    "humanas": [
        "filosofia", "sociologia", "geografia", "história", "historia", "sociedade", "cultura",
        "política", "politica", "economia", "cidadania", "direitos humanos", "meio ambiente"
    ],
    "natureza": [
        "física", "fisica", "química", "quimica", "biologia", "ciências", "ciencia",
        "ecologia", "saúde", "saude", "tecnologia", "ambiente", "natureza", "universo"
    ],
    "matematica": [
        "álgebra", "algebra", "aritmética", "aritmetica", "matemática básica", "matematica basica",
        "geometria plana", "geometria espacial", "geometria analítica", "geometria analitica",
        "cálculo", "calculo", "estatística", "estatistica", "probabilidade", "razão", "proporção"
    ]
}

def normalizar_texto(texto: str) -> str:
    """Normaliza texto para busca (remove acentos, lowercase)"""
    if not texto:
        return ""
    texto = texto.lower()
    # Remove acentos básicos (simplificado)
    texto = texto.replace('á', 'a').replace('à', 'a').replace('â', 'a').replace('ã', 'a')
    texto = texto.replace('é', 'e').replace('ê', 'e')
    texto = texto.replace('í', 'i')
    texto = texto.replace('ó', 'o').replace('ô', 'o').replace('õ', 'o')
    texto = texto.replace('ú', 'u').replace('ü', 'u')
    texto = texto.replace('ç', 'c')
    return texto

def encontrar_campos_semanticos(texto: str, area: str) -> List[str]:
    """Encontra campos semânticos presentes no texto"""
    texto_normalizado = normalizar_texto(texto)
    campos_encontrados = []
    
    # Mapear área para chave do dicionário
    area_map = {
        'languages': 'linguagens',
        'human-sciences': 'humanas',
        'natural-sciences': 'natureza',
        'mathematics': 'matematica'
    }
    
    area_key = area_map.get(area, area.lower())
    campos_area = SEMANTIC_FIELDS.get(area_key, [])
    
    # Buscar campos semânticos no texto
    for campo in campos_area:
        campo_normalizado = normalizar_texto(campo)
        # Buscar palavra completa (evitar matches parciais)
        pattern = r'\b' + re.escape(campo_normalizado) + r'\b'
        if re.search(pattern, texto_normalizado):
            campos_encontrados.append(campo)
    
    return campos_encontrados

def processar_todas_questoes(dados: Dict[int, List[Dict]]) -> Dict:
    """Processa todas as questões mapeando campos semânticos"""
    resultados = {}
    estatisticas_globais = defaultdict(int)
    
    print("🔄 Processando questões e mapeando campos semânticos...")
    print()
    
    for ano in sorted(dados.keys()):
        questoes = dados[ano]
        questoes_mapeadas = []
        campos_por_questao = defaultdict(int)
        
        for questao in questoes:
            contexto = questao.get('context', '')
            pergunta = questao.get('question', '')
            texto_completo = f"{contexto} {pergunta}"
            area = questao.get('area', 'desconhecida')
            
            # Encontrar campos semânticos
            campos = encontrar_campos_semanticos(texto_completo, area)
            
            questao_mapeada = questao.copy()
            questao_mapeada['campos_semanticos'] = campos
            questao_mapeada['num_campos_semanticos'] = len(campos)
            
            questoes_mapeadas.append(questao_mapeada)
            
            # Estatísticas
            for campo in campos:
                campos_por_questao[campo] += 1
                estatisticas_globais[campo] += 1
        
        resultados[ano] = {
            'questoes': questoes_mapeadas,
            'estatisticas': {
                'total_questoes': len(questoes),
                'questoes_com_campos': sum(1 for q in questoes_mapeadas if q['campos_semanticos']),
                'campos_mais_frequentes': dict(sorted(campos_por_questao.items(), 
                                                      key=lambda x: x[1], reverse=True)[:10])
            }
        }
        
        print(f"  {ano}: {len(questoes)} questões, "
              f"{sum(1 for q in questoes_mapeadas if q['campos_semanticos'])} com campos identificados")
    
    print()
    print("📊 Campos semânticos mais frequentes (global):")
    top_campos = sorted(estatisticas_globais.items(), key=lambda x: x[1], reverse=True)[:20]
    for campo, count in top_campos:
        print(f"   {campo:30s}: {count:4d} ocorrências")
    
    return resultados

def salvar_resultados(resultados: Dict, output_dir: Path):
    """Salva resultados do mapeamento"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar completo
    arquivo = output_dir / "campos_semanticos_completo.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    # Salvar apenas estatísticas
    estatisticas = {ano: dados['estatisticas'] for ano, dados in resultados.items()}
    arquivo_stats = output_dir / "campos_semanticos_estatisticas.json"
    with open(arquivo_stats, 'w', encoding='utf-8') as f:
        json.dump(estatisticas, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em:")
    print(f"   - {arquivo.name}")
    print(f"   - {arquivo_stats.name}")

def main():
    """Função principal"""
    print("=" * 70)
    print("🔍 MAPEAMENTO DE CAMPOS SEMÂNTICOS - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    analises_dir = project_root / "data" / "analises"
    
    # Carregar dados
    print("📥 Carregando dados...")
    dados = {}
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        dados[ano] = questoes
    
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # Processar mapeamento
    resultados = processar_todas_questoes(dados)
    
    # Salvar resultados
    salvar_resultados(resultados, analises_dir)
    
    print()
    print("=" * 70)
    print("✅ MAPEAMENTO DE CAMPOS SEMÂNTICOS CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    main()


