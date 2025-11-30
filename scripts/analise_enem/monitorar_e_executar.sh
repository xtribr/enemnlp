#!/bin/bash
# Script para monitorar Passo 1 e executar 2 e 3 quando concluir

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "======================================================================"
echo "📊 MONITORAMENTO DO PASSO 1"
echo "======================================================================"
echo ""

# Verificar se Passo 1 está rodando
PASSO1_PID=$(pgrep -f "21_avaliacao_acuracia_maritaca.py" | head -1)

if [ -z "$PASSO1_PID" ]; then
    echo "⚠️  Passo 1 não está rodando. Iniciando..."
    export CURSORMINIMAC='107341642936117619902_e1ed52697ebc2587'
    nohup python scripts/analise_enem/21_avaliacao_acuracia_maritaca.py > logs/passo1.log 2>&1 &
    PASSO1_PID=$!
    echo "✅ Passo 1 iniciado (PID: $PASSO1_PID)"
    echo "📝 Logs em: logs/passo1.log"
else
    echo "✅ Passo 1 já está rodando (PID: $PASSO1_PID)"
fi

echo ""
echo "🔄 Monitorando progresso..."
echo "   Pressione Ctrl+C para parar o monitoramento"
echo ""

# Monitorar até concluir
while kill -0 $PASSO1_PID 2>/dev/null; do
    # Verificar arquivo de resultados
    if [ -f "data/analises/avaliacao_acuracia_maritaca.json" ]; then
        # Contar questões processadas
        PROCESSADAS=$(python3 -c "
import json
try:
    with open('data/analises/avaliacao_acuracia_maritaca.json') as f:
        data = json.load(f)
    total = 0
    for ano, dados in data.items():
        if isinstance(dados, dict) and 'estatisticas' in dados:
            total += dados['estatisticas'].get('total', 0)
    print(total)
except:
    print(0)
" 2>/dev/null)
        
        if [ ! -z "$PROCESSADAS" ] && [ "$PROCESSADAS" -gt 0 ]; then
            echo "📊 Progresso: $PROCESSADAS questões processadas (de 2891)"
        fi
    fi
    
    # Mostrar últimas linhas do log
    if [ -f "logs/passo1.log" ]; then
        echo "--- Últimas linhas do log ---"
        tail -5 logs/passo1.log 2>/dev/null | grep -E "(Avaliando|Acurácia|✅|❌)" || echo "Aguardando..."
    fi
    
    sleep 30  # Verificar a cada 30 segundos
done

echo ""
echo "======================================================================"
echo "✅ PASSO 1 CONCLUÍDO!"
echo "======================================================================"
echo ""

# Verificar resultados
if [ -f "data/analises/avaliacao_acuracia_maritaca.json" ]; then
    echo "📊 Resultados do Passo 1:"
    python3 -c "
import json
with open('data/analises/avaliacao_acuracia_maritaca.json') as f:
    data = json.load(f)
if '_geral' in data:
    geral = data['_geral']
    print(f\"  Total de questões: {geral['total_questoes']}\")
    print(f\"  Total de acertos: {geral['total_acertos']}\")
    print(f\"  Acurácia geral: {geral['acuracia_geral']:.2f}%\")
" 2>/dev/null || echo "  Arquivo encontrado, mas formato pode estar diferente"
fi

echo ""
echo "🚀 Iniciando Passo 2: Gerar Embeddings..."
echo "----------------------------------------------------------------------"
python scripts/analise_enem/04_gerar_embeddings.py

echo ""
echo "🚀 Iniciando Passo 3: Análise de Complexidade..."
echo "----------------------------------------------------------------------"
export CURSORMINIMAC='107341642936117619902_e1ed52697ebc2587'
python scripts/analise_enem/19_integracao_maritaca.py

echo ""
echo "======================================================================"
echo "✅ TODOS OS PASSOS CONCLUÍDOS!"
echo "======================================================================"


