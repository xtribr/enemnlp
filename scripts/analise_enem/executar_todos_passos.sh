#!/bin/bash
# Script para executar os 3 passos principais em sequência

set -e

echo "======================================================================"
echo "🚀 EXECUTANDO PASSOS 1, 2 E 3 - ANÁLISES COMPLETAS"
echo "======================================================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# Verificar API key
if [ -z "$CURSORMINIMAC" ]; then
    echo "❌ CURSORMINIMAC não configurada!"
    echo "   Configure com: export CURSORMINIMAC='sua-chave-aqui'"
    exit 1
fi

echo "📊 PASSO 1: Avaliação completa com Maritaca (objetivo 90%)"
echo "----------------------------------------------------------------------"
echo "⚠️  Isso processará TODAS as questões (pode demorar 30-40 minutos)"
echo ""
python scripts/analise_enem/21_avaliacao_acuracia_maritaca.py

echo ""
echo "📊 PASSO 2: Gerar embeddings para TODAS as questões"
echo "----------------------------------------------------------------------"
echo "⚠️  Isso processará TODAS as questões (pode demorar 20-30 minutos)"
echo ""
python scripts/analise_enem/04_gerar_embeddings.py

echo ""
echo "📊 PASSO 3: Análise completa de complexidade com Maritaca"
echo "----------------------------------------------------------------------"
echo "⚠️  Isso processará TODAS as questões (pode demorar 30-40 minutos)"
echo ""
python scripts/analise_enem/19_integracao_maritaca.py

echo ""
echo "======================================================================"
echo "✅ TODOS OS PASSOS CONCLUÍDOS"
echo "======================================================================"
echo ""
echo "📁 Resultados salvos em:"
echo "   - data/analises/avaliacao_acuracia_maritaca.json"
echo "   - data/embeddings/"
echo "   - data/analises/analise_complexidade_maritaca.json"


