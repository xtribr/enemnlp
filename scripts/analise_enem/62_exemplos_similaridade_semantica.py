#!/usr/bin/env python3
"""
📚 Exemplos de Similaridade Semântica - ENEM

Mostra exemplos concretos de questões semanticamente similares:
- Dentro da mesma área (intra-área)
- Entre áreas correlatas (inter-área)
"""
import json
import sys
from pathlib import Path
import numpy as np
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

def carregar_questoes_por_ano(processed_dir: Path) -> Dict[int, List[Dict]]:
    """Carrega todas as questões por ano"""
    questoes_por_ano = {}
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        questoes_por_ano[ano] = questoes
    
    return questoes_por_ano

def encontrar_questoes_similares(questao_ref: Dict, questao_ref_emb: np.ndarray,
                                banco_questoes: List[Dict], banco_embeddings: np.ndarray,
                                top_k: int = 3, mesma_area: bool = True) -> List[Tuple[Dict, float]]:
    """Encontra questões similares usando embeddings"""
    similaridades = []
    ids_vistos = set()
    
    for i, questao in enumerate(banco_questoes):
        # Filtrar por área se necessário
        if mesma_area:
            if questao.get('area') != questao_ref.get('area'):
                continue
        
        # Evitar a própria questão e duplicatas
        questao_id = questao.get('id', '')
        if questao_id == questao_ref.get('id', '') or questao_id in ids_vistos:
            continue
        
        ids_vistos.add(questao_id)
        
        # Calcular similaridade
        emb_questao = banco_embeddings[i].reshape(1, -1)
        emb_ref = questao_ref_emb.reshape(1, -1)
        sim = cosine_similarity(emb_ref, emb_questao)[0][0]
        
        similaridades.append((questao, float(sim)))
    
    # Ordenar por similaridade e retornar top_k
    similaridades.sort(key=lambda x: x[1], reverse=True)
    return similaridades[:top_k]

def formatar_questao_para_exibicao(questao: Dict, max_chars: int = 300) -> str:
    """Formata questão para exibição"""
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    
    # Se não tem contexto, usar apenas pergunta
    if not contexto:
        texto_completo = pergunta
    else:
        texto_completo = f"{contexto}\n{pergunta}".strip()
    
    # Limpar quebras de linha excessivas
    texto_completo = ' '.join(texto_completo.split())
    
    if len(texto_completo) > max_chars:
        texto_completo = texto_completo[:max_chars] + "..."
    
    return texto_completo

def mostrar_exemplos_intra_area(questoes_por_ano: Dict[int, List[Dict]],
                                embeddings_por_ano: Dict[int, np.ndarray],
                                area: str, num_exemplos: int = 3):
    """Mostra exemplos de similaridade dentro da mesma área"""
    
    print(f"\n{'=' * 70}")
    print(f"🔍 EXEMPLOS: SIMILARIDADE INTRA-ÁREA - {area.upper()}")
    print(f"{'=' * 70}")
    print()
    
    # Coletar todas as questões da área
    todas_questoes_area = []
    todas_embeddings_area = []
    indices_questoes = []
    
    for ano in sorted(questoes_por_ano.keys()):
        if ano not in embeddings_por_ano:
            continue
        
        questoes_ano = questoes_por_ano[ano]
        embeddings_ano = embeddings_por_ano[ano]
        
        # Filtrar questões da área e mapear corretamente
        questoes_area_ano = [q for q in questoes_ano if q.get('area') == area]
        
        if len(questoes_area_ano) == 0:
            continue
        
        # Se temos embeddings para todas as questões do ano, usar índice sequencial
        # Caso contrário, precisamos mapear corretamente
        if len(embeddings_ano) >= len(questoes_ano):
            # Mapear questões da área para seus embeddings
            idx_emb = 0
            for questao in questoes_ano:
                if questao.get('area') == area:
                    if idx_emb < len(embeddings_ano):
                        todas_questoes_area.append(questao)
                        todas_embeddings_area.append(embeddings_ano[idx_emb])
                        indices_questoes.append((ano, idx_emb))
                idx_emb += 1
        else:
            # Se não temos embeddings suficientes, usar apenas questões que têm embedding
            for i, questao in enumerate(questoes_area_ano):
                if i < len(embeddings_ano):
                    todas_questoes_area.append(questao)
                    todas_embeddings_area.append(embeddings_ano[i])
                    indices_questoes.append((ano, i))
    
    if len(todas_questoes_area) < 2:
        print(f"⚠️  Poucas questões disponíveis para {area}")
        return
    
    # Converter para numpy array
    embeddings_array = np.array(todas_embeddings_area)
    
    # Selecionar questões de referência (diferentes anos)
    anos_unicos = sorted(set(q.get('exam', '') for q in todas_questoes_area))
    questoes_referencia = []
    
    for ano_str in anos_unicos[:num_exemplos]:
        questoes_ano = [q for q in todas_questoes_area if str(q.get('exam', '')) == str(ano_str)]
        if questoes_ano:
            questoes_referencia.append(questoes_ano[0])
    
    if not questoes_referencia:
        # Pegar questões aleatórias
        import random
        questoes_referencia = random.sample(todas_questoes_area, min(num_exemplos, len(todas_questoes_area)))
    
    # Para cada questão de referência, encontrar similares
    for i, questao_ref in enumerate(questoes_referencia, 1):
        idx_ref = todas_questoes_area.index(questao_ref)
        emb_ref = embeddings_array[idx_ref]
        
        similares = encontrar_questoes_similares(
            questao_ref, emb_ref, todas_questoes_area, embeddings_array,
            top_k=2, mesma_area=True
        )
        
        print(f"📌 Exemplo {i}: Questão de Referência")
        print(f"   Ano: {questao_ref.get('exam', 'N/A')} | ID: {questao_ref.get('id', 'N/A')}")
        texto_ref = formatar_questao_para_exibicao(questao_ref, 250)
        print(f"   Texto: {texto_ref}")
        print()
        
        if similares:
            print(f"   🔗 Questões Similares (mesma área):")
            for j, (questao_sim, sim_score) in enumerate(similares, 1):
                print(f"      {j}. Similaridade: {sim_score:.3f} | Ano: {questao_sim.get('exam', 'N/A')} | ID: {questao_sim.get('id', 'N/A')}")
                texto_sim = formatar_questao_para_exibicao(questao_sim, 250)
                print(f"         {texto_sim}")
                print()
        print()

def mostrar_exemplos_inter_area(questoes_por_ano: Dict[int, List[Dict]],
                                embeddings_por_ano: Dict[int, np.ndarray],
                                area1: str, area2: str, num_exemplos: int = 2):
    """Mostra exemplos de similaridade entre áreas correlatas"""
    
    print(f"\n{'=' * 70}")
    print(f"🔗 EXEMPLOS: SIMILARIDADE INTER-ÁREA - {area1.upper()} ↔ {area2.upper()}")
    print(f"{'=' * 70}")
    print()
    
    # Coletar questões de ambas as áreas
    questoes_area1 = []
    embeddings_area1 = []
    questoes_area2 = []
    embeddings_area2 = []
    
    for ano in sorted(questoes_por_ano.keys()):
        if ano not in embeddings_por_ano:
            continue
        
        questoes_ano = questoes_por_ano[ano]
        embeddings_ano = embeddings_por_ano[ano]
        
        # Mapear corretamente questões para embeddings
        if len(embeddings_ano) >= len(questoes_ano):
            idx_emb = 0
            for questao in questoes_ano:
                if questao.get('area') == area1 and idx_emb < len(embeddings_ano):
                    questoes_area1.append(questao)
                    embeddings_area1.append(embeddings_ano[idx_emb])
                elif questao.get('area') == area2 and idx_emb < len(embeddings_ano):
                    questoes_area2.append(questao)
                    embeddings_area2.append(embeddings_ano[idx_emb])
                idx_emb += 1
        else:
            # Fallback: usar apenas primeiras questões
            questoes_area1_ano = [q for q in questoes_ano if q.get('area') == area1]
            questoes_area2_ano = [q for q in questoes_ano if q.get('area') == area2]
            
            for i, questao in enumerate(questoes_area1_ano):
                if i < len(embeddings_ano):
                    questoes_area1.append(questao)
                    embeddings_area1.append(embeddings_ano[i])
            
            for i, questao in enumerate(questoes_area2_ano):
                if i < len(embeddings_ano):
                    questoes_area2.append(questao)
                    embeddings_area2.append(embeddings_ano[i])
    
    if len(questoes_area1) == 0 or len(questoes_area2) == 0:
        print(f"⚠️  Dados insuficientes para comparar {area1} e {area2}")
        return
    
    embeddings_array1 = np.array(embeddings_area1)
    embeddings_array2 = np.array(embeddings_area2)
    
    # Selecionar questões de referência da área 1
    import random
    questoes_ref = random.sample(questoes_area1, min(num_exemplos, len(questoes_area1)))
    
    for i, questao_ref in enumerate(questoes_ref, 1):
        idx_ref = questoes_area1.index(questao_ref)
        emb_ref = embeddings_array1[idx_ref]
        
        # Encontrar questões similares na área 2
        similaridades = []
        for j, questao_area2 in enumerate(questoes_area2):
            emb_area2 = embeddings_array2[j].reshape(1, -1)
            emb_ref_reshaped = emb_ref.reshape(1, -1)
            sim = cosine_similarity(emb_ref_reshaped, emb_area2)[0][0]
            similaridades.append((questao_area2, float(sim)))
        
        similaridades.sort(key=lambda x: x[1], reverse=True)
        top_similares = similaridades[:2]
        
        print(f"📌 Exemplo {i}: Questão de {area1}")
        print(f"   Ano: {questao_ref.get('exam', 'N/A')} | ID: {questao_ref.get('id', 'N/A')}")
        texto_ref = formatar_questao_para_exibicao(questao_ref, 250)
        print(f"   Texto: {texto_ref}")
        print()
        
        if top_similares:
            print(f"   🔗 Questões Similares em {area2}:")
            for j, (questao_sim, sim_score) in enumerate(top_similares, 1):
                print(f"      {j}. Similaridade: {sim_score:.3f} | Ano: {questao_sim.get('exam', 'N/A')} | ID: {questao_sim.get('id', 'N/A')}")
                texto_sim = formatar_questao_para_exibicao(questao_sim, 250)
                print(f"         {texto_sim}")
                print()
        print()

def main():
    """Função principal"""
    print("=" * 70)
    print("📚 EXEMPLOS DE SIMILARIDADE SEMÂNTICA - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    embeddings_dir = project_root / "data" / "embeddings"
    processed_dir = project_root / "data" / "processed"
    
    # Carregar dados
    print("📥 Carregando dados...")
    embeddings_por_ano = carregar_embeddings(embeddings_dir)
    questoes_por_ano = carregar_questoes_por_ano(processed_dir)
    
    if not embeddings_por_ano or not questoes_por_ano:
        print("❌ Dados insuficientes")
        return
    
    print(f"✅ {len(embeddings_por_ano)} anos com embeddings")
    print(f"✅ {len(questoes_por_ano)} anos com questões")
    print()
    
    # Mapear áreas
    areas_map = {
        'languages': 'Linguagens',
        'human-sciences': 'Humanas',
        'natural-sciences': 'Natureza',
        'mathematics': 'Matemática'
    }
    
    # 1. Exemplos intra-área
    print("=" * 70)
    print("🔍 PARTE 1: SIMILARIDADE INTRA-ÁREA")
    print("=" * 70)
    print("(Questões da mesma área em anos diferentes)")
    print()
    
    for area_codigo, area_nome in areas_map.items():
        mostrar_exemplos_intra_area(questoes_por_ano, embeddings_por_ano, 
                                   area_codigo, num_exemplos=2)
    
    # 2. Exemplos inter-área (áreas correlatas)
    print("\n" + "=" * 70)
    print("🔗 PARTE 2: SIMILARIDADE INTER-ÁREA (ÁREAS CORRELATAS)")
    print("=" * 70)
    print("(Questões de áreas diferentes mas semanticamente relacionadas)")
    print()
    
    # Pares correlatos mais altos
    pares_correlatos = [
        ('languages', 'human-sciences'),      # 0.789
        ('natural-sciences', 'mathematics'), # 0.649
    ]
    
    for area1_codigo, area2_codigo in pares_correlatos:
        area1_nome = areas_map[area1_codigo]
        area2_nome = areas_map[area2_codigo]
        mostrar_exemplos_inter_area(questoes_por_ano, embeddings_por_ano,
                                   area1_codigo, area2_codigo, num_exemplos=2)
    
    print("=" * 70)
    print("✅ EXEMPLOS EXIBIDOS")
    print("=" * 70)
    print()
    print("💡 Interpretação:")
    print("   • Similaridade alta (>0.8): Questões muito similares semanticamente")
    print("   • Similaridade média (0.6-0.8): Questões relacionadas mas distintas")
    print("   • Similaridade baixa (<0.6): Questões com pouca relação semântica")

if __name__ == "__main__":
    main()

