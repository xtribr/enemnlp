#!/usr/bin/env python3
"""
Testa num_fewshot 5 para ver se mais exemplos ajudam
Compara com num_fewshot 3
"""
import subprocess
import sys
import json
from pathlib import Path
import time

def executar_avaliacao_fewshot(num_fewshot: int, num_questoes: int = 50):
    """Executa avaliação com num_fewshot específico"""
    project_root = Path(__file__).parent.parent.parent
    
    print(f"🚀 Executando avaliação com num_fewshot={num_fewshot}...")
    print(f"   Questões: {num_questoes}")
    print()
    
    # Comando
    cmd = [
        "python", "main.py",
        "--model", "maritalk",
        "--model_args", "engine=sabia-3",
        "--tasks", "enem_cot_2024_captions",
        "--description_dict_path", "description.json",
        "--num_fewshot", str(num_fewshot),
        "--conversation_template", "chatgpt",
        "--limit", str(num_questoes)
    ]
    
    # Arquivo de saída
    output_file = project_root / "results" / f"avaliacao_fewshot_{num_fewshot}.json"
    output_file.parent.mkdir(exist_ok=True)
    cmd.extend(["--output_path", str(output_file)])
    
    inicio = time.time()
    
    try:
        result = subprocess.run(cmd, cwd=project_root, check=True, capture_output=False)
        tempo_total = time.time() - inicio
        
        # Carregar e analisar resultados
        with open(output_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        resultados = dados['results']['enem_cot_2024_captions']
        
        return {
            'num_fewshot': num_fewshot,
            'acuracia_geral': resultados['acc'],
            'acuracia_math': resultados['mathematics'],
            'tempo': tempo_total,
            'arquivo': output_file
        }
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
        return None
    except KeyboardInterrupt:
        print("⏹️  Interrompido pelo usuário")
        return None

def comparar_fewshot():
    """Compara diferentes valores de num_fewshot"""
    print("=" * 70)
    print("🧪 TESTE: num_fewshot 3 vs 5")
    print("=" * 70)
    print()
    
    resultados = []
    
    # Testar few-shot 3
    print("📊 TESTE 1: num_fewshot = 3")
    print("-" * 70)
    resultado_3 = executar_avaliacao_fewshot(3, num_questoes=50)
    if resultado_3:
        resultados.append(resultado_3)
        print()
        print(f"✅ Concluído: {resultado_3['acuracia_math']*100:.2f}% em matemática")
        print()
    
    # Testar few-shot 5
    print("📊 TESTE 2: num_fewshot = 5")
    print("-" * 70)
    resultado_5 = executar_avaliacao_fewshot(5, num_questoes=50)
    if resultado_5:
        resultados.append(resultado_5)
        print()
        print(f"✅ Concluído: {resultado_5['acuracia_math']*100:.2f}% em matemática")
        print()
    
    # Comparação
    if len(resultados) == 2:
        print("=" * 70)
        print("📊 COMPARAÇÃO DE RESULTADOS")
        print("=" * 70)
        print()
        
        print("Acurácia Geral:")
        print(f"   num_fewshot 3: {resultados[0]['acuracia_geral']*100:.2f}%")
        print(f"   num_fewshot 5: {resultados[1]['acuracia_geral']*100:.2f}%")
        diferenca_geral = (resultados[1]['acuracia_geral'] - resultados[0]['acuracia_geral']) * 100
        print(f"   Diferença: {diferenca_geral:+.2f}%")
        print()
        
        print("Acurácia Matemática:")
        print(f"   num_fewshot 3: {resultados[0]['acuracia_math']*100:.2f}%")
        print(f"   num_fewshot 5: {resultados[1]['acuracia_math']*100:.2f}%")
        diferenca_math = (resultados[1]['acuracia_math'] - resultados[0]['acuracia_math']) * 100
        print(f"   Diferença: {diferenca_math:+.2f}%")
        print()
        
        if diferenca_math > 0:
            print(f"✅ num_fewshot 5 é MELHOR (+{diferenca_math:.2f}%)")
        elif diferenca_math < 0:
            print(f"⚠️  num_fewshot 3 é melhor ({diferenca_math:.2f}%)")
        else:
            print("➡️  Empate")
        print()
        
        print("Tempo de execução:")
        print(f"   num_fewshot 3: {resultados[0]['tempo']:.1f}s")
        print(f"   num_fewshot 5: {resultados[1]['tempo']:.1f}s")
        print()
    
    # Salvar comparação
    project_root = Path(__file__).parent.parent.parent
    arquivo_comparacao = project_root / "data" / "analises" / "comparacao_fewshot.json"
    arquivo_comparacao.parent.mkdir(exist_ok=True)
    
    with open(arquivo_comparacao, 'w', encoding='utf-8') as f:
        json.dump({
            'resultados': resultados,
            'timestamp': time.time()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Comparação salva em: {arquivo_comparacao}")

def main():
    """Função principal"""
    import os
    
    # Configurar API key
    os.environ['CURSORMINIMAC'] = '107341642936117619902_e1ed52697ebc2587'
    
    comparar_fewshot()

if __name__ == "__main__":
    main()

