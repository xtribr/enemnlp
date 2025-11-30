#!/usr/bin/env python3
"""
Modelagem de Tópicos para Questões do ENEM

Usa LDA e NMF para identificar tópicos predominantes nas provas.
"""
import json
import sys
from pathlib import Path
import numpy as np
from typing import Dict, List
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

def preparar_textos_para_topicos(dados: Dict[int, List[Dict]], por_area: bool = False) -> Dict:
    """Prepara textos para modelagem de tópicos"""
    textos_por_grupo = defaultdict(list)
    ids_por_grupo = defaultdict(list)
    
    for ano, questoes in dados.items():
        for questao in questoes:
            # Combinar contexto e pergunta
            contexto = questao.get('context', '').strip()
            pergunta = questao.get('question', '').strip()
            texto = f"{contexto} {pergunta}".strip()
            
            if not texto:
                continue
            
            # Agrupar por área ou por ano
            if por_area:
                area = questao.get('area', 'geral')
                chave = f"{ano}_{area}"
            else:
                chave = str(ano)
            
            textos_por_grupo[chave].append(texto)
            ids_por_grupo[chave].append(questao.get('id', ''))
    
    return textos_por_grupo, ids_por_grupo

def modelagem_lda(textos: List[str], num_topics: int = 10, lang: str = 'portuguese'):
    """Modelagem de tópicos usando LDA"""
    try:
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.decomposition import LatentDirichletAllocation
        import nltk
        from nltk.corpus import stopwords
        
        # Download stopwords se necessário
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        # Stopwords em português
        stop_words = stopwords.words('portuguese')
        
        # Vectorização
        vectorizer = CountVectorizer(
            max_features=1000,
            stop_words=stop_words,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        
        print(f"  🔄 Vectorizando {len(textos)} textos...")
        X = vectorizer.fit_transform(textos)
        
        # LDA
        print(f"  🔄 Treinando LDA com {num_topics} tópicos...")
        lda = LatentDirichletAllocation(
            n_components=num_topics,
            random_state=42,
            max_iter=20,
            learning_method='online'
        )
        lda.fit(X)
        
        # Extrair tópicos
        feature_names = vectorizer.get_feature_names_out()
        topicos = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topicos.append({
                'id': topic_idx,
                'palavras_chave': top_words,
                'pesos': [float(topic[i]) for i in top_words_idx]
            })
        
        return topicos, lda, vectorizer
    
    except ImportError as e:
        print(f"  ⚠️  Dependências não instaladas: {e}")
        print("  Instale com: pip install scikit-learn nltk")
        return None, None, None
    except Exception as e:
        print(f"  ❌ Erro na modelagem LDA: {e}")
        return None, None, None

def modelagem_nmf(textos: List[str], num_topics: int = 10, lang: str = 'portuguese'):
    """Modelagem de tópicos usando NMF"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import NMF
        import nltk
        from nltk.corpus import stopwords
        
        # Download stopwords se necessário
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        stop_words = stopwords.words('portuguese')
        
        # Vectorização TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=stop_words,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        
        print(f"  🔄 Vectorizando {len(textos)} textos...")
        X = vectorizer.fit_transform(textos)
        
        # NMF
        print(f"  🔄 Treinando NMF com {num_topics} tópicos...")
        nmf = NMF(n_components=num_topics, random_state=42, max_iter=200)
        nmf.fit(X)
        
        # Extrair tópicos
        feature_names = vectorizer.get_feature_names_out()
        topicos = []
        
        for topic_idx, topic in enumerate(nmf.components_):
            top_words_idx = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topicos.append({
                'id': topic_idx,
                'palavras_chave': top_words,
                'pesos': [float(topic[i]) for i in top_words_idx]
            })
        
        return topicos, nmf, vectorizer
    
    except ImportError as e:
        print(f"  ⚠️  Dependências não instaladas: {e}")
        return None, None, None
    except Exception as e:
        print(f"  ❌ Erro na modelagem NMF: {e}")
        return None, None, None

def processar_por_ano(dados: Dict[int, List[Dict]], metodo: str = "lda", num_topics: int = 10):
    """Processa modelagem de tópicos por ano"""
    resultados = {}
    
    textos_por_grupo, ids_por_grupo = preparar_textos_para_topicos(dados, por_area=False)
    
    print(f"🔧 Método: {metodo.upper()}, Tópicos: {num_topics}")
    print()
    
    for chave in sorted(textos_por_grupo.keys()):
        textos = textos_por_grupo[chave]
        print(f"📊 Processando {chave} ({len(textos)} questões)...")
        
        if metodo.lower() == "lda":
            topicos, modelo, vectorizer = modelagem_lda(textos, num_topics)
        elif metodo.lower() == "nmf":
            topicos, modelo, vectorizer = modelagem_nmf(textos, num_topics)
        else:
            print(f"  ❌ Método desconhecido: {metodo}")
            continue
        
        if topicos:
            resultados[chave] = {
                'topicos': topicos,
                'num_questoes': len(textos)
            }
            print(f"  ✅ {len(topicos)} tópicos identificados")
        else:
            print(f"  ❌ Falha na modelagem para {chave}")
        
        print()
    
    return resultados

def salvar_resultados(resultados: Dict, output_dir: Path, metodo: str):
    """Salva resultados da modelagem"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / f"topicos_{metodo}.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em: {arquivo}")

def main():
    """Função principal"""
    print("=" * 70)
    print("📚 MODELAGEM DE TÓPICOS - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    analises_dir = project_root / "data" / "analises"
    
    # Carregar dados
    print("📥 Carregando dados...")
    dados = carregar_dados_processados(processed_dir)
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # Processar com LDA
    print("🔄 Processando com LDA...")
    resultados_lda = processar_por_ano(dados, metodo="lda", num_topics=10)
    if resultados_lda:
        salvar_resultados(resultados_lda, analises_dir, "lda")
    
    print()
    
    # Processar com NMF
    print("🔄 Processando com NMF...")
    resultados_nmf = processar_por_ano(dados, metodo="nmf", num_topics=10)
    if resultados_nmf:
        salvar_resultados(resultados_nmf, analises_dir, "nmf")
    
    print()
    print("=" * 70)
    print("✅ MODELAGEM DE TÓPICOS CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()


