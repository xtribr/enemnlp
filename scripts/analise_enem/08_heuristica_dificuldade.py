#!/usr/bin/env python3
"""
Análise de Dificuldade das Questões do ENEM

Usa heurísticas baseadas em complexidade sintática, raridade lexical e outras métricas.
"""
import json
import sys
from pathlib import Path
import numpy as np
from typing import Dict, List
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_dados_processados(processed_dir: Path) -> Dict[int, List[Dict]]:
    """Carrega todos os dados processados"""
    dados = {}
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        dados[ano] = questoes
    return dados

def calcular_complexidade_sintatica(texto: str) -> float:
    """Calcula complexidade sintática básica"""
    if not texto:
        return 0.0
    
    # Contar sentenças
    sentencas = re.split(r'[.!?]+', texto)
    num_sentencas = len([s for s in sentencas if s.strip()])
    
    # Contar palavras
    palavras = texto.split()
    num_palavras = len(palavras)
    
    # Palavras por sentença
    palavras_por_sentenca = num_palavras / num_sentencas if num_sentencas > 0 else 0
    
    # Contar palavras longas (>6 caracteres)
    palavras_longas = sum(1 for p in palavras if len(p) > 6)
    percentual_longas = (palavras_longas / num_palavras * 100) if num_palavras > 0 else 0
    
    # Complexidade = palavras por sentença + percentual de palavras longas
    complexidade = palavras_por_sentenca + (percentual_longas / 10)
    
    return complexidade

def calcular_raridade_lexical(texto: str, vocabulario_geral: Dict[str, int] = None) -> float:
    """Calcula raridade lexical (frequência de palavras raras)"""
    if not texto:
        return 0.0
    
    palavras = texto.lower().split()
    
    if vocabulario_geral is None:
        # Se não houver vocabulário geral, usar heurística simples
        # Palavras raras = palavras longas ou com caracteres especiais
        palavras_raras = sum(1 for p in palavras if len(p) > 8 or not p.isalnum())
        return (palavras_raras / len(palavras) * 100) if palavras else 0.0
    
    # Calcular frequência média das palavras
    frequencias = []
    for palavra in palavras:
        freq = vocabulario_geral.get(palavra, 0)
        if freq > 0:
            frequencias.append(freq)
    
    if not frequencias:
        return 100.0  # Todas as palavras são raras
    
    # Raridade = inverso da frequência média (normalizado)
    freq_media = np.mean(frequencias)
    raridade = 100.0 / (1 + freq_media)  # Normalizado
    
    return raridade

def construir_vocabulario_geral(dados: Dict[int, List[Dict]]) -> Dict[str, int]:
    """Constrói vocabulário geral de todas as questões"""
    vocabulario = {}
    
    for questoes in dados.values():
        for questao in questoes:
            texto = f"{questao.get('context', '')} {questao.get('question', '')}".lower()
            palavras = texto.split()
            
            for palavra in palavras:
                palavra_limpa = re.sub(r'[^\w]', '', palavra)
                if palavra_limpa:
                    vocabulario[palavra_limpa] = vocabulario.get(palavra_limpa, 0) + 1
    
    return vocabulario

def calcular_metricas_dificuldade(questao: Dict, vocabulario_geral: Dict[str, int]) -> Dict:
    """Calcula todas as métricas de dificuldade para uma questão"""
    contexto = questao.get('context', '')
    pergunta = questao.get('question', '')
    texto_completo = f"{contexto} {pergunta}"
    
    # Complexidade sintática
    complexidade_sint = calcular_complexidade_sintatica(texto_completo)
    
    # Raridade lexical
    raridade_lex = calcular_raridade_lexical(texto_completo, vocabulario_geral)
    
    # Comprimento do texto
    comprimento = len(texto_completo)
    
    # Número de alternativas (normalmente 5)
    num_alternativas = len(questao.get('alternatives', []))
    
    # Comprimento das alternativas
    alternativas = questao.get('alternatives', [])
    comprimento_alternativas = sum(len(alt) for alt in alternativas)
    
    # Score de dificuldade (combinação de métricas)
    # Normalizar cada métrica para escala 0-100
    score_complexidade = min(complexidade_sint * 5, 100)  # Normalizar
    score_raridade = min(raridade_lex, 100)
    score_comprimento = min(comprimento / 50, 100)  # Normalizar
    
    # Score final (média ponderada)
    score_dificuldade = (
        score_complexidade * 0.4 +
        score_raridade * 0.4 +
        score_comprimento * 0.2
    )
    
    return {
        'complexidade_sintatica': float(complexidade_sint),
        'raridade_lexical': float(raridade_lex),
        'comprimento_texto': comprimento,
        'comprimento_alternativas': comprimento_alternativas,
        'num_alternativas': num_alternativas,
        'score_dificuldade': float(score_dificuldade),
        'nivel_dificuldade': (
            'muito_facil' if score_dificuldade < 30 else
            'facil' if score_dificuldade < 50 else
            'medio' if score_dificuldade < 70 else
            'dificil' if score_dificuldade < 85 else
            'muito_dificil'
        )
    }

def processar_todas_questoes(dados: Dict[int, List[Dict]]) -> Dict:
    """Processa todas as questões calculando dificuldade"""
    print("📚 Construindo vocabulário geral...")
    vocabulario_geral = construir_vocabulario_geral(dados)
    print(f"✅ Vocabulário: {len(vocabulario_geral)} palavras únicas")
    print()
    
    resultados = {}
    
    for ano in sorted(dados.keys()):
        questoes = dados[ano]
        print(f"📊 Processando {ano} ({len(questoes)} questões)...")
        
        metricas_ano = []
        for questao in questoes:
            metricas = calcular_metricas_dificuldade(questao, vocabulario_geral)
            metricas['id'] = questao.get('id', '')
            metricas['area'] = questao.get('area', 'desconhecida')
            metricas_ano.append(metricas)
        
        # Estatísticas por ano
        scores = [m['score_dificuldade'] for m in metricas_ano]
        resultados[ano] = {
            'questoes': metricas_ano,
            'estatisticas': {
                'media_dificuldade': float(np.mean(scores)),
                'mediana_dificuldade': float(np.median(scores)),
                'desvio_padrao': float(np.std(scores)),
                'min': float(np.min(scores)),
                'max': float(np.max(scores))
            }
        }
        
        print(f"  ✅ Dificuldade média: {np.mean(scores):.2f}")
        print()
    
    return resultados

def salvar_resultados(resultados: Dict, output_dir: Path):
    """Salva resultados da análise de dificuldade"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvar completo
    arquivo_completo = output_dir / "dificuldade_completo.json"
    with open(arquivo_completo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    # Salvar apenas estatísticas
    estatisticas = {ano: dados['estatisticas'] for ano, dados in resultados.items()}
    arquivo_stats = output_dir / "dificuldade_estatisticas.json"
    with open(arquivo_stats, 'w', encoding='utf-8') as f:
        json.dump(estatisticas, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados salvos em:")
    print(f"   - {arquivo_completo.name}")
    print(f"   - {arquivo_stats.name}")

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 ANÁLISE DE DIFICULDADE - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    analises_dir = project_root / "data" / "analises"
    
    # Carregar dados
    print("📥 Carregando dados...")
    dados = carregar_dados_processados(processed_dir)
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # Processar dificuldade
    resultados = processar_todas_questoes(dados)
    
    # Salvar resultados
    salvar_resultados(resultados, analises_dir)
    
    print()
    print("=" * 70)
    print("✅ ANÁLISE DE DIFICULDADE CONCLUÍDA")
    print("=" * 70)
    print("\n⚠️  IMPORTANTE: Dificuldade calculada por heurísticas.")
    print("   Valide com dados reais de desempenho quando disponíveis.")

if __name__ == "__main__":
    main()


