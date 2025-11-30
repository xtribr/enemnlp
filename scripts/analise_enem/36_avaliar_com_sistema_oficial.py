#!/usr/bin/env python3
"""
Avaliação usando Sistema Oficial do lm_eval
Usa enem_cot_2024_captions com num_fewshot 3 (82-91% em matemática)
"""
import subprocess
import sys
from pathlib import Path

def executar_avaliacao_oficial(num_questoes: int = None):
    """Executa avaliação usando sistema oficial"""
    project_root = Path(__file__).parent.parent.parent
    
    print("=" * 70)
    print("🚀 AVALIAÇÃO COM SISTEMA OFICIAL")
    print("📊 Usando: enem_cot_2024_captions + num_fewshot 3")
    print("=" * 70)
    print()
    
    # Comando base
    cmd = [
        "python", "main.py",
        "--model", "maritalk",
        "--model_args", "engine=sabia-3",
        "--tasks", "enem_cot_2024_captions",
        "--description_dict_path", "description.json",
        "--num_fewshot", "3",
        "--conversation_template", "chatgpt"
    ]
    
    # Adicionar limite se especificado
    if num_questoes:
        cmd.extend(["--limit", str(num_questoes)])
    
    # Arquivo de saída
    output_file = project_root / "results" / "avaliacao_oficial_captions.json"
    output_file.parent.mkdir(exist_ok=True)
    cmd.extend(["--output_path", str(output_file)])
    
    print("🔧 Comando a ser executado:")
    print("   " + " ".join(cmd))
    print()
    print("📊 Esta configuração deve dar 82-91% em matemática")
    print("   (vs 24-56% dos scripts customizados)")
    print()
    
    # Executar
    print("🚀 Executando avaliação...")
    print()
    
    try:
        result = subprocess.run(cmd, cwd=project_root, check=True, capture_output=False)
        print()
        print("=" * 70)
        print("✅ AVALIAÇÃO CONCLUÍDA")
        print("=" * 70)
        print(f"💾 Resultados salvos em: {output_file}")
        print()
        print("📊 Para ver os resultados:")
        print(f"   python scripts/analise_enem/37_analisar_resultados_oficial.py {output_file}")
    except subprocess.CalledProcessError as e:
        print()
        print("❌ Erro ao executar avaliação")
        print(f"   Código de saída: {e.returncode}")
        return False
    except KeyboardInterrupt:
        print()
        print("⏹️  Avaliação interrompida pelo usuário")
        return False
    
    return True

def main():
    """Função principal"""
    import sys
    
    num_questoes = None
    if len(sys.argv) > 1:
        try:
            num_questoes = int(sys.argv[1])
        except ValueError:
            print("⚠️  Argumento inválido. Usando todas as questões.")
    
    executar_avaliacao_oficial(num_questoes)

if __name__ == "__main__":
    main()

