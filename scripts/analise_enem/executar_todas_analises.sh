#!/bin/bash
# Script para executar todas as análises do ENEM em sequência

set -e

echo "======================================================================"
echo "🚀 EXECUTANDO TODAS AS ANÁLISES DO ENEM"
echo "======================================================================"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# Verificar se dados estão carregados
if [ ! -d "data/processed" ] || [ -z "$(ls -A data/processed/*.jsonl 2>/dev/null)" ]; then
    echo "❌ Dados não encontrados. Execute primeiro:"
    echo "   python scripts/analise_enem/01_carregar_dados_historico.py"
    exit 1
fi

echo "📊 FASE 1: Análises Básicas"
echo "----------------------------------------------------------------------"
echo "1. Normalizando dados..."
python scripts/analise_enem/02_normalizar_dados.py

echo ""
echo "2. Validando dados..."
python scripts/analise_enem/03_validar_dados.py

echo ""
echo "📊 FASE 2: Análises Semânticas (OPCIONAL - requer dependências)"
echo "----------------------------------------------------------------------"
echo "3. Gerando embeddings..."
echo "   ⚠️  Instale: pip install sentence-transformers"
# python scripts/analise_enem/04_gerar_embeddings.py

echo ""
echo "4. Modelagem de tópicos..."
echo "   ⚠️  Instale: pip install scikit-learn nltk"
# python scripts/analise_enem/06_modelagem_topicos.py

echo ""
echo "📊 FASE 3: Análises de Dificuldade e Similaridade"
echo "----------------------------------------------------------------------"
echo "5. Análise de dificuldade..."
python scripts/analise_enem/08_heuristica_dificuldade.py

echo ""
echo "6. Similaridade entre provas..."
python scripts/analise_enem/09_similaridade_provas.py

echo ""
echo "📊 FASE 4: Análises Temporais"
echo "----------------------------------------------------------------------"
echo "7. Série temporal..."
python scripts/analise_enem/11_serie_temporal.py

echo ""
echo "8. Modelos preditivos..."
python scripts/analise_enem/14_modelo_tendencias.py

echo ""
echo "📊 FASE 5: Visualizações"
echo "----------------------------------------------------------------------"
echo "9. Gerando visualizações..."
echo "   ⚠️  Instale: pip install matplotlib seaborn"
# python scripts/analise_enem/17_visualizacoes.py

echo ""
echo "📊 FASE 6: Integração com API Maritaca (OPCIONAL)"
echo "----------------------------------------------------------------------"
echo "10. Análise com API Maritaca..."
echo "    ⚠️  Requer chave API configurada"
echo "    ⚠️  Pode consumir créditos"
# python scripts/analise_enem/19_integracao_maritaca.py

echo ""
echo "======================================================================"
echo "✅ TODAS AS ANÁLISES CONCLUÍDAS"
echo "======================================================================"
echo ""
echo "📁 Resultados salvos em:"
echo "   - data/analises/"
echo "   - reports/"
echo ""
echo "💡 Para análises opcionais, instale dependências e descomente os comandos"


