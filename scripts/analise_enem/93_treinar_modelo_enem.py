#!/usr/bin/env python3
"""
🧠 TREINAR MODELO NLP - ENEM (2009-2025)

Treina modelo transformer usando fine-tuning com dados ENEM.

Metodologia correta:
1. Carregar dataset preparado
2. Carregar modelo base (BERT em português)
3. Fine-tuning com HuggingFace Transformers
4. Avaliar durante treinamento
5. Salvar modelo treinado
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import random

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        TrainingArguments, Trainer, DataCollatorWithPadding
    )
    from datasets import Dataset
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("❌ transformers e datasets não instalados")
    print("   Execute: pip install transformers datasets torch")

def carregar_dataset(training_dir: Path) -> Dict[str, List[Dict]]:
    """Carrega datasets de treino, validação e teste"""
    datasets = {}
    
    for split in ['train', 'validation', 'test']:
        arquivo = training_dir / f"{split}.jsonl"
        if not arquivo.exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            print("   Execute primeiro: python scripts/analise_enem/92_preparar_dataset_treinamento.py")
            return None
        
        dados = []
        with open(arquivo, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    dados.append(json.loads(line))
        
        datasets[split] = dados
        print(f"✅ {split}: {len(dados)} questões")
    
    return datasets

def preparar_dataset_huggingface(dados: List[Dict], tokenizer, max_length: int = 512):
    """Prepara dataset no formato HuggingFace"""
    inputs = []
    labels = []
    
    # Mapear respostas para números
    label_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    
    for item in dados:
        texto = item['input']
        resposta = item['output']
        
        # Tokenizar
        encoded = tokenizer(
            texto,
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors='pt'
        )
        
        inputs.append({
            'input_ids': encoded['input_ids'].squeeze(),
            'attention_mask': encoded['attention_mask'].squeeze()
        })
        labels.append(label_map.get(resposta, 0))
    
    return Dataset.from_dict({
        'input_ids': [x['input_ids'] for x in inputs],
        'attention_mask': [x['attention_mask'] for x in inputs],
        'labels': labels
    })

def treinar_modelo(
    model_name: str = "neuralmind/bert-base-portuguese-cased",
    train_dataset,
    val_dataset,
    output_dir: Path,
    num_epochs: int = 3,
    batch_size: int = 16,
    learning_rate: float = 2e-5
):
    """Treina modelo usando HuggingFace Trainer"""
    
    print(f"\n📥 Carregando modelo base: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=5  # A, B, C, D, E
    )
    
    print("✅ Modelo carregado")
    
    # Preparar datasets
    print("\n🔄 Preparando datasets...")
    train_hf = preparar_dataset_huggingface(train_dataset, tokenizer)
    val_hf = preparar_dataset_huggingface(val_dataset, tokenizer)
    print("✅ Datasets preparados")
    
    # Configurar treinamento
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=0.01,
        logging_dir=str(output_dir / "logs"),
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=3,
        fp16=torch.cuda.is_available(),  # Usar GPU se disponível
    )
    
    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    # Métricas
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = predictions.argmax(axis=-1)
        accuracy = (predictions == labels).mean()
        return {'accuracy': accuracy}
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_hf,
        eval_dataset=val_hf,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    # Treinar
    print("\n🚀 Iniciando treinamento...")
    print(f"   Épocas: {num_epochs}")
    print(f"   Batch size: {batch_size}")
    print(f"   Learning rate: {learning_rate}")
    print(f"   GPU disponível: {torch.cuda.is_available()}")
    print()
    
    trainer.train()
    
    # Salvar modelo
    print("\n💾 Salvando modelo treinado...")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)
    
    print(f"✅ Modelo salvo em: {output_dir}")
    
    # Avaliar no conjunto de validação
    print("\n📊 Avaliando modelo...")
    eval_results = trainer.evaluate()
    
    print(f"   Acurácia: {eval_results.get('eval_accuracy', 0) * 100:.2f}%")
    
    return model, tokenizer, eval_results

def main():
    """Função principal"""
    print("=" * 70)
    print("🧠 TREINAMENTO DE MODELO NLP - ENEM")
    print("=" * 70)
    print()
    
    if not HAS_TRANSFORMERS:
        print("❌ Dependências não instaladas")
        return
    
    project_root = Path(__file__).parent.parent.parent
    training_dir = project_root / "data" / "training"
    models_dir = project_root / "data" / "models"
    output_dir = models_dir / "enem_bert_trained"
    
    # Verificar dataset
    if not training_dir.exists():
        print(f"❌ Diretório não encontrado: {training_dir}")
        print("   Execute primeiro: python scripts/analise_enem/92_preparar_dataset_treinamento.py")
        return
    
    # Carregar datasets
    print("📥 Carregando datasets...")
    datasets = carregar_dataset(training_dir)
    
    if not datasets:
        return
    
    # Modelo base (BERT em português)
    model_name = "neuralmind/bert-base-portuguese-cased"
    
    # Treinar
    model, tokenizer, eval_results = treinar_modelo(
        model_name=model_name,
        train_dataset=datasets['train'],
        val_dataset=datasets['validation'],
        output_dir=output_dir,
        num_epochs=3,
        batch_size=16,
        learning_rate=2e-5
    )
    
    # Salvar resultados
    results_file = output_dir / "training_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'model_name': model_name,
            'train_size': len(datasets['train']),
            'val_size': len(datasets['validation']),
            'test_size': len(datasets['test']),
            'eval_results': {k: float(v) for k, v in eval_results.items()}
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados salvos em: {results_file}")
    
    print()
    print("=" * 70)
    print("✅ TREINAMENTO CONCLUÍDO")
    print("=" * 70)
    print()
    print("💡 Próximo passo:")
    print("   python scripts/analise_enem/94_avaliar_modelo_treinado.py")

if __name__ == "__main__":
    main()

