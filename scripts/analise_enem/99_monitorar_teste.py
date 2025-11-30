#!/usr/bin/env python3
"""
📊 MONITORAMENTO DE TESTE EM EXECUÇÃO

Monitora o progresso do teste em execução e mostra estatísticas em tempo real.
"""

import time
import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime

def monitorar_teste():
    """Monitora teste em execução"""
    log_file = Path("/tmp/teste_natureza_completo.log")
    
    if not log_file.exists():
        print("❌ Arquivo de log não encontrado")
        print("   O teste pode não estar rodando ou ainda não iniciou")
        return
    
    print("=" * 70)
    print("📊 MONITORAMENTO DE TESTE - NATUREZA (45 questões)")
    print("=" * 70)
    print()
    
    # Ler log
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Procurar por resultados
    resultados = []
    em_questao = False
    questao_atual = None
    
    for line in lines:
        line = line.strip()
        
        # Detectar início de questão
        if line.startswith('Q') and ':' in line:
            em_questao = True
            questao_atual = line.split(':')[0]
        
        # Detectar resultado
        if '✅' in line or '❌' in line:
            if '✅' in line:
                resultado = {'status': 'correct', 'line': line}
            else:
                resultado = {'status': 'error', 'line': line}
            
            # Extrair informações
            if questao_atual:
                resultado['questao'] = questao_atual
            
            resultados.append(resultado)
            em_questao = False
    
    # Estatísticas
    total_processadas = len(resultados)
    corretos = sum(1 for r in resultados if r.get('status') == 'correct')
    erros = sum(1 for r in resultados if r.get('status') == 'error')
    
    print(f"📈 PROGRESSO:")
    print(f"   Questões processadas: {total_processadas}/45")
    print(f"   Progresso: {total_processadas/45*100:.1f}%")
    print()
    
    if total_processadas > 0:
        acuracia_atual = (corretos / total_processadas) * 100
        print(f"📊 ESTATÍSTICAS ATUAIS:")
        print(f"   Corretos: {corretos}")
        print(f"   Erros: {erros}")
        print(f"   Acurácia atual: {acuracia_atual:.2f}%")
        print()
        
        # Comparação com anterior
        acuracia_anterior = 44.44
        diferenca = acuracia_atual - acuracia_anterior
        if diferenca > 0:
            print(f"📈 COMPARAÇÃO:")
            print(f"   Acurácia anterior (45 questões): {acuracia_anterior:.2f}%")
            print(f"   Acurácia atual ({total_processadas} questões): {acuracia_atual:.2f}%")
            print(f"   Diferença: {diferenca:+.2f} pontos")
        print()
    
    # Últimas questões
    if resultados:
        print("📋 ÚLTIMAS QUESTÕES PROCESSADAS:")
        for r in resultados[-5:]:
            status_icon = "✅" if r.get('status') == 'correct' else "❌"
            questao = r.get('questao', 'N/A')
            print(f"   {status_icon} {questao}")
        print()
    
    # Verificar se ainda está rodando
    import subprocess
    processo = subprocess.run(
        ['ps', 'aux'], 
        capture_output=True, 
        text=True
    )
    
    if '98_teste_prompts_revisados_local.py' in processo.stdout:
        print("🔄 TESTE AINDA EM EXECUÇÃO")
        print("   Aguarde a conclusão...")
    else:
        print("✅ TESTE CONCLUÍDO")
        print("   Verifique o arquivo de log completo para resultados finais")
    
    print()
    print("=" * 70)
    print("💡 Para atualizar: execute este script novamente")
    print("=" * 70)

if __name__ == "__main__":
    while True:
        monitorar_teste()
        print("\n⏳ Aguardando 30 segundos para próxima atualização...")
        print("   (Pressione Ctrl+C para sair)\n")
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n✅ Monitoramento encerrado")
            break

