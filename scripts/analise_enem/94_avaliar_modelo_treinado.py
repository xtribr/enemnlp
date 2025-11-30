#!/usr/bin/env python3
"""
📊 AVALIAR MODELO TREINADO - ENEM

Avalia modelo NLP treinado no conjunto de teste.

Metodologia correta:
1. Carregar modelo treinado
2. Avaliar em conjunto de teste
3. Calcular métricas (acurácia geral, por área, por dificuldade)
4. Gerar relatório completo
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("❌ transformers não instalado")
    print("   Execute: pip install transformers torch")

def carregar_modelo_treinado(model_dir: Path):
    """Carrega modelo e tokenizer treinados"""
    print(f"📥 Carregando modelo de: {model_dir}")
    
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
    model.eval()
    
    print("✅ Modelo carregado")
    return model, tokenizer

def carregar_dataset_teste(training_dir: Path) -> List[Dict]:
    """Carrega conjunto de teste"""
    arquivo = training_dir / "test.jsonl"
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return None
    
    dados = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                dados.append(json.loads(line))
    
    print(f"✅ {len(dados)} questões de teste carregadas")
    return dados

def prever_resposta(model, tokenizer, texto: str) -> str:
    """Faz predição usando modelo treinado"""
    # Tokenizar
    encoded = tokenizer(
        texto,
        truncation=True,
        padding='max_length',
        max_length=512,
        return_tensors='pt'
    )
    
    # Predição
    with torch.no_grad():
        outputs = model(**encoded)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = predictions.argmax(dim=-1).item()
    
    # Mapear de volta para letra
    label_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    return label_map.get(predicted_class, 'A')

def avaliar_modelo(model, tokenizer, dataset_teste: List[Dict]) -> Dict:
    """Avalia modelo no conjunto de teste"""
    print("\n🔄 Avaliando modelo...")
    
    resultados = []
    correct_count = 0
    
    for i, item in enumerate(dataset_teste):
        texto = item['input']
        resposta_correta = item['output']
        
        # Predição
        resposta_predita = prever_resposta(model, tokenizer, texto)
        
        # Verificar acerto
        acerto = resposta_predita == resposta_correta
        if acerto:
            correct_count += 1
        
        resultados.append({
            'id': item.get('id', ''),
            'ano': item.get('ano'),
            'area': item.get('area', ''),
            'resposta_correta': resposta_correta,
            'resposta_predita': resposta_predita,
            'acerto': acerto
        })
        
        if (i + 1) % 50 == 0:
            print(f"   Processadas: {i + 1}/{len(dataset_teste)}")
    
    # Calcular métricas
    acuracia_geral = (correct_count / len(dataset_teste)) * 100 if dataset_teste else 0
    
    # Por área
    stats_area = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in resultados:
        area = r.get('area', 'unknown')
        stats_area[area]['total'] += 1
        if r['acerto']:
            stats_area[area]['correct'] += 1
    
    acuracia_por_area = {}
    for area, stats in stats_area.items():
        acuracia_por_area[area] = {
            'acuracia': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0,
            'correct': stats['correct'],
            'total': stats['total']
        }
    
    # Por ano
    stats_ano = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in resultados:
        ano = r.get('ano')
        if ano:
            stats_ano[ano]['total'] += 1
            if r['acerto']:
                stats_ano[ano]['correct'] += 1
    
    acuracia_por_ano = {}
    for ano, stats in sorted(stats_ano.items()):
        acuracia_por_ano[ano] = {
            'acuracia': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0,
            'correct': stats['correct'],
            'total': stats['total']
        }
    
    return {
        'acuracia_geral': acuracia_geral,
        'total_questoes': len(dataset_teste),
        'correct': correct_count,
        'acuracia_por_area': acuracia_por_area,
        'acuracia_por_ano': acuracia_por_ano,
        'resultados': resultados
    }

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 AVALIAÇÃO DE MODELO TREINADO - ENEM")
    print("=" * 70)
    print()
    
    if not HAS_TRANSFORMERS:
        print("❌ Dependências não instaladas")
        return
    
    project_root = Path(__file__).parent.parent.parent
    models_dir = project_root / "data" / "models"
    model_dir = models_dir / "enem_bert_trained"
    training_dir = project_root / "data" / "training"
    results_dir = project_root / "results"
    
    # Verificar modelo
    if not model_dir.exists():
        print(f"❌ Modelo não encontrado: {model_dir}")
        print("   Execute primeiro: python scripts/analise_enem/93_treinar_modelo_enem.py")
        return
    
    # Carregar modelo
    model, tokenizer = carregar_modelo_treinado(model_dir)
    
    # Carregar dataset de teste
    print("\n📥 Carregando dataset de teste...")
    dataset_teste = carregar_dataset_teste(training_dir)
    
    if not dataset_teste:
        return
    
    # Avaliar
    resultados = avaliar_modelo(model, tokenizer, dataset_teste)
    
    # Mostrar resultados
    print("\n" + "=" * 70)
    print("📊 RESULTADOS DA AVALIAÇÃO")
    print("=" * 70)
    print()
    print(f"Acurácia Geral: {resultados['acuracia_geral']:.2f}%")
    print(f"Acertos: {resultados['correct']}/{resultados['total_questoes']}")
    print()
    
    print("📊 Por Área:")
    for area, stats in sorted(resultados['acuracia_por_area'].items()):
        print(f"   {area:20s}: {stats['acuracia']:5.2f}% ({stats['correct']}/{stats['total']})")
    
    print()
    print("📊 Por Ano:")
    for ano, stats in sorted(resultados['acuracia_por_ano'].items()):
        print(f"   {ano}: {stats['acuracia']:5.2f}% ({stats['correct']}/{stats['total']})")
    
    # Salvar resultados
    results_dir.mkdir(exist_ok=True)
    results_file = results_dir / "avaliacao_modelo_treinado.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"💾 Resultados salvos em: {results_file}")
    print()
    print("=" * 70)
    print("✅ AVALIAÇÃO CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()

