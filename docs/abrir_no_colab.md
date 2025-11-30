# 🚀 Como Abrir o BrainX no Google Colab

## Método 1: Link Direto (Recomendado)

Se o repositório estiver no GitHub, use este link:

```
https://colab.research.google.com/github/xtribr/enemnlp/blob/main/notebooks/brainx_sistema_completo_colab.ipynb
```

**Passos:**
1. Clique no link acima
2. O Colab abrirá automaticamente o notebook
3. Habilite GPU: Runtime → Change runtime type → GPU
4. Execute todas as células

---

## Método 2: Upload Manual

### Passo 1: Acessar Google Colab
1. Acesse: https://colab.research.google.com
2. Faça login com sua conta Google

### Passo 2: Fazer Upload do Notebook
1. Clique em **File → Upload notebook**
2. Selecione o arquivo: `notebooks/brainx_sistema_completo_colab.ipynb`
3. Aguarde o upload completar

### Passo 3: Habilitar GPU
1. Vá em **Runtime → Change runtime type**
2. Em **Hardware accelerator**, selecione **GPU**
3. Para melhor performance, escolha **T4** ou **V100** (se disponível)
4. Clique em **Save**

### Passo 4: Executar
1. Execute as células na ordem (Shift+Enter)
2. Configure sua chave API quando solicitado
3. Aguarde o processamento completo

---

## Método 3: Clonar do GitHub no Colab

Se preferir clonar o repositório diretamente no Colab:

```python
# Execute esta célula no Colab:
!git clone https://github.com/xtribr/enemnlp.git
%cd enemnlp
```

Depois abra o notebook:
- File → Open notebook
- Navegue até: `enemnlp/notebooks/brainx_sistema_completo_colab.ipynb`

---

## ⚙️ Configurações Recomendadas

### Para Teste Rápido
```python
QUESTOES_POR_AREA = 10
N_PASSAGENS = 3
```

### Para Avaliação Completa
```python
QUESTOES_POR_AREA = 45
N_PASSAGENS = 5
```

### Para Máxima Qualidade
```python
QUESTOES_POR_AREA = None  # Todas as questões
N_PASSAGENS = 7
```

---

## 🔑 Configurar API Key

No Colab, quando a célula pedir a chave API:

1. Cole sua chave da Maritaca quando solicitado
2. Ou configure como variável de ambiente:
   ```python
   import os
   os.environ['CURSORMINIMAC'] = 'sua_chave_aqui'
   ```

---

## 📊 Monitoramento

Durante a execução, você verá:
- ✅ Barra de progresso (tqdm)
- ✅ Resultados em tempo real (✅ ou ❌)
- ✅ Estatísticas por área
- ✅ Tempo decorrido

---

## 💾 Resultados

Os resultados são salvos automaticamente em:
- `results/avaliacao_colab_YYYYMMDD_HHMMSS.json`

Você pode baixar o arquivo:
- File → Download → results/avaliacao_colab_*.json

---

## ⚠️ Troubleshooting

### GPU não disponível
- Verifique se habilitou GPU em Runtime
- Se estiver no plano gratuito, GPU pode não estar sempre disponível
- Tente novamente mais tarde ou use Colab Pro

### Erro de API
- Verifique se a chave está correta
- Certifique-se de que a chave tem créditos disponíveis

### Timeout/Disconexão
- Colab tem limite de tempo (12h gratuito, 24h Pro)
- Salve resultados intermediários
- Use menos questões se necessário

---

*Última atualização: 30/11/2025*

