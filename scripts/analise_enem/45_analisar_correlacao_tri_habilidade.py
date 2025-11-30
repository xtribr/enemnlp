#!/usr/bin/env python3
"""
📊 Análise de Correlação TRI/Habilidade vs Taxa de Acerto

==========================================================

Este script analisa os resultados da avaliação e responde:
1. A TRI impacta na taxa de acerto?
2. Quais habilidades são mais difíceis para o modelo?
3. Existe correlação entre dificuldade e erro?

Uso:
    python 45_analisar_correlacao_tri_habilidade.py [arquivo_json]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
import statistics


def load_results(filepath):
    """Carrega os resultados do arquivo JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_correlation(x_values, y_values):
    """Calcula correlação de Pearson entre duas listas."""
    n = len(x_values)
    if n < 2:
        return 0
    
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    
    sum_sq_x = sum((x - mean_x) ** 2 for x in x_values)
    sum_sq_y = sum((y - mean_y) ** 2 for y in y_values)
    
    denominator = (sum_sq_x * sum_sq_y) ** 0.5
    
    if denominator == 0:
        return 0
    
    return numerator / denominator


def analyze_tri_correlation(data):
    """Analisa correlação entre TRI e taxa de acerto."""
    
    print("=" * 70)
    print("📊 ANÁLISE 1: TRI vs TAXA DE ACERTO")
    print("=" * 70)
    print()
    
    resultados = data['resultados']
    
    # Filtrar questões com TRI válido
    valid_results = [r for r in resultados if r['tri'] != 'N/A' and r['tri'] != 0]
    
    # Agrupar por faixas de TRI
    faixas = {
        "< 500": (0, 500),
        "500-550": (500, 550),
        "550-600": (550, 600),
        "600-650": (600, 650),
        "650-700": (650, 700),
        "700-750": (700, 750),
        "> 750": (750, 10000)
    }
    
    print("📈 Taxa de Acerto por Faixa de TRI:")
    print("-" * 60)
    print(f"{'Faixa TRI':<15} | {'Acurácia':>10} | {'Acertos':>12} | {'Tendência'}")
    print("-" * 60)
    
    faixa_data = []
    for faixa_nome, (tri_min, tri_max) in faixas.items():
        questoes = [r for r in valid_results 
                   if tri_min <= float(r['tri']) < tri_max]
        
        if questoes:
            acertos = sum(1 for q in questoes if q['correto'])
            total = len(questoes)
            acc = acertos / total
            
            # Determinar tendência
            if acc >= 0.9:
                tendencia = "🟢 Excelente"
            elif acc >= 0.8:
                tendencia = "🟢 Ótimo"
            elif acc >= 0.7:
                tendencia = "🟡 Bom"
            elif acc >= 0.6:
                tendencia = "🟠 Regular"
            else:
                tendencia = "🔴 Difícil"
            
            print(f"{faixa_nome:<15} | {acc:>9.1%} | {acertos:>5}/{total:<5} | {tendencia}")
            faixa_data.append((faixa_nome, acc, total))
    
    print()
    
    # Calcular correlação TRI vs Acerto
    tri_values = []
    acerto_values = []
    
    for r in valid_results:
        tri_values.append(float(r['tri']))
        acerto_values.append(1 if r['correto'] else 0)
    
    correlation = calculate_correlation(tri_values, acerto_values)
    
    print(f"📊 Correlação TRI vs Acerto: {correlation:.3f}")
    print()
    
    if correlation < -0.3:
        print("💡 CONCLUSÃO: TRI tem FORTE IMPACTO negativo na taxa de acerto")
        print("   → Quanto MAIOR o TRI, MENOR a chance de acerto")
    elif correlation < -0.1:
        print("💡 CONCLUSÃO: TRI tem IMPACTO MODERADO negativo na taxa de acerto")
        print("   → TRI influencia, mas outros fatores também são relevantes")
    else:
        print("💡 CONCLUSÃO: TRI tem BAIXO IMPACTO direto na taxa de acerto")
        print("   → O modelo não segue o padrão esperado de dificuldade")
    
    print()
    return correlation


def analyze_habilidade_correlation(data):
    """Analisa quais habilidades são mais difíceis para o modelo."""
    
    print("=" * 70)
    print("📊 ANÁLISE 2: HABILIDADE vs TAXA DE ACERTO")
    print("=" * 70)
    print()
    
    resultados = data['resultados']
    
    # Agrupar por habilidade
    hab_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'tri_sum': 0})
    
    for r in resultados:
        hab = r['habilidade']
        if hab and hab != 'N/A':
            hab_stats[hab]['total'] += 1
            if r['correto']:
                hab_stats[hab]['correct'] += 1
            if r['tri'] != 'N/A' and r['tri'] != 0:
                hab_stats[hab]['tri_sum'] += float(r['tri'])
    
    # Calcular acurácia e ordenar
    hab_list = []
    for hab, stats in hab_stats.items():
        if stats['total'] >= 1:  # Pelo menos 1 questão
            acc = stats['correct'] / stats['total']
            tri_medio = stats['tri_sum'] / stats['total'] if stats['total'] > 0 else 0
            hab_list.append({
                'hab': hab,
                'acc': acc,
                'correct': stats['correct'],
                'total': stats['total'],
                'tri_medio': tri_medio
            })
    
    # Ordenar por acurácia (piores primeiro)
    hab_list_sorted = sorted(hab_list, key=lambda x: x['acc'])
    
    print("🔴 HABILIDADES MAIS DIFÍCEIS (menor acurácia):")
    print("-" * 70)
    print(f"{'Hab':<8} | {'Acurácia':>10} | {'Acertos':>10} | {'TRI Médio':>10} | Status")
    print("-" * 70)
    
    for h in hab_list_sorted[:10]:
        if h['acc'] < 0.6:
            status = "❌ CRÍTICO"
        elif h['acc'] < 0.8:
            status = "⚠️ ATENÇÃO"
        else:
            status = "✅ OK"
        
        print(f"{h['hab']:<8} | {h['acc']:>9.1%} | {h['correct']:>4}/{h['total']:<4} | {h['tri_medio']:>10.1f} | {status}")
    
    print()
    print("🟢 HABILIDADES MAIS FÁCEIS (maior acurácia):")
    print("-" * 70)
    
    for h in sorted(hab_list, key=lambda x: -x['acc'])[:10]:
        if h['acc'] >= 0.9:
            status = "🌟 EXCELENTE"
        elif h['acc'] >= 0.8:
            status = "✅ ÓTIMO"
        else:
            status = "🟡 BOM"
        
        print(f"{h['hab']:<8} | {h['acc']:>9.1%} | {h['correct']:>4}/{h['total']:<4} | {h['tri_medio']:>10.1f} | {status}")
    
    print()
    return hab_list


def analyze_tema_comparison(data):
    """Compara desempenho entre temas."""
    
    print("=" * 70)
    print("📊 ANÁLISE 3: COMPARAÇÃO ENTRE TEMAS")
    print("=" * 70)
    print()
    
    resultados = data['resultados']
    
    # Agrupar por tema
    tema_stats = defaultdict(lambda: {
        'correct': 0, 'total': 0, 
        'tri_acertos': [], 'tri_erros': [],
        'erros_facil': 0, 'erros_dificil': 0
    })
    
    for r in resultados:
        tema = r.get('tema', 'Desconhecido')
        tema_stats[tema]['total'] += 1
        
        tri = float(r['tri']) if r['tri'] != 'N/A' and r['tri'] != 0 else None
        
        if r['correto']:
            tema_stats[tema]['correct'] += 1
            if tri:
                tema_stats[tema]['tri_acertos'].append(tri)
        else:
            if tri:
                tema_stats[tema]['tri_erros'].append(tri)
                if tri < 650:
                    tema_stats[tema]['erros_facil'] += 1
                else:
                    tema_stats[tema]['erros_dificil'] += 1
    
    print(f"{'Tema':<30} | {'Acurácia':>10} | {'TRI Médio Erros':>15} | {'Erros Fácil':>12} | {'Erros Difícil':>13}")
    print("-" * 90)
    
    # Ordenar por total de questões
    temas_ordenados = sorted(tema_stats.items(), key=lambda x: -x[1]['total'])
    
    for tema, stats in temas_ordenados:
        if stats['total'] > 0:
            acc = stats['correct'] / stats['total']
            tri_erros = statistics.mean(stats['tri_erros']) if stats['tri_erros'] else 0
            
            print(f"{tema:<30} | {acc:>9.1%} | {tri_erros:>15.1f} | {stats['erros_facil']:>12} | {stats['erros_dificil']:>13}")
    
    print()
    return tema_stats


def analyze_figura_impact(data):
    """Analisa impacto da presença de figuras."""
    
    print("=" * 70)
    print("📊 ANÁLISE 4: IMPACTO DAS FIGURAS")
    print("=" * 70)
    print()
    
    resultados = data['resultados']
    
    # Geral
    geral = {
        'com_fig': {'correct': 0, 'total': 0},
        'sem_fig': {'correct': 0, 'total': 0}
    }
    
    for r in resultados:
        if r.get('tem_figura', False):
            geral['com_fig']['total'] += 1
            if r['correto']:
                geral['com_fig']['correct'] += 1
        else:
            geral['sem_fig']['total'] += 1
            if r['correto']:
                geral['sem_fig']['correct'] += 1
    
    print(f"{'Categoria':<20} | {'Acurácia':>10} | {'Acertos':>12} | {'Total':>8}")
    print("-" * 55)
    
    acc_com = geral['com_fig']['correct'] / geral['com_fig']['total'] if geral['com_fig']['total'] > 0 else 0
    acc_sem = geral['sem_fig']['correct'] / geral['sem_fig']['total'] if geral['sem_fig']['total'] > 0 else 0
    
    print(f"{'Com Figura':<20} | {acc_com:>9.1%} | {geral['com_fig']['correct']:>4}/{geral['com_fig']['total']:<6} | {geral['com_fig']['total']:>8}")
    print(f"{'Sem Figura':<20} | {acc_sem:>9.1%} | {geral['sem_fig']['correct']:>4}/{geral['sem_fig']['total']:<6} | {geral['sem_fig']['total']:>8}")
    
    diff = acc_sem - acc_com
    diff_str = f"{diff:+.1%}" if diff != 0 else "0%"
    print(f"{'Diferença':<20} | {diff_str:>10} | {'':>12} | {'':>8}")
    
    print()
    
    # Por tema (se houver dados suficientes)
    tema_figura = defaultdict(lambda: {
        'com_fig': {'correct': 0, 'total': 0},
        'sem_fig': {'correct': 0, 'total': 0}
    })
    
    for r in resultados:
        tema = r.get('tema', 'Desconhecido')
        if r.get('tem_figura', False):
            tema_figura[tema]['com_fig']['total'] += 1
            if r['correto']:
                tema_figura[tema]['com_fig']['correct'] += 1
        else:
            tema_figura[tema]['sem_fig']['total'] += 1
            if r['correto']:
                tema_figura[tema]['sem_fig']['correct'] += 1
    
    # Mostrar apenas temas com dados suficientes
    temas_com_dados = [(t, s) for t, s in tema_figura.items() 
                       if s['com_fig']['total'] > 0 or s['sem_fig']['total'] > 0]
    
    if temas_com_dados:
        print("📊 Por Tema:")
        print("-" * 70)
        print(f"{'Tema':<30} | {'Com Figura':>12} | {'Sem Figura':>12} | {'Diferença':>12}")
        print("-" * 70)
        
        for tema, stats in sorted(temas_com_dados, key=lambda x: -(x[1]['com_fig']['total'] + x[1]['sem_fig']['total']))[:10]:
            acc_com = stats['com_fig']['correct'] / stats['com_fig']['total'] if stats['com_fig']['total'] > 0 else 0
            acc_sem = stats['sem_fig']['correct'] / stats['sem_fig']['total'] if stats['sem_fig']['total'] > 0 else 0
            diff = acc_sem - acc_com
            diff_str = f"{diff:+.1%}" if diff != 0 else "0%"
            
            if stats['com_fig']['total'] > 0 or stats['sem_fig']['total'] > 0:
                print(f"{tema[:28]:<30} | {acc_com:>11.1%} | {acc_sem:>11.1%} | {diff_str:>12}")
    
    print()
    return geral


def generate_conclusions(data, correlation):
    """Gera conclusões e recomendações."""
    
    print("=" * 70)
    print("🎯 CONCLUSÕES E RECOMENDAÇÕES")
    print("=" * 70)
    print()
    
    resultados = data['resultados']
    erros = [r for r in resultados if not r['correto']]
    
    # Análise dos erros
    erros_por_tri = defaultdict(list)
    for e in erros:
        if e['tri'] != 'N/A' and e['tri'] != 0:
            tri = float(e['tri'])
            if tri < 600:
                erros_por_tri['fácil'].append(e)
            elif tri < 700:
                erros_por_tri['médio'].append(e)
            else:
                erros_por_tri['difícil'].append(e)
    
    print("📌 DESCOBERTAS PRINCIPAIS:")
    print()
    
    # 1. Correlação TRI
    print(f"1️⃣ TRI vs ACERTO (correlação: {correlation:.3f})")
    if correlation < -0.2:
        print("   ✅ O modelo SEGUE o padrão esperado: erra mais questões difíceis (TRI alto)")
    else:
        print("   ⚠️ O modelo NÃO segue o padrão esperado: erra questões de forma irregular")
    print()
    
    # 2. Erros inesperados
    total_erros = len(erros)
    erros_faceis = len(erros_por_tri['fácil'])
    pct_erros_faceis = erros_faceis / total_erros if total_erros > 0 else 0
    
    print(f"2️⃣ ERROS EM QUESTÕES FÁCEIS:")
    print(f"   {erros_faceis} de {total_erros} erros ({pct_erros_faceis:.1%}) são em questões TRI < 600")
    if pct_erros_faceis > 0.3:
        print("   ⚠️ ALERTA: Muitos erros em questões fáceis - possível problema de interpretação")
    else:
        print("   ✅ Maioria dos erros são em questões difíceis (esperado)")
    print()
    
    # 3. Temas problemáticos
    print("3️⃣ TEMAS QUE PRECISAM ATENÇÃO:")
    metricas = data.get('metricas', {})
    por_tema = metricas.get('por_tema', {})
    
    temas_problematicos = []
    for tema, stats in por_tema.items():
        acc = stats.get('accuracy', 0)
        if acc < 0.85 and stats.get('total', 0) >= 3:  # Pelo menos 3 questões
            temas_problematicos.append((tema, acc))
    
    if temas_problematicos:
        for tema, acc in sorted(temas_problematicos, key=lambda x: x[1]):
            print(f"   ⚠️ {tema}: {acc:.1%}")
    else:
        print("   ✅ Todos os temas com acurácia adequada")
    print()
    
    # 4. Recomendações
    print("📋 RECOMENDAÇÕES:")
    print()
    print("   1. CURTO PRAZO:")
    print("      • Revisar few-shots para incluir mais exemplos com figuras/tabelas")
    print("      • Adicionar instrução específica para leitura cuidadosa de enunciados")
    print()
    print("   2. MÉDIO PRAZO:")
    print("      • Criar prompts específicos por área (LC, CH, CN, MT)")
    print("      • Testar temperatura mais baixa (0.05) para maior consistência")
    print()
    print("   3. LONGO PRAZO:")
    print("      • Fine-tuning em questões de Álgebra e Estatística")
    print("      • Ensemble de modelos para decisões borderline")
    print()


def main():
    """Função principal."""
    
    # Encontrar arquivo de resultados
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
    else:
        results_dir = Path('results')
        json_files = list(results_dir.glob('avaliacao_detalhada_*.json'))
        
        if not json_files:
            print("❌ Nenhum arquivo de resultados encontrado")
            print("   Execute primeiro: python 40_avaliar_com_logging_detalhado.py")
            sys.exit(1)
        
        filepath = max(json_files, key=lambda x: x.stat().st_mtime)
        print(f"📂 Usando arquivo mais recente: {filepath}")
    
    # Carregar dados
    data = load_results(filepath)
    
    print()
    print("=" * 70)
    print("📊 ANÁLISE DE CORRELAÇÃO TRI/HABILIDADE vs ACERTO")
    print("=" * 70)
    print()
    print(f"📁 Arquivo: {filepath}")
    print(f"📊 Total de questões: {len(data['resultados'])}")
    print(f"📈 Acurácia geral: {data['metricas']['accuracy']:.1%}")
    print()
    
    # Executar análises
    correlation = analyze_tri_correlation(data)
    analyze_habilidade_correlation(data)
    analyze_tema_comparison(data)
    analyze_figura_impact(data)
    generate_conclusions(data, correlation)
    
    print()
    print(f"✅ Análise concluída!")
    print(f"   Resultados exibidos acima")


if __name__ == "__main__":
    main()

