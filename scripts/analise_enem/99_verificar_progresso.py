#!/usr/bin/env python3
"""
📊 VERIFICADOR DE PROGRESSO RÁPIDO

Verifica rapidamente o status do teste em execução.
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def verificar_progresso():
    """Verifica progresso do teste"""
    print("=" * 70)
    print("📊 STATUS DO TESTE - NATUREZA (45 questões)")
    print("=" * 70)
    print()
    
    # 1. Verificar processo
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    processos = [line for line in result.stdout.split('\n') 
                 if '99_teste_completo' in line and 'grep' not in line]
    
    if processos:
        print("✅ Processo ATIVO")
        # Extrair tempo de execução
        for proc in processos:
            parts = proc.split()
            if len(parts) > 9:
                print(f"   PID: {parts[1]}")
                print(f"   Status: Rodando")
        print()
    else:
        print("❌ Processo NÃO encontrado")
        print("   O teste pode ter terminado")
        print()
    
    # 2. Verificar arquivo de progresso
    results_dir = Path("results")
    arquivo_progresso = results_dir / "teste_completo_natural-sciences_PROGRESSO.json"
    
    if arquivo_progresso.exists():
        print("✅ Arquivo de progresso encontrado!")
        print()
        
        with open(arquivo_progresso, 'r') as f:
            data = json.load(f)
        
        total_atual = data.get('total', 0)
        total_final = data.get('total_final', 45)
        corretos = data.get('correct', 0)
        acuracia = data.get('accuracy', 0)
        tempo_total = data.get('tempo_total', 0)
        
        print(f"📊 PROGRESSO: {total_atual}/{total_final} questões ({total_atual/total_final*100:.1f}%)")
        print(f"✅ Acertos: {corretos}/{total_atual}")
        print(f"🎯 Acurácia: {acuracia:.2f}%")
        print(f"⏱️  Tempo: {tempo_total/60:.1f} min")
        
        if total_atual > 0:
            tempo_medio = tempo_total / total_atual
            tempo_restante = tempo_medio * (total_final - total_atual)
            print(f"⏱️  Restante: ~{tempo_restante/60:.1f} min")
        
        # Verificar viés
        dist_predita = data.get('distribuicao_predita', {})
        dist_correta = data.get('distribuicao_correta', {})
        count_e_predita = dist_predita.get('E', 0)
        count_e_correta = dist_correta.get('E', 0)
        
        if count_e_predita > count_e_correta * 1.5 and total_atual > 10:
            print(f"\n⚠️  VIÉS: E escolhida {count_e_predita} vezes")
        else:
            print(f"\n✅ Sem viés para E")
        
        if total_atual >= total_final:
            print("\n✅ TESTE CONCLUÍDO!")
        
    else:
        print("⏳ Arquivo de progresso ainda não criado")
        print("   (Será criado após processar 5 questões)")
        print()
        print("💡 O teste está processando as primeiras questões...")
        print("   Estimativa: ~30 minutos no total")
    
    # 3. Verificar arquivos finais
    print()
    print("📁 Verificando arquivos finais...")
    arquivos_finais = sorted(results_dir.glob("teste_completo_natural-sciences_*.json"),
                            key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Filtrar arquivo de progresso
    arquivos_finais = [a for a in arquivos_finais if 'PROGRESSO' not in a.name]
    
    if arquivos_finais:
        arquivo_mais_recente = arquivos_finais[0]
        mod_time = datetime.fromtimestamp(arquivo_mais_recente.stat().st_mtime)
        
        # Verificar se é completo (45 questões)
        try:
            with open(arquivo_mais_recente, 'r') as f:
                data = json.load(f)
            if data.get('total', 0) == 45:
                print(f"✅ Teste completo encontrado: {arquivo_mais_recente.name}")
                print(f"   Acurácia: {data.get('accuracy', 0)*100:.2f}%")
                print(f"   Modificado: {mod_time.strftime('%H:%M:%S')}")
        except:
            pass
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    verificar_progresso()

