# Status da Extração ENEM 2025

## 📊 Progresso Atual

### Linguagens (01-45)
- ✅ **45 questões extraídas** (100% completo)
- 📁 Arquivo: `data/enem/enem_2025_linguagens_imagens.jsonl`
- ✅ Todas as questões têm gabarito (label)

### Ciências Humanas (46-90)
- ✅ **45 questões processadas** (100% completo)
- ⚠️ **6 questões incompletas** (50, 52, 57, 70, 76, 81) - dados não disponíveis no JSON original
- 📁 Arquivo: `data/enem/enem_2025_humanas_imagens.jsonl`
- ✅ Todas as questões têm gabarito (label)

### Ciências da Natureza (91-135)
- ✅ **45 questões processadas** (100% completo)
- 📁 Arquivo: `data/enem/enem_2025_natureza_imagens.jsonl`
- ✅ Todas as questões têm gabarito (label)
- 📸 20 questões têm descrições de imagens

### Matemática (136-180)
- ✅ **45 questões processadas** (100% completo)
- 📁 Arquivo: `data/enem/enem_2025_matematica_imagens.jsonl`
- ✅ Todas as questões têm gabarito (label)
- 📸 22 questões têm descrições de imagens

## 📝 Questões Extraídas

### Linguagens (01-25):
1. ✅ Questão 01 - Inglês (Halloween/cultural appropriation)
2. ✅ Questão 02 - Inglês (Filosofia/Angela Davis)
3. ✅ Questão 03 - Inglês (Poema indígena)
4. ✅ Questão 04 - Inglês (Snowflake generation)
5. ✅ Questão 05 - Inglês (What is sleep? - com imagem)
6. ✅ Questão 06 - Texto "De próprio punho"
7. ✅ Questão 07 - Texto "De próprio punho"
8. ✅ Questão 08 - Texto "De próprio punho"
9. ✅ Questão 09 - Texto "De próprio punho"
10. ✅ Questão 10 - Texto "De próprio punho"
11. ✅ Questão 11 - Lei 10.639/2003
12. ✅ Questão 12 - Programa Maré Inclusiva
13. ✅ Questão 13 - Inocência (romantismo)
14. ✅ Questão 14 - Cartaz Fernando Pessoa (com imagem)
15. ✅ Questão 15 - Dalton Paula (com imagem)
16. ✅ Questão 16 - Soneto simbolista
17. ✅ Questão 17 - Texto "Antes do inverno"
18. ✅ Questão 18 - Marina (futebol/esporte)
19. ✅ Questão 19 - Atletas brasileiras (saúde mental)
20. ✅ Questão 20 - Língua de santo
21. ✅ Questão 21 - Texto "O meu medo"
22. ✅ Questão 22 - Bancos indígenas (com imagem)
23. ✅ Questão 23 - Adriana Varejão (com imagem)
24. ✅ Questão 24 - Cartaz UNICEF (com imagem)
25. ✅ Questão 25 - Texto sobre palavras automatizadas

### Ciências Humanas (46-90):
- ✅ Todas as 45 questões foram processadas do arquivo `enem_2025_linguagens_humanas.json`
- ⚠️ Questões incompletas (precisam ser preenchidas manualmente):
  - Questão 50: Tem pergunta mas sem alternativas
  - Questões 52, 57, 70, 76, 81: Completamente vazias no JSON original

## 🔄 Próximos Passos

1. ✅ **Linguagens**: Completo (45/45 questões)
2. ✅ **Humanas**: Completo (45/45 questões, 6 incompletas)
3. ✅ **Natureza**: Completo (45/45 questões)
4. ✅ **Matemática**: Completo (45/45 questões)
5. **Integração**: Integrar todas as questões ao sistema existente
6. **Completar dados**: Preencher manualmente as 6 questões incompletas de Humanas
7. **Validação**: Validar todas as questões extraídas

## 📋 Formato das Questões

As questões extraídas seguem o formato padrão:
```json
{
  "id": "enem_2025_languages_1",
  "exam": "2025",
  "area": "languages",
  "number": "1",
  "context": "...",
  "question": "...",
  "alternatives": ["A. ...", "B. ...", ...],
  "label": "D",
  "has_images": false
}
```

## 💡 Notas

- As questões com `has_images: true` têm descrições de imagens incluídas
- Todas as questões extraídas têm gabarito (label)
- Scripts utilizados:
  - `50_extrair_completo_linguas_2025.py` - Extrai questões de Linguagens (01-45)
  - `52_extrair_humanas_2025.py` - Extrai questões de Humanas (46-90)
  - `53_extrair_natureza_matematica_2025.py` - Extrai questões de Natureza (91-135) e Matemática (136-180)
- Questões incompletas são marcadas com `"incomplete": true` no JSONL
- As questões incompletas de Humanas precisam ser preenchidas manualmente a partir das imagens originais
- Questões de Natureza e Matemática foram extraídas principalmente das imagens fornecidas, com prioridade sobre o JSON original

