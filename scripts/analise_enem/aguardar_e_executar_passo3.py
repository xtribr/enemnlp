#!/usr/bin/env python3
"""
Monitora o Passo 1 e executa o Passo 3 automaticamente quando concluir
"""
import time
import json
import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
arquivo_resultado = project_root / "data" / "analises" / "avaliacao_acuracia_maritaca.json"

def verificar_passo1_rodando():
    """Verifica se o Passo 1 está rodando"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "21_avaliacao_acuracia_maritaca.py"],
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except:
        return False

def verificar_passo1_concluido():
    """Verifica se o Passo 1 foi concluído"""
    if not arquivo_resultado.exists():
        return False
    
    try:
        with open(arquivo_resultado, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar se tem resultado geral
        if '_geral' in data:
            geral = data['_geral']
            total = geral.get('total_questoes', 0)
            # Se processou mais de 2000 questões, provavelmente concluiu
            if total > 2000:
                return True
        
        # Verificar se processou todos os anos esperados (17 anos)
        anos_processados = [k for k in data.keys() if k != '_geral' and isinstance(data[k], dict)]
        if len(anos_processados) >= 15:  # Pelo menos 15 anos
            return True
        
        return False
    except:
        return False

def obter_progresso():
    """Obtém progresso atual do Passo 1"""
    if not arquivo_resultado.exists():
        return None
    
    try:
        with open(arquivo_resultado, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total = 0
        acertos = 0
        anos_processados = []
        
        for ano, dados in data.items():
            if ano == '_geral':
                continue
            if isinstance(dados, dict) and 'estatisticas' in dados:
                stats = dados['estatisticas']
                total += stats.get('total', 0)
                acertos += stats.get('acertos', 0)
                anos_processados.append(ano)
        
        if total > 0:
            acuracia = (acertos / total) * 100
            return {
                'total': total,
                'acertos': acertos,
                'acuracia': acuracia,
                'anos': sorted(anos_processados)
            }
    except:
        pass
    
    return None

def executar_passo3():
    """Executa o Passo 3"""
    print("\n" + "=" * 70)
    print("🚀 INICIANDO PASSO 3: Análise de Complexidade com Maritaca")
    print("=" * 70)
    print()
    
    script_passo3 = project_root / "scripts" / "analise_enem" / "19_integracao_maritaca.py"
    
    # Verificar se API key está configurada
    import os
    api_key = os.environ.get("CURSORMINIMAC")
    if not api_key:
        print("⚠️  CURSORMINIMAC não configurada!")
        print("   Configure com: export CURSORMINIMAC='sua-chave-aqui'")
        return False
    
    try:
        # Executar Passo 3
        result = subprocess.run(
            [sys.executable, str(script_passo3)],
            cwd=str(project_root),
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n✅ PASSO 3 CONCLUÍDO COM SUCESSO!")
            return True
        else:
            print(f"\n❌ Passo 3 terminou com código de erro: {result.returncode}")
            return False
    except Exception as e:
        print(f"\n❌ Erro ao executar Passo 3: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 MONITORAMENTO AUTOMÁTICO - Passo 1 → Passo 3")
    print("=" * 70)
    print()
    print("🔄 Monitorando Passo 1...")
    print("   Quando concluir, executarei o Passo 3 automaticamente")
    print("   Pressione Ctrl+C para parar o monitoramento")
    print()
    
    ultimo_progresso = None
    tentativas_sem_mudanca = 0
    
    while True:
        # Verificar se Passo 1 está rodando
        if not verificar_passo1_rodando():
            print("⚠️  Passo 1 não está rodando")
            print("   Verificando se já concluiu...")
            
            if verificar_passo1_concluido():
                print("✅ Passo 1 já foi concluído!")
                break
            else:
                print("❌ Passo 1 não está rodando e não concluiu")
                print("   Execute o Passo 1 primeiro:")
                print("   python scripts/analise_enem/21_avaliacao_acuracia_maritaca.py")
                return
        
        # Obter progresso
        progresso = obter_progresso()
        
        if progresso:
            # Mostrar progresso se mudou
            if progresso != ultimo_progresso:
                print(f"\n📊 Progresso: {progresso['total']} questões processadas")
                print(f"   Acurácia parcial: {progresso['acuracia']:.2f}%")
                print(f"   Anos processados: {len(progresso['anos'])}")
                ultimo_progresso = progresso
                tentativas_sem_mudanca = 0
            else:
                tentativas_sem_mudanca += 1
                
                # Se não mudou por muito tempo, verificar se concluiu
                if tentativas_sem_mudanca >= 10:  # 5 minutos sem mudança
                    if verificar_passo1_concluido():
                        print("\n✅ Passo 1 concluído (detectado por inatividade)")
                        break
        else:
            print(".", end="", flush=True)
        
        # Verificar se concluiu
        if verificar_passo1_concluido():
            print("\n✅ Passo 1 CONCLUÍDO!")
            break
        
        time.sleep(30)  # Verificar a cada 30 segundos
    
    # Mostrar resultados finais do Passo 1
    if arquivo_resultado.exists():
        try:
            with open(arquivo_resultado, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if '_geral' in data:
                geral = data['_geral']
                print("\n" + "=" * 70)
                print("📊 RESULTADOS FINAIS DO PASSO 1")
                print("=" * 70)
                print(f"Total de questões: {geral.get('total_questoes', 0)}")
                print(f"Total de acertos: {geral.get('total_acertos', 0)}")
                print(f"Acurácia geral: {geral.get('acuracia_geral', 0):.2f}%")
                
                if geral.get('acuracia_geral', 0) >= 90:
                    print("\n🎉 OBJETIVO ALCANÇADO! Acurácia >= 90%")
                else:
                    diferenca = 90 - geral.get('acuracia_geral', 0)
                    print(f"\n📈 Faltam {diferenca:.2f}% para alcançar 90%")
        except:
            pass
    
    # Executar Passo 3
    print("\n" + "=" * 70)
    executar_passo3()
    
    print("\n" + "=" * 70)
    print("✅ MONITORAMENTO CONCLUÍDO")
    print("=" * 70)
    print("\n📁 Resultados salvos em:")
    print("   - data/analises/avaliacao_acuracia_maritaca.json")
    print("   - data/analises/analise_complexidade_maritaca.json")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoramento interrompido pelo usuário")
        sys.exit(0)


