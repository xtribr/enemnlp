#!/usr/bin/env python3
"""
Análise detalhada dos erros do Passo 1 para melhorar o prompt
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def analisar_erros():
    """Analisa erros detalhadamente"""
    arquivo = Path(__file__).parent.parent.parent / "data" / "analises" / "avaliacao_acuracia_maritaca.json"
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    erros = []
    acertos = []
    
    for ano, dados in data.items():
        if ano == '_geral':
            continue
        if isinstance(dados, dict) and 'avaliacoes' in dados:
            for aval in dados['avaliacoes']:
                if not aval.get('acerto', False):
                    erros.append({
                        'ano': ano,
                        'area': aval.get('area', 'desconhecida'),
                        'id': aval.get('id', ''),
                        'resposta_correta': aval.get('resposta_correta'),
                        'resposta_ia': aval.get('resposta_ia')
                    })
                else:
                    acertos.append(aval.get('area', 'desconhecida'))
    
    print("=" * 70)
    print("📊 ANÁLISE DETALHADA DE ERROS")
    print("=" * 70)
    print()
    print(f"Total de erros: {len(erros)}")
    print(f"Total de acertos: {len(acertos)}")
    print(f"Taxa de erro: {len(erros)/(len(erros)+len(acertos))*100:.2f}%")
    print()
    
    # Erros por área
    erros_por_area = defaultdict(int)
    acertos_por_area = defaultdict(int)
    
    for erro in erros:
        erros_por_area[erro['area']] += 1
    for acerto in acertos:
        acertos_por_area[acerto] += 1
    
    print("📊 Erros e acurácia por área:")
    for area in set(list(erros_por_area.keys()) + list(acertos_por_area.keys())):
        erros_area = erros_por_area.get(area, 0)
        acertos_area = acertos_por_area.get(area, 0)
        total_area = erros_area + acertos_area
        if total_area > 0:
            acuracia_area = (acertos_area / total_area) * 100
            print(f"   {area:20s}: {erros_area:3d} erros, {acertos_area:3d} acertos, {acuracia_area:5.2f}% acurácia")
    
    print()
    
    # Padrões de erro
    padroes = defaultdict(int)
    for erro in erros:
        correta = erro['resposta_correta']
        ia = erro['resposta_ia']
        if correta and ia:
            padroes[f'{correta}→{ia}'] += 1
    
    print("📊 Padrões de erro mais comuns:")
    for padrao, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {padrao:10s}: {count:3d} vezes ({count/len(erros)*100:.1f}% dos erros)")
    
    print()
    
    # Análise de confusão
    print("📊 Matriz de confusão (resposta correta → resposta da IA):")
    confusao = defaultdict(lambda: defaultdict(int))
    for erro in erros:
        correta = erro['resposta_correta']
        ia = erro['resposta_ia']
        if correta and ia:
            confusao[correta][ia] += 1
    
    letras = ['A', 'B', 'C', 'D', 'E']
    print("   ", end="")
    for l in letras:
        print(f"{l:>6}", end="")
    print()
    for correta in letras:
        print(f"{correta}:", end="")
        for ia in letras:
            count = confusao[correta].get(ia, 0)
            print(f"{count:>6}", end="")
        print()
    
    print()
    
    # Recomendações
    print("💡 RECOMENDAÇÕES PARA MELHORAR O PROMPT:")
    print()
    
    # Área com mais erros
    area_mais_erros = max(erros_por_area.items(), key=lambda x: x[1])
    print(f"1. Área com mais erros: {area_mais_erros[0]} ({area_mais_erros[1]} erros)")
    print("   → Adicionar contexto específico para esta área no prompt")
    
    # Padrão mais comum
    padrao_mais_comum = max(padroes.items(), key=lambda x: x[1])
    print(f"2. Padrão de erro mais comum: {padrao_mais_comum[0]}")
    print("   → A IA tende a escolher {padrao_mais_comum[0].split('→')[1]} quando a resposta correta é {padrao_mais_comum[0].split('→')[0]}")
    print("   → Adicionar instruções específicas para evitar este tipo de erro")
    
    print()
    print("3. Melhorias sugeridas no prompt:")
    print("   - Adicionar exemplos (few-shot learning)")
    print("   - Enfatizar análise cuidadosa de cada alternativa")
    print("   - Adicionar instrução para eliminar alternativas claramente incorretas")
    print("   - Usar chain-of-thought (raciocínio passo a passo)")
    
    return erros, padroes, erros_por_area

if __name__ == "__main__":
    analisar_erros()


