#!/usr/bin/env python3
"""
🔍 ANÁLISE DE ERROS DO JSON - NATUREZA

Analisa o JSON de resultados do Colab para identificar padrões de erro.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

def analisar_json(json_path: Path):
    """Analisa JSON de resultados"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    resultados = data.get('resultados', [])
    
    print("=" * 70)
    print("🔍 ANÁLISE DE ERROS - NATUREZA")
    print("=" * 70)
    print()
    
    # Estatísticas gerais
    total = len(resultados)
    corretos = sum(1 for r in resultados if r.get('correto', False))
    erros = total - corretos
    
    print(f"📊 ESTATÍSTICAS GERAIS:")
    print(f"   Total: {total}")
    print(f"   Corretos: {corretos} ({corretos/total*100:.1f}%)")
    print(f"   Erros: {erros} ({erros/total*100:.1f}%)")
    print()
    
    # Padrões de erro (correta → errada)
    padroes_erro = Counter()
    erros_list = [r for r in resultados if not r.get('correto', False)]
    
    for erro in erros_list:
        correta = erro.get('gabarito', '')
        predita = erro.get('resposta', '')
        if correta and predita and correta != 'Anulado':
            padrao = f"{correta}→{predita}"
            padroes_erro[padrao] += 1
    
    print("🔍 TOP 10 PADRÕES DE ERRO (Correta → Errada):")
    print()
    for padrao, count in padroes_erro.most_common(10):
        pct = (count / len(erros_list)) * 100
        print(f"   {padrao:8s}: {count:2d} vezes ({pct:5.1f}% dos erros)")
    print()
    
    # Distribuição de respostas preditas
    respostas_preditas = Counter()
    respostas_corretas = Counter()
    
    for r in resultados:
        predita = r.get('resposta', '')
        correta = r.get('gabarito', '')
        if predita:
            respostas_preditas[predita] += 1
        if correta and correta != 'Anulado':
            respostas_corretas[correta] += 1
    
    print("📊 DISTRIBUIÇÃO DE RESPOSTAS:")
    print()
    print("   Preditas pelo modelo:")
    for letra in ['A', 'B', 'C', 'D', 'E']:
        count = respostas_preditas.get(letra, 0)
        pct = (count / total) * 100
        print(f"      {letra}: {count:2d} vezes ({pct:5.1f}%)")
    print()
    print("   Corretas (gabarito):")
    for letra in ['A', 'B', 'C', 'D', 'E']:
        count = respostas_corretas.get(letra, 0)
        pct = (count / total) * 100
        print(f"      {letra}: {count:2d} vezes ({pct:5.1f}%)")
    print()
    
    # Análise de confiança
    confianca_corretos = [r.get('confianca', 0) for r in resultados if r.get('correto', False)]
    confianca_erros = [r.get('confianca', 0) for r in resultados if not r.get('correto', False)]
    
    if confianca_corretos:
        print("📈 CONFIANÇA:")
        print(f"   Média (corretos): {sum(confianca_corretos)/len(confianca_corretos):.2f}")
        print(f"   Média (erros): {sum(confianca_erros)/len(confianca_erros):.2f}")
        print()
    
    # Questões que mais erraram
    print("❌ QUESTÕES COM ERRO:")
    print()
    for erro in sorted(erros_list, key=lambda x: x.get('numero', 0))[:10]:
        num = erro.get('numero', 'N/A')
        predita = erro.get('resposta', 'N/A')
        correta = erro.get('gabarito', 'N/A')
        conf = erro.get('confianca', 0)
        print(f"   Q{num}: Predita={predita}, Correta={correta}, Conf={conf:.0%}")
    print()
    
    # Análise específica: viés para E
    count_e = respostas_preditas.get('E', 0)
    pct_e = (count_e / total) * 100
    count_e_correta = respostas_corretas.get('E', 0)
    pct_e_correta = (count_e_correta / total) * 100
    
    print("⚠️  ANÁLISE DE VIÉS:")
    print()
    print(f"   Modelo escolheu 'E': {count_e} vezes ({pct_e:.1f}%)")
    print(f"   Respostas corretas 'E': {count_e_correta} vezes ({pct_e_correta:.1f}%)")
    if count_e > count_e_correta * 1.5:
        print(f"   ⚠️  VIÉS DETECTADO: Modelo escolhe 'E' {count_e/count_e_correta:.1f}x mais que o esperado!")
    print()
    
    # Salvar relatório
    relatorio = f"""# 🔍 ANÁLISE DE ERROS - NATUREZA

## 📊 RESUMO

- **Total**: {total} questões
- **Corretos**: {corretos} ({corretos/total*100:.1f}%)
- **Erros**: {erros} ({erros/total*100:.1f}%)

## 🔍 PADRÕES DE ERRO

### Top 10 Padrões (Correta → Errada)

"""
    
    for padrao, count in padroes_erro.most_common(10):
        pct = (count / len(erros_list)) * 100
        relatorio += f"- **{padrao}**: {count} vezes ({pct:.1f}% dos erros)\n"
    
    relatorio += f"""
## 📊 DISTRIBUIÇÃO DE RESPOSTAS

### Preditas pelo Modelo

"""
    for letra in ['A', 'B', 'C', 'D', 'E']:
        count = respostas_preditas.get(letra, 0)
        pct = (count / total) * 100
        relatorio += f"- {letra}: {count} vezes ({pct:.1f}%)\n"
    
    relatorio += "\n### Corretas (Gabarito)\n\n"
    for letra in ['A', 'B', 'C', 'D', 'E']:
        count = respostas_corretas.get(letra, 0)
        pct = (count / total) * 100
        relatorio += f"- {letra}: {count} vezes ({pct:.1f}%)\n"
    
    relatorio += f"""
## ⚠️  VIÉS DETECTADO

- Modelo escolheu 'E': {count_e} vezes ({pct_e:.1f}%)
- Respostas corretas 'E': {count_e_correta} vezes ({pct_e_correta:.1f}%)
- **Problema**: Modelo tem viés forte para escolher alternativa E

## 📈 CONFIANÇA

- Média (corretos): {sum(confianca_corretos)/len(confianca_corretos):.2f}
- Média (erros): {sum(confianca_erros)/len(confianca_erros):.2f}

## 💡 RECOMENDAÇÕES

1. **Corrigir viés para E**: O modelo está escolhendo E com muita frequência
2. **Melhorar prompts**: Enfatizar análise igual de todas as alternativas
3. **Revisar extração de resposta**: Verificar se está capturando corretamente
4. **Ajustar self-consistency**: Pode estar reforçando respostas erradas
"""
    
    output_file = Path(json_path).parent / f"analise_erros_{Path(json_path).stem}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"💾 Relatório salvo em: {output_file}")
    print()
    print("=" * 70)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
        # Tentar encontrar o arquivo na área de trabalho
        json_path = Path("/Users/bunker/Desktop/avaliacao_colab_natureza_20251130_182919.json")
    
    if not json_path.exists():
        print(f"❌ Arquivo não encontrado: {json_path}")
        sys.exit(1)
    
    analisar_json(json_path)

