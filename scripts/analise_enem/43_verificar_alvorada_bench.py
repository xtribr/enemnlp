#!/usr/bin/env python3
"""
Verifica disponibilidade de ENEM 2025 no dataset Alvorada-bench

Dataset: https://huggingface.co/datasets/HenriqueGodoy/Alvorada-bench
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from datasets import load_dataset
    
    print("=" * 70)
    print("📊 VERIFICAÇÃO DO DATASET ALVORADA-BENCH")
    print("=" * 70)
    print()
    
    print("📥 Carregando dataset...")
    dataset = load_dataset("HenriqueGodoy/Alvorada-bench", "questions", split="train")
    
    print(f"✅ Dataset carregado! Total: {len(dataset)} questões")
    print()
    
    # Verificar ENEM 2025
    enem_2025 = dataset.filter(lambda x: x.get('exam_year') == 2025 and 
                                          x.get('exam_type') == 'enem')
    
    print(f"📊 ENEM 2025 no dataset:")
    print(f"   Total encontrado: {len(enem_2025)} questões")
    print()
    
    if len(enem_2025) == 0:
        print("❌ ENEM 2025 NÃO está disponível no Alvorada-bench")
        print()
        print("📋 Anos ENEM disponíveis:")
        enem_anos = set([q.get('exam_year') for q in dataset 
                        if q.get('exam_type') == 'enem' and q.get('exam_year')])
        print(f"   {sorted(enem_anos)}")
        print()
        print("📋 Exames de 2025 disponíveis:")
        exams_2025 = {}
        for q in dataset:
            if q.get('exam_year') == 2025:
                exam_type = q.get('exam_type', 'unknown')
                exams_2025[exam_type] = exams_2025.get(exam_type, 0) + 1
        
        for exam_type, count in sorted(exams_2025.items()):
            print(f"   {exam_type}: {count} questões")
        print()
        print("💡 Conclusão:")
        print("   O dataset Alvorada-bench contém ENEM até 2024.")
        print("   Para ENEM 2025, precisamos usar os arquivos JSON fornecidos.")
        print("   Atualmente temos 118 questões processadas de 180 esperadas.")
    else:
        print("✅ ENEM 2025 encontrado!")
        print()
        # Verificar distribuição
        subjects = {}
        for q in enem_2025:
            subject = q.get('subject', 'unknown')
            subjects[subject] = subjects.get(subject, 0) + 1
        
        print("📊 Distribuição por área:")
        for subject, count in sorted(subjects.items()):
            print(f"   {subject}: {count} questões")
        
        if len(enem_2025) == 180:
            print()
            print("✅ Dataset completo com todas as 180 questões!")
        else:
            print()
            print(f"⚠️  Faltam {180 - len(enem_2025)} questões")
    
    print()
    print("=" * 70)

except ImportError:
    print("❌ Biblioteca 'datasets' não instalada")
    print("   Instale com: pip install datasets")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

