#!/usr/bin/env python3
"""
🔍 ANÁLISE DETALHADA DE ERROS - ENEM

Analisa erros do modelo em detalhes para identificar problemas.

Foco:
1. Padrões de erro
2. Tipos de questões que mais erram
3. Respostas do modelo vs gabarito
4. Problemas na extração de resposta
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from collections import defaultdict, Counter
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_resultados(results_dir: Path) -> List[Dict]:
    """Carrega resultados de avaliação"""
    resultados = []
    
    # Procurar arquivos de resultados
    for json_file in sorted(results_dir.glob("*.json"), reverse=True):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Verificar se tem resultados
                if 'results' in data:
                    resultados.extend(data['results'])
                elif isinstance(data, list):
                    resultados.extend(data)
        except:
            continue
    
    return resultados

def analisar_padroes_erro(resultados: List[Dict]) -> Dict:
    """Analisa padrões de erro"""
    erros = [r for r in resultados if not r.get('correto', False)]
    
    # Padrões de erro (resposta correta → resposta errada)
    padroes = Counter()
    for erro in erros:
        correta = erro.get('resposta_correta', '') or erro.get('correct_label', '')
        predita = erro.get('resposta_predita', '') or erro.get('model_answer', '')
        if correta and predita:
            padrao = f"{correta}→{predita}"
            padroes[padrao] += 1
    
    # Por área
    erros_por_area = defaultdict(int)
    total_por_area = defaultdict(int)
    
    for r in resultados:
        area = r.get('area', 'unknown')
        total_por_area[area] += 1
        if not r.get('correto', False):
            erros_por_area[area] += 1
    
    acuracia_por_area = {}
    for area in total_por_area:
        total = total_por_area[area]
        erros = erros_por_area[area]
        acertos = total - erros
        acuracia_por_area[area] = {
            'acuracia': (acertos / total * 100) if total > 0 else 0,
            'acertos': acertos,
            'erros': erros,
            'total': total
        }
    
    # Por número de questão
    erros_por_numero = {}
    for erro in erros:
        num = erro.get('numero', 0) or erro.get('number', 0)
        if num:
            erros_por_numero[num] = erro
    
    return {
        'total_erros': len(erros),
        'total_questoes': len(resultados),
        'padroes_erro': dict(padroes.most_common(10)),
        'acuracia_por_area': acuracia_por_area,
        'erros_por_numero': erros_por_numero,
        'exemplos_erro': erros[:10]  # Primeiros 10 erros
    }

def analisar_extracao_resposta(resultados: List[Dict]) -> Dict:
    """Analisa se a extração de resposta está funcionando"""
    problemas_extracao = []
    
    for r in resultados:
        predita = r.get('resposta_predita', '') or r.get('model_answer', '')
        resposta_raw = r.get('model_response_raw', '') or r.get('resposta_raw', '')
        
        # Verificar se extração falhou
        if not predita and resposta_raw:
            problemas_extracao.append({
                'id': r.get('id', ''),
                'numero': r.get('numero', 0),
                'resposta_raw': resposta_raw[:200] if resposta_raw else None
            })
    
    return {
        'total_problemas_extracao': len(problemas_extracao),
        'exemplos': problemas_extracao[:5]
    }

def gerar_relatorio(analise: Dict, output_file: Path):
    """Gera relatório de análise"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    relatorio = f"""# 🔍 ANÁLISE DETALHADA DE ERROS - ENEM

## 📊 RESUMO GERAL

- **Total de questões**: {analise['total_questoes']}
- **Total de erros**: {analise['total_erros']}
- **Acurácia geral**: {(1 - analise['total_erros']/analise['total_questoes'])*100:.2f}%

## 🔍 PADRÕES DE ERRO

### Top 10 Padrões (Correta → Errada)

"""
    
    for padrao, count in list(analise['padroes_erro'].items())[:10]:
        relatorio += f"- **{padrao}**: {count} vezes\n"
    
    relatorio += "\n## 📊 ACURÁCIA POR ÁREA\n\n"
    
    for area, stats in sorted(analise['acuracia_por_area'].items()):
        relatorio += f"### {area}\n"
        relatorio += f"- Acurácia: {stats['acuracia']:.2f}%\n"
        relatorio += f"- Acertos: {stats['acertos']}/{stats['total']}\n"
        relatorio += f"- Erros: {stats['erros']}\n\n"
    
    if analise.get('problemas_extracao'):
        relatorio += "## ⚠️ PROBLEMAS NA EXTRAÇÃO DE RESPOSTA\n\n"
        relatorio += f"- Total de problemas: {analise['problemas_extracao']['total_problemas_extracao']}\n\n"
        relatorio += "### Exemplos:\n\n"
        for ex in analise['problemas_extracao']['exemplos']:
            relatorio += f"- Q{ex['numero']}: {ex['resposta_raw'][:100]}...\n"
    
    relatorio += "\n## 📋 EXEMPLOS DE ERROS\n\n"
    
    for i, erro in enumerate(analise['exemplos_erro'][:5], 1):
        relatorio += f"### Erro {i}\n"
        relatorio += f"- ID: {erro.get('id', 'N/A')}\n"
        relatorio += f"- Número: {erro.get('numero', 'N/A')}\n"
        relatorio += f"- Área: {erro.get('area', 'N/A')}\n"
        relatorio += f"- Correta: {erro.get('resposta_correta', 'N/A')}\n"
        relatorio += f"- Predita: {erro.get('resposta_predita', 'N/A')}\n"
        relatorio += "\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"💾 Relatório salvo em: {output_file}")

def main():
    """Função principal"""
    print("=" * 70)
    print("🔍 ANÁLISE DETALHADA DE ERROS - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    results_dir = project_root / "results"
    
    if not results_dir.exists():
        print(f"❌ Diretório não encontrado: {results_dir}")
        return
    
    # Carregar resultados
    print("📥 Carregando resultados...")
    resultados = carregar_resultados(results_dir)
    
    if not resultados:
        print("❌ Nenhum resultado encontrado")
        print("   Execute primeiro uma avaliação")
        return
    
    print(f"✅ {len(resultados)} resultados carregados")
    
    # Analisar
    print("\n🔄 Analisando erros...")
    analise = analisar_padroes_erro(resultados)
    analise['problemas_extracao'] = analisar_extracao_resposta(resultados)
    
    # Mostrar resumo
    print("\n📊 RESUMO:")
    print(f"   Total: {analise['total_questoes']} questões")
    print(f"   Erros: {analise['total_erros']}")
    print(f"   Acurácia: {(1 - analise['total_erros']/analise['total_questoes'])*100:.2f}%")
    
    print("\n📊 Por Área:")
    for area, stats in sorted(analise['acuracia_por_area'].items()):
        print(f"   {area:20s}: {stats['acuracia']:5.2f}% ({stats['acertos']}/{stats['total']})")
    
    print("\n🔍 Top 5 Padrões de Erro:")
    for padrao, count in list(analise['padroes_erro'].items())[:5]:
        print(f"   {padrao}: {count} vezes")
    
    if analise['problemas_extracao']['total_problemas_extracao'] > 0:
        print(f"\n⚠️  Problemas na extração: {analise['problemas_extracao']['total_problemas_extracao']}")
    
    # Gerar relatório
    print("\n💾 Gerando relatório...")
    output_file = results_dir / "analise_erros_detalhada.md"
    gerar_relatorio(analise, output_file)
    
    # Salvar JSON também
    json_file = results_dir / "analise_erros_detalhada.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(analise, f, indent=2, ensure_ascii=False)
    
    print(f"💾 JSON salvo em: {json_file}")
    
    print()
    print("=" * 70)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()

