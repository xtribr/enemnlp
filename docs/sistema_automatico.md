# 🤖 Sistema Automático de Monitoramento

## ✅ Status: ATIVO

O sistema está configurado para monitorar automaticamente o Passo 1 e executar o Passo 3 quando concluir.

---

## 🔄 Como Funciona

### 1. Monitoramento Contínuo
- ✅ Verifica o progresso do Passo 1 a cada 30 segundos
- ✅ Mostra estatísticas em tempo real
- ✅ Detecta quando o Passo 1 conclui

### 2. Execução Automática
- ✅ Quando Passo 1 concluir, executa Passo 3 automaticamente
- ✅ Mostra resultados finais
- ✅ Salva todos os resultados

---

## 📊 Processos em Execução

### Passo 1: Avaliação de Acurácia
- **Status**: 🟢 Em execução
- **Processando**: 2.891 questões
- **Tempo estimado**: 30-40 minutos

### Passo 2: Embeddings
- **Status**: 🟢 Em execução
- **Processando**: Embeddings para todas as questões
- **Tempo estimado**: 20-30 minutos

### Monitoramento Automático
- **Status**: 🟢 Ativo
- **Função**: Monitora Passo 1 e executa Passo 3
- **Log**: `logs/monitoramento.log`

---

## 📝 Como Verificar

### Ver Logs do Monitoramento:
```bash
tail -f logs/monitoramento.log
```

### Ver Progresso Atual:
```bash
python scripts/analise_enem/verificar_progresso.py
```

### Ver Processos:
```bash
ps aux | grep -E "(21_avaliacao|04_gerar|aguardar_e_executar)" | grep -v grep
```

---

## 🎯 O Que Acontecerá

1. **Passo 1 conclui** → Sistema detecta automaticamente
2. **Mostra resultados** → Acurácia geral, estatísticas
3. **Executa Passo 3** → Análise de complexidade completa
4. **Salva resultados** → Todos os arquivos finais

---

## 📁 Arquivos de Resultados

### Passo 1:
- `data/analises/avaliacao_acuracia_maritaca.json`
- Contém: avaliações, acurácia por ano, acurácia geral

### Passo 2:
- `data/embeddings/embeddings_*.npy` (um por ano)
- `data/embeddings/indice_embeddings.json`

### Passo 3:
- `data/analises/analise_complexidade_maritaca.json`
- Contém: complexidade, conceitos principais, justificativas

---

## ⏱️ Tempo Estimado

- **Passo 1**: 30-40 minutos (em execução)
- **Passo 2**: 20-30 minutos (em execução)
- **Passo 3**: 30-40 minutos (aguardando)
- **Total**: 80-110 minutos

---

## ✅ Checklist

- [x] Passo 1 em execução
- [x] Passo 2 em execução
- [x] Monitoramento ativo
- [ ] Passo 1 concluído
- [ ] Passo 2 concluído
- [ ] Passo 3 executado automaticamente
- [ ] Acurácia >= 90% alcançada

---

**Status**: 🟢 **SISTEMA AUTOMÁTICO ATIVO**

**Última atualização**: Monitoramento iniciado, aguardando conclusão do Passo 1


