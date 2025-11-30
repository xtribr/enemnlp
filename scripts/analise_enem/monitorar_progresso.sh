#!/bin/bash
# Script simples para monitorar progresso do Passo 1

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "📊 Monitorando progresso do Passo 1..."
echo "   Pressione Ctrl+C para parar"
echo ""

while true; do
    clear
    echo "======================================================================"
    echo "📊 PROGRESSO DO PASSO 1 - $(date '+%H:%M:%S')"
    echo "======================================================================"
    echo ""
    
    python3 scripts/analise_enem/verificar_progresso.py 2>&1
    
    echo ""
    echo "🔄 Atualizando a cada 30 segundos..."
    echo "   Pressione Ctrl+C para parar"
    
    sleep 30
done


