#!/usr/bin/env python3
"""
Monitora o progresso do treinamento em tempo real
"""
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def monitorar_treinamento():
    """Monitora progresso do treinamento"""
    project_root = Path(__file__).parent.parent.parent
    analises_dir = project_root / "data" / "analises"
    
    print("=" * 70)
    print("📊 MONITORAMENTO DO TREINAMENTO")
    print("=" * 70)
    print()
    
    iteracoes_encontradas = []
    ultima_iteracao = 0
    
    while True:
        # Verificar iterações
        arquivos_iteracao = sorted(analises_dir.glob("treinamento_iteracao_*.json"))
        
        if len(arquivos_iteracao) > ultima_iteracao:
            # Nova iteração encontrada
            for arquivo in arquivos_iteracao[ultima_iteracao:]:
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                        iteracoes_encontradas.append(dados)
                        ultima_iteracao += 1
                        
                        print(f"✅ Iteração {dados['iteracao']} concluída!")
                        print(f"   Acertos: {dados['acertos']}/{dados['total']}")
                        print(f"   Acurácia: {dados['acuracia']:.2f}%")
                        print(f"   Tempo: {dados['tempo']:.1f}s")
                        print()
                except:
                    pass
        
        # Verificar se treinamento completo foi finalizado
        arquivo_final = analises_dir / "treinamento_completo_maritaca.json"
        if arquivo_final.exists():
            print("=" * 70)
            print("🎉 TREINAMENTO COMPLETO FINALIZADO!")
            print("=" * 70)
            print()
            
            with open(arquivo_final, 'r', encoding='utf-8') as f:
                dados_final = json.load(f)
            
            print("📊 Resumo Final:")
            print()
            for iteracao in dados_final.get('iteracoes', []):
                print(f"   Iteração {iteracao['iteracao']}: {iteracao['acuracia']:.2f}% ({iteracao['acertos']}/{iteracao['total']})")
            
            melhor = dados_final.get('melhor_iteracao', {})
            print()
            print(f"🏆 Melhor iteração: {melhor.get('iteracao', 'N/A')} com {melhor.get('acuracia', 0):.2f}%")
            print()
            print(f"💾 Resultados completos em: {arquivo_final}")
            break
        
        # Mostrar status atual
        if iteracoes_encontradas:
            print(f"⏳ Aguardando próxima iteração... (Atual: {ultima_iteracao} iterações)")
        else:
            print("⏳ Aguardando início do treinamento...")
        
        time.sleep(5)  # Verificar a cada 5 segundos

if __name__ == "__main__":
    try:
        monitorar_treinamento()
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoramento interrompido pelo usuário")

