#!/usr/bin/env python3
"""
Análise de Similaridade entre Provas do ENEM

Calcula similaridade lexical e semântica entre provas de diferentes anos.
"""
import json
import sys
from pathlib import Path
import numpy as np
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

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

def carregar_embeddings(embeddings_dir: Path) -> Dict[int, np.ndarray]:
    """Carrega embeddings se disponíveis"""
    embeddings = {}
    
    if not embeddings_dir.exists():
        return embeddings
    
    indice_file = embeddings_dir / "indice_embeddings.json"
    if indice_file.exists():
        with open(indice_file, 'r') as f:
            indice = json.load(f)
        
        for ano in indice['anos']:
            emb_file = embeddings_dir / f"embeddings_{ano}.npy"
            if emb_file.exists():
                embeddings[ano] = np.load(emb_file)
    
    return embeddings

def similaridade_lexical_jaccard(texto1: str, texto2: str) -> float:
    """Calcula similaridade de Jaccard entre dois textos"""
    palavras1 = set(texto1.lower().split())
    palavras2 = set(texto2.lower().split())
    
    if not palavras1 or not palavras2:
        return 0.0
    
    intersecao = len(palavras1 & palavras2)
    uniao = len(palavras1 | palavras2)
    
    return intersecao / uniao if uniao > 0 else 0.0

def similaridade_lexical_cosseno(vocab1: Dict[str, int], vocab2: Dict[str, int]) -> float:
    """Calcula similaridade de cosseno entre vocabulários"""
    todas_palavras = set(vocab1.keys()) | set(vocab2.keys())
    
    if not todas_palavras:
        return 0.0
    
    vetor1 = np.array([vocab1.get(p, 0) for p in todas_palavras])
    vetor2 = np.array([vocab2.get(p, 0) for p in todas_palavras])
    
    # Normalizar
    norm1 = np.linalg.norm(vetor1)
    norm2 = np.linalg.norm(vetor2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return np.dot(vetor1, vetor2) / (norm1 * norm2)

def construir_vocabulario_ano(questoes: List[Dict]) -> Dict[str, int]:
    """Constrói vocabulário de um ano"""
    vocabulario = Counter()
    
    for questao in questoes:
        contexto = questao.get('context', '')
        pergunta = questao.get('question', '')
        texto = f"{contexto} {pergunta}".lower()
        
        palavras = texto.split()
        vocabulario.update(palavras)
    
    return dict(vocabulario)

def similaridade_semantica_embeddings(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Calcula similaridade semântica usando embeddings"""
    if emb1.shape[0] == 0 or emb2.shape[0] == 0:
        return 0.0
    
    # Calcular embedding médio de cada prova
    emb1_medio = emb1.mean(axis=0).reshape(1, -1)
    emb2_medio = emb2.mean(axis=0).reshape(1, -1)
    
    # Similaridade de cosseno
    similaridade = cosine_similarity(emb1_medio, emb2_medio)[0][0]
    
    return float(similaridade)

def calcular_similaridade_entre_anos(dados: Dict[int, List[Dict]], embeddings: Dict[int, np.ndarray] = None) -> Dict:
    """Calcula similaridade entre todos os pares de anos"""
    anos = sorted(dados.keys())
    resultados = {
        'similaridade_lexical_jaccard': {},
        'similaridade_lexical_cosseno': {},
        'similaridade_semantica': {}
    }
    
    # Construir vocabulários
    print("📚 Construindo vocabulários...")
    vocabularios = {}
    textos_completos = {}
    
    for ano in anos:
        questoes = dados[ano]
        vocabularios[ano] = construir_vocabulario_ano(questoes)
        
        # Texto completo do ano (para Jaccard)
        textos = []
        for questao in questoes:
            contexto = questao.get('context', '')
            pergunta = questao.get('question', '')
            textos.append(f"{contexto} {pergunta}")
        textos_completos[ano] = " ".join(textos)
    
    print(f"✅ {len(vocabularios)} vocabulários construídos")
    print()
    
    # Calcular similaridades
    print("🔄 Calculando similaridades...")
    total_pares = len(anos) * (len(anos) - 1) // 2
    contador = 0
    
    for i, ano1 in enumerate(anos):
        for ano2 in anos[i+1:]:
            contador += 1
            
            # Similaridade Jaccard
            jaccard = similaridade_lexical_jaccard(
                textos_completos[ano1],
                textos_completos[ano2]
            )
            resultados['similaridade_lexical_jaccard'][f"{ano1}-{ano2}"] = jaccard
            
            # Similaridade Cosseno (vocabulário)
            cosseno = similaridade_lexical_cosseno(
                vocabularios[ano1],
                vocabularios[ano2]
            )
            resultados['similaridade_lexical_cosseno'][f"{ano1}-{ano2}"] = cosseno
            
            # Similaridade Semântica (se embeddings disponíveis)
            if embeddings and ano1 in embeddings and ano2 in embeddings:
                semantica = similaridade_semantica_embeddings(
                    embeddings[ano1],
                    embeddings[ano2]
                )
                resultados['similaridade_semantica'][f"{ano1}-{ano2}"] = semantica
            
            if contador % 10 == 0:
                print(f"  Processados {contador}/{total_pares} pares...")
    
    print(f"✅ {contador} pares processados")
    print()
    
    return resultados

def criar_matriz_similaridade(resultados: Dict, tipo: str) -> Tuple[np.ndarray, List[int]]:
    """Cria matriz de similaridade"""
    anos = sorted(set(
        int(ano) for par in resultados[tipo].keys()
        for ano in par.split('-')
    ))
    
    matriz = np.zeros((len(anos), len(anos)))
    
    for i, ano1 in enumerate(anos):
        for j, ano2 in enumerate(anos):
            if i == j:
                matriz[i, j] = 1.0
            else:
                chave = f"{min(ano1, ano2)}-{max(ano1, ano2)}"
                matriz[i, j] = resultados[tipo].get(chave, 0.0)
    
    return matriz, anos

def main():
    """Função principal"""
    print("=" * 70)
    print("🔗 ANÁLISE DE SIMILARIDADE ENTRE PROVAS - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    embeddings_dir = project_root / "data" / "embeddings"
    analises_dir = project_root / "data" / "analises"
    
    # Carregar dados
    print("📥 Carregando dados...")
    dados = carregar_dados_processados(processed_dir)
    print(f"✅ {len(dados)} anos carregados")
    
    # Carregar embeddings (opcional)
    embeddings = {}
    if embeddings_dir.exists():
        print("📥 Carregando embeddings...")
        embeddings = carregar_embeddings(embeddings_dir)
        if embeddings:
            print(f"✅ {len(embeddings)} anos com embeddings")
        else:
            print("⚠️  Nenhum embedding encontrado (similaridade semântica não disponível)")
    else:
        print("⚠️  Diretório de embeddings não encontrado")
        print("   Execute: 04_gerar_embeddings.py para gerar embeddings")
    print()
    
    # Calcular similaridades
    resultados = calcular_similaridade_entre_anos(dados, embeddings)
    
    # Salvar resultados
    analises_dir.mkdir(parents=True, exist_ok=True)
    arquivo = analises_dir / "similaridade_provas.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print("💾 Resultados salvos em:")
    print(f"   {arquivo}")
    print()
    
    # Estatísticas
    print("=" * 70)
    print("📊 ESTATÍSTICAS DE SIMILARIDADE")
    print("=" * 70)
    
    for tipo, valores in resultados.items():
        if valores:
            similaridades = list(valores.values())
            print(f"\n{tipo.upper()}:")
            print(f"  Média: {np.mean(similaridades):.3f}")
            print(f"  Mediana: {np.median(similaridades):.3f}")
            print(f"  Min: {np.min(similaridades):.3f}")
            print(f"  Max: {np.max(similaridades):.3f}")
    
    print()
    print("=" * 70)
    print("✅ ANÁLISE DE SIMILARIDADE CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()


