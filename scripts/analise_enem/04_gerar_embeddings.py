#!/usr/bin/env python3
"""
Geração de Embeddings Semânticos para Questões do ENEM

Usa modelos pré-treinados em português para gerar embeddings das questões.
"""
import json
import sys
from pathlib import Path
import numpy as np
from typing import List, Dict
import pickle

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

def gerar_embeddings_com_transformers(questoes: List[Dict], model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
    """Gera embeddings usando sentence-transformers"""
    try:
        from sentence_transformers import SentenceTransformer
        
        print(f"  📥 Carregando modelo: {model_name}")
        model = SentenceTransformer(model_name)
        
        # Preparar textos (questão + contexto)
        textos = []
        for questao in questoes:
            contexto = questao.get('context', '').strip()
            pergunta = questao.get('question', '').strip()
            texto_completo = f"{contexto} {pergunta}".strip()
            textos.append(texto_completo if texto_completo else pergunta)
        
        print(f"  🔄 Gerando embeddings para {len(textos)} questões...")
        embeddings = model.encode(textos, show_progress_bar=True, batch_size=32)
        
        return embeddings, model.get_sentence_embedding_dimension()
    
    except ImportError:
        print("  ⚠️  sentence-transformers não instalado. Instale com: pip install sentence-transformers")
        return None, None
    except Exception as e:
        print(f"  ❌ Erro ao gerar embeddings: {e}")
        return None, None

def gerar_embeddings_com_bert_pt(questoes: List[Dict], model_name: str = "neuralmind/bert-base-portuguese-cased"):
    """Gera embeddings usando BERT em português"""
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        print(f"  📥 Carregando modelo: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        model.eval()
        
        # Preparar textos
        textos = []
        for questao in questoes:
            contexto = questao.get('context', '').strip()
            pergunta = questao.get('question', '').strip()
            texto_completo = f"{contexto} {pergunta}".strip()
            textos.append(texto_completo if texto_completo else pergunta)
        
        print(f"  🔄 Gerando embeddings para {len(textos)} questões...")
        embeddings = []
        
        # Processar em batches
        batch_size = 16
        for i in range(0, len(textos), batch_size):
            batch_textos = textos[i:i+batch_size]
            
            # Tokenizar
            encoded = tokenizer(
                batch_textos,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt'
            )
            
            # Gerar embeddings
            with torch.no_grad():
                outputs = model(**encoded)
                # Usar média dos embeddings da última camada
                batch_embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
                embeddings.append(batch_embeddings)
        
        embeddings = np.vstack(embeddings)
        return embeddings, embeddings.shape[1]
    
    except ImportError:
        print("  ⚠️  transformers não instalado. Instale com: pip install transformers torch")
        return None, None
    except Exception as e:
        print(f"  ❌ Erro ao gerar embeddings: {e}")
        return None, None

def processar_por_ano(dados: Dict[int, List[Dict]], metodo: str = "sentence-transformers", 
                      anos_amostra: List[int] = None, max_questoes_por_ano: int = None) -> Dict[int, np.ndarray]:
    """Processa embeddings para todos os anos (ou amostra)"""
    embeddings_por_ano = {}
    
    print(f"🔧 Método selecionado: {metodo}")
    if anos_amostra:
        print(f"📊 Processando apenas anos: {anos_amostra}")
    if max_questoes_por_ano:
        print(f"📊 Limitando a {max_questoes_por_ano} questões por ano")
    print()
    
    anos_para_processar = anos_amostra if anos_amostra else sorted(dados.keys())
    
    for ano in anos_para_processar:
        questoes = dados[ano]
        
        # Limitar número de questões se especificado
        if max_questoes_por_ano and len(questoes) > max_questoes_por_ano:
            import random
            questoes = random.sample(questoes, max_questoes_por_ano)
            print(f"📊 Processando {ano} ({len(questoes)} questões de {len(dados[ano])} - amostra)...")
        else:
            print(f"📊 Processando {ano} ({len(questoes)} questões)...")
        
        if metodo == "sentence-transformers":
            embeddings, dim = gerar_embeddings_com_transformers(questoes)
        elif metodo == "bert-pt":
            embeddings, dim = gerar_embeddings_com_bert_pt(questoes)
        else:
            print(f"  ❌ Método desconhecido: {metodo}")
            continue
        
        if embeddings is not None:
            embeddings_por_ano[ano] = embeddings
            print(f"  ✅ Embeddings gerados: shape {embeddings.shape}, dimensão {dim}")
        else:
            print(f"  ❌ Falha ao gerar embeddings para {ano}")
        
        print()
    
    return embeddings_por_ano

def salvar_embeddings(embeddings_por_ano: Dict[int, np.ndarray], output_dir: Path):
    """Salva embeddings em arquivos"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar por ano
    for ano, embeddings in embeddings_por_ano.items():
        arquivo = output_dir / f"embeddings_{ano}.npy"
        np.save(arquivo, embeddings)
        print(f"  💾 {ano}: {embeddings.shape} salvo em {arquivo.name}")
    
    # Salvar índice
    indice = {
        'anos': list(embeddings_por_ano.keys()),
        'dimensoes': {ano: emb.shape[1] for ano, emb in embeddings_por_ano.items()},
        'total_questoes': {ano: emb.shape[0] for ano, emb in embeddings_por_ano.items()}
    }
    
    with open(output_dir / "indice_embeddings.json", 'w', encoding='utf-8') as f:
        json.dump(indice, f, indent=2, ensure_ascii=False)
    
    print(f"  💾 Índice salvo em indice_embeddings.json")

def main():
    """Função principal"""
    print("=" * 70)
    print("🧠 GERAÇÃO DE EMBEDDINGS SEMÂNTICOS - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    embeddings_dir = project_root / "data" / "embeddings"
    
    # Verificar dados
    if not processed_dir.exists():
        print(f"❌ Diretório não encontrado: {processed_dir}")
        print("   Execute primeiro: 01_carregar_dados_historico.py")
        return
    
    # Carregar dados
    print("📥 Carregando dados processados...")
    dados = carregar_dados_processados(processed_dir)
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # Escolher método (sentence-transformers é mais rápido e eficiente)
    metodo = "sentence-transformers"  # ou "bert-pt"
    
    # Processar TODOS os anos e TODAS as questões
    anos_amostra = None  # Todos os anos
    max_questoes = None   # Todas as questões
    
    # Gerar embeddings
    total_questoes = sum(len(q) for q in dados.values())
    print(f"🔄 Gerando embeddings para TODAS as questões ({total_questoes} questões, {len(dados)} anos)...")
    embeddings_por_ano = processar_por_ano(dados, metodo=metodo, 
                                          anos_amostra=anos_amostra,
                                          max_questoes_por_ano=max_questoes)
    
    if not embeddings_por_ano:
        print("❌ Nenhum embedding gerado")
        return
    
    # Salvar embeddings
    print("💾 Salvando embeddings...")
    salvar_embeddings(embeddings_por_ano, embeddings_dir)
    
    print()
    print("=" * 70)
    print("✅ GERAÇÃO DE EMBEDDINGS CONCLUÍDA")
    print("=" * 70)
    print(f"\n📁 Embeddings salvos em: {embeddings_dir}")
    print("\n💡 Próximos passos:")
    print("   1. Executar: 05_analise_lexical.py")
    print("   2. Executar: 06_modelagem_topicos.py")

if __name__ == "__main__":
    main()

