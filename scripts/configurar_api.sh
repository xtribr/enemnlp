#!/bin/bash
# 🔑 Script de Configuração da API Maritaca

echo "🔑 Configuração da API Maritaca (Sabiá-3)"
echo "=========================================="
echo ""

# Verificar se a chave foi fornecida como argumento
if [ -z "$1" ]; then
    echo "📝 Uso:"
    echo "   ./scripts/configurar_api.sh SUA_CHAVE_COMPLETA"
    echo ""
    echo "   Ou configure manualmente:"
    echo "   export CURSORMINIMAC=sua_chave_completa"
    echo ""
    echo "⚠️  Sua chave parece começar com: 107341...bc2587"
    echo "   Forneça a chave COMPLETA (sem asteriscos)"
    exit 1
fi

CHAVE=$1

# Verificar tamanho da chave (geralmente chaves API têm 40+ caracteres)
if [ ${#CHAVE} -lt 20 ]; then
    echo "⚠️  Aviso: A chave parece muito curta (${#CHAVE} caracteres)"
    echo "   Certifique-se de fornecer a chave completa"
    read -p "   Continuar mesmo assim? (s/N): " confirm
    if [ "$confirm" != "s" ] && [ "$confirm" != "S" ]; then
        exit 1
    fi
fi

# Configurar variável de ambiente
export CURSORMINIMAC="$CHAVE"

echo "✅ Variável CURSORMINIMAC configurada"
echo "   Primeiros caracteres: ${CHAVE:0:10}..."
echo "   Últimos caracteres: ...${CHAVE: -10}"
echo ""

# Verificar se openai está instalado
if ! python3 -c "import openai" 2>/dev/null; then
    echo "📦 Instalando openai..."
    pip3 install openai
fi

# Testar configuração
echo "🧪 Testando configuração..."
python3 << EOF
import os
import sys

api_key = os.getenv('CURSORMINIMAC')
if not api_key:
    print("❌ Erro: CURSORMINIMAC não está configurada")
    sys.exit(1)

try:
    import openai
    client = openai.OpenAI(
        api_key=api_key,
        base_url='https://api.maritaca.ai/v1'
    )
    print("✅ Cliente OpenAI configurado corretamente")
    print("✅ Base URL: https://api.maritaca.ai/v1")
    print("")
    print("🎉 Configuração concluída com sucesso!")
    print("")
    print("📝 Para tornar permanente, adicione ao ~/.zshrc ou ~/.bashrc:")
    print("   echo 'export CURSORMINIMAC=\"$CHAVE\"' >> ~/.zshrc")
except ImportError:
    print("❌ Erro: openai não instalado")
    print("   Execute: pip3 install openai")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Aviso: {e}")
    print("   A chave foi configurada, mas não foi possível testar a conexão")
EOF

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "🚀 Agora você pode executar:"
echo "   python scripts/analise_enem/83_teste_rapido_todas_areas.py --questoes_por_area 3"

