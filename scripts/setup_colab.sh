#!/bin/bash
# Script de setup rápido para Google Colab
# Execute no Colab com: !bash setup_colab.sh

set -e

echo "🚀 Configurando ambiente GPT-4-ENEM no Colab..."

# Verificar GPU
echo "📊 Verificando GPU..."
python3 -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"Não disponível\"}')"

# Instalar dependências principais
echo "📦 Instalando dependências..."
pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -q transformers datasets scikit-learn
pip install -q sqlitedict pytablewriter sacrebleu rouge-score
pip install -q pycountry numexpr tqdm jsonlines
pip install -q openai fschat

# Clonar repositório (se não existir)
if [ ! -d "gpt-4-enem" ]; then
    echo "📥 Clonando repositório..."
    git clone https://github.com/piresramon/gpt-4-enem.git
fi

cd gpt-4-enem

# Instalar projeto
echo "🔧 Instalando projeto..."
pip install -e . -q

# Criar diretório de resultados
mkdir -p results

echo "✅ Setup concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure sua chave API:"
echo "   import os"
echo "   os.environ['CURSORMINIMAC'] = 'sua-chave-aqui'"
echo ""
echo "2. Execute uma avaliação:"
echo "   !python main.py --model maritalk --model_args engine=sabia-3 --tasks enem_cot_2024_blind --limit 5"


