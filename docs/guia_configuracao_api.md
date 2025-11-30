# 🔑 Guia de Configuração da API - BrainX

## 📋 API Utilizada

O BrainX utiliza a **API da Maritaca (Sabiá-3)** para avaliação de questões do ENEM.

**Modelo**: Sabiá-3 (Maritaca AI)  
**Base URL**: `https://api.maritaca.ai/v1`

---

## 🔧 Configuração

### Opção 1: Variável de Ambiente (Recomendado)

O sistema procura por uma das seguintes variáveis de ambiente:

```bash
# Opção A: CURSORMINIMAC (usado pelo Cursor)
export CURSORMINIMAC=sua_chave_api_aqui

# Opção B: MARITALK_API_SECRET_KEY (nome padrão Maritaca)
export MARITALK_API_SECRET_KEY=sua_chave_api_aqui
```

### Como Configurar

#### No Terminal (Linux/Mac):

```bash
# Configurar temporariamente (válido apenas nesta sessão)
export CURSORMINIMAC=sua_chave_api_aqui

# Ou adicionar ao ~/.bashrc ou ~/.zshrc (permanente)
echo 'export CURSORMINIMAC=sua_chave_api_aqui' >> ~/.zshrc
source ~/.zshrc
```

#### No Windows (PowerShell):

```powershell
# Configurar temporariamente
$env:CURSORMINIMAC="sua_chave_api_aqui"

# Ou configurar permanentemente
[System.Environment]::SetEnvironmentVariable('CURSORMINIMAC', 'sua_chave_api_aqui', 'User')
```

### Opção 2: Arquivo .env (Alternativa)

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
CURSORMINIMAC=sua_chave_api_aqui
```

E carregue antes de executar:

```bash
source .env
python scripts/analise_enem/83_teste_rapido_todas_areas.py
```

---

## 🔑 Como Obter a Chave da API

### 1. Acesse o Portal da Maritaca

- Website: https://maritaca.ai
- Ou: https://console.maritaca.ai

### 2. Crie uma Conta ou Faça Login

- Se não tem conta, crie uma gratuita
- Se já tem, faça login

### 3. Acesse a Seção de API Keys

- Vá para "API Keys" ou "Chaves de API"
- Procure por "Sabiá-3" ou "API Secret Key"

### 4. Gere ou Copie sua Chave

- Se não tem chave, gere uma nova
- Copie a chave (ela só aparece uma vez!)

### 5. Configure no Sistema

```bash
export CURSORMINIMAC=sua_chave_copiada_aqui
```

---

## ✅ Verificar Configuração

### Teste Rápido

```bash
# Verificar se a variável está configurada
echo $CURSORMINIMAC

# Ou
echo $MARITALK_API_SECRET_KEY
```

### Teste com Script

```bash
# Teste simples (vai falhar se não estiver configurado)
python scripts/analise_enem/83_teste_rapido_todas_areas.py --questoes_por_area 1 --passagens 1
```

Se estiver configurado corretamente, o script iniciará. Se não, mostrará:

```
❌ Erro: Chave API não encontrada
   Configure: export CURSORMINIMAC=...
```

---

## 📦 Dependências Necessárias

### 1. Instalar Biblioteca OpenAI

O sistema usa a biblioteca `openai` (compatível com Maritaca):

```bash
pip install openai
```

### 2. Verificar Instalação

```bash
python -c "import openai; print('✅ openai instalado')"
```

---

## 🚀 Exemplo Completo de Configuração

```bash
# 1. Instalar dependências
pip install openai

# 2. Configurar API key
export CURSORMINIMAC=sua_chave_api_maritaca_aqui

# 3. Verificar configuração
echo $CURSORMINIMAC

# 4. Executar teste rápido
python scripts/analise_enem/83_teste_rapido_todas_areas.py --questoes_por_area 3 --passagens 3
```

---

## ⚠️ Segurança

### ⚠️ NUNCA faça:

- ❌ Commitar a chave no Git
- ❌ Compartilhar a chave publicamente
- ❌ Colocar a chave diretamente no código
- ❌ Enviar a chave por email/mensagem

### ✅ SEMPRE faça:

- ✅ Usar variáveis de ambiente
- ✅ Adicionar `.env` ao `.gitignore`
- ✅ Manter a chave privada
- ✅ Rotacionar a chave periodicamente

### Arquivo .gitignore

Certifique-se de que seu `.gitignore` inclui:

```
.env
*.env
.env.local
```

---

## 🔍 Troubleshooting

### Erro: "Chave API não encontrada"

**Solução:**
```bash
# Verificar se está configurada
echo $CURSORMINIMAC

# Se vazio, configurar novamente
export CURSORMINIMAC=sua_chave_aqui
```

### Erro: "openai não instalado"

**Solução:**
```bash
pip install openai
```

### Erro: "401 Unauthorized"

**Solução:**
- Verificar se a chave está correta
- Verificar se a chave não expirou
- Gerar uma nova chave na plataforma Maritaca

### Erro: "Rate limit exceeded"

**Solução:**
- Aguardar alguns minutos
- Reduzir número de passagens (`--passagens 1`)
- Verificar limites da sua conta Maritaca

---

## 📚 Recursos Adicionais

- **Documentação Maritaca**: https://docs.maritaca.ai
- **Portal Maritaca**: https://maritaca.ai
- **Suporte**: Entre em contato com suporte@maritaca.ai

---

## 🎯 Resumo Rápido

```bash
# 1. Instalar
pip install openai

# 2. Configurar
export CURSORMINIMAC=sua_chave_aqui

# 3. Testar
python scripts/analise_enem/83_teste_rapido_todas_areas.py --questoes_por_area 3
```

---

*Documento criado em: 30/11/2025*  
*Última atualização: Configuração para Maritaca Sabiá-3*

