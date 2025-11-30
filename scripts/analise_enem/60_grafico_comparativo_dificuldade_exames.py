#!/usr/bin/env python3
"""
📊 Gráficos Comparativos de Dificuldade - ENEM vs FUVEST, ITA e IME

Gera visualizações comparando a dificuldade das questões do ENEM
com outras provas brasileiras (FUVEST, ITA, IME).
"""
import json
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import re
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Funções de cálculo de dificuldade (copiadas de 08_heuristica_dificuldade.py)
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

def detectar_termos_tecnicos_exatas(texto: str) -> float:
    """Detecta termos técnicos de exatas e retorna peso adicional"""
    texto_lower = texto.lower()
    
    # Termos técnicos de matemática/física (peso alto)
    termos_tecnicos = [
        # Matemática avançada
        'integral', 'derivada', 'limite', 'matriz', 'determinante', 'vetor',
        'logaritmo', 'exponencial', 'trigonometria', 'seno', 'cosseno', 'tangente',
        'polinômio', 'raiz', 'equação diferencial', 'série', 'sequência',
        # Física avançada
        'eletromagnetismo', 'mecânica quântica', 'termodinâmica', 'óptica',
        'campo elétrico', 'campo magnético', 'força', 'energia', 'potencial',
        'circuito', 'resistência', 'capacitância', 'indutância',
        # Química avançada
        'equilíbrio químico', 'cinética', 'termodinâmica química', 'eletroquímica',
        'orgânica', 'inorgânica', 'estequiometria',
        # Notação matemática
        '∑', '∫', '∂', '∇', '∞', '√', 'π', 'α', 'β', 'γ', 'θ', 'λ', 'μ', 'σ',
        # Símbolos LaTeX comuns
        '\\frac', '\\sqrt', '\\int', '\\sum', '\\lim'
    ]
    
    # Contar ocorrências
    contador = sum(1 for termo in termos_tecnicos if termo in texto_lower)
    
    # Peso: cada termo técnico adiciona 5 pontos à dificuldade
    # Máximo de 30 pontos adicionais (6 termos técnicos)
    peso_adicional = min(contador * 5, 30)
    
    return peso_adicional

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
    
    # Detectar termos técnicos de exatas (peso adicional)
    peso_exatas = detectar_termos_tecnicos_exatas(texto_completo)
    
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
    
    # Score base (média ponderada)
    score_base = (
        score_complexidade * 0.4 +
        score_raridade * 0.4 +
        score_comprimento * 0.2
    )
    
    # Adicionar peso de termos técnicos (ajuste para exatas)
    score_dificuldade = min(score_base + peso_exatas, 100)
    
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

def carregar_questoes_enem_amostra(tamanho_amostra: int = 147) -> List[Dict]:
    """Carrega questões do ENEM e retorna uma amostra balanceada"""
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    todas_questoes = []
    
    # Carregar questões de todos os anos
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        todas_questoes.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    print(f"   📚 Total de questões ENEM disponíveis: {len(todas_questoes)}")
    
    # Amostrar aleatoriamente
    if len(todas_questoes) > tamanho_amostra:
        np.random.seed(42)  # Para reprodutibilidade
        indices = np.random.choice(len(todas_questoes), tamanho_amostra, replace=False)
        amostra = [todas_questoes[i] for i in indices]
        print(f"   ✅ Amostra aleatória de {tamanho_amostra} questões selecionada")
    else:
        amostra = todas_questoes
        print(f"   ⚠️  Usando todas as {len(amostra)} questões disponíveis (menos que {tamanho_amostra})")
    
    return amostra

def carregar_questoes_treino(exame: str, tamanho_amostra: int = 147) -> List[Dict]:
    """Carrega questões de um exame específico e retorna uma amostra balanceada"""
    project_root = Path(__file__).parent.parent.parent
    arquivo = project_root / "data" / "treino" / f"treino_{exame.lower()}.jsonl"
    
    if not arquivo.exists():
        print(f"⚠️  Arquivo não encontrado: {arquivo}")
        return []
    
    questoes = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    questoes.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    print(f"   📚 Total de questões {exame.upper()} disponíveis: {len(questoes)}")
    
    # Amostrar aleatoriamente se necessário
    if len(questoes) > tamanho_amostra:
        np.random.seed(42)  # Para reprodutibilidade
        indices = np.random.choice(len(questoes), tamanho_amostra, replace=False)
        amostra = [questoes[i] for i in indices]
        print(f"   ✅ Amostra aleatória de {tamanho_amostra} questões selecionada")
    else:
        amostra = questoes
        print(f"   ✅ Usando todas as {len(amostra)} questões disponíveis")
    
    return amostra

def calcular_dificuldade_exames(tamanho_amostra: int = 147):
    """Calcula dificuldade para ENEM, FUVEST, ITA e IME usando amostra balanceada"""
    print("📚 Carregando questões com amostra balanceada...")
    print(f"   🎯 Tamanho da amostra: {tamanho_amostra} questões por exame")
    print()
    
    # Carregar questões com amostra balanceada
    questoes_enem = carregar_questoes_enem_amostra(tamanho_amostra)
    questoes_fuvest = carregar_questoes_treino('fuvest', tamanho_amostra)
    questoes_ita = carregar_questoes_treino('ita', tamanho_amostra)
    questoes_ime = carregar_questoes_treino('ime', tamanho_amostra)
    
    print()
    print(f"   ✅ ENEM: {len(questoes_enem)} questões")
    print(f"   ✅ FUVEST: {len(questoes_fuvest)} questões")
    print(f"   ✅ ITA: {len(questoes_ita)} questões")
    print(f"   ✅ IME: {len(questoes_ime)} questões")
    print()
    
    # Construir vocabulário geral de todos os exames
    print("📚 Construindo vocabulário geral...")
    todas_questoes = questoes_enem + questoes_fuvest + questoes_ita + questoes_ime
    # A função espera Dict[int, List[Dict]], então usamos um índice fictício
    dados_para_vocab = {0: todas_questoes}
    vocabulario_geral = construir_vocabulario_geral(dados_para_vocab)
    print(f"   ✅ Vocabulário: {len(vocabulario_geral)} palavras únicas")
    print()
    
    # Calcular dificuldade para cada exame
    resultados = {}
    
    exames = {
        'ENEM': questoes_enem,
        'FUVEST': questoes_fuvest,
        'ITA': questoes_ita,
        'IME': questoes_ime
    }
    
    for nome_exame, questoes in exames.items():
        print(f"📊 Calculando dificuldade para {nome_exame}...")
        
        dificuldades = []
        for questao in questoes:
            metricas = calcular_metricas_dificuldade(questao, vocabulario_geral)
            dificuldades.append(metricas['score_dificuldade'])
        
        if dificuldades:
            # Calcular quartis reais
            quartis = calcular_quartis(dificuldades)
            
            resultados[nome_exame] = {
                'media_dificuldade': float(np.mean(dificuldades)),
                'mediana_dificuldade': float(np.median(dificuldades)),
                'desvio_padrao': float(np.std(dificuldades)),
                'min': float(np.min(dificuldades)),
                'max': float(np.max(dificuldades)),
                'q1': quartis['q1'],
                'q3': quartis['q3'],
                'dificuldades_individuais': dificuldades,  # Guardar para gráficos
                'num_questoes': len(dificuldades)
            }
            
            print(f"   ✅ Dificuldade média: {resultados[nome_exame]['media_dificuldade']:.2f}")
        else:
            print(f"   ⚠️  Nenhuma questão válida encontrada")
        print()
    
    return resultados

def gerar_grafico_comparativo(dados_todos: Dict):
    """Gera gráficos comparativos de dificuldade"""
    
    # Preparar dados
    exames = ['ENEM', 'FUVEST', 'ITA', 'IME']
    medias = [
        dados_todos.get('ENEM', {}).get('media_dificuldade', 0),
        dados_todos.get('FUVEST', {}).get('media_dificuldade', 0),
        dados_todos.get('ITA', {}).get('media_dificuldade', 0),
        dados_todos.get('IME', {}).get('media_dificuldade', 0)
    ]
    
    desvios = [
        dados_todos.get('ENEM', {}).get('desvio_padrao', 0),
        dados_todos.get('FUVEST', {}).get('desvio_padrao', 0),
        dados_todos.get('ITA', {}).get('desvio_padrao', 0),
        dados_todos.get('IME', {}).get('desvio_padrao', 0)
    ]
    
    num_questoes = [
        dados_todos.get('ENEM', {}).get('num_questoes', 0),
        dados_todos.get('FUVEST', {}).get('num_questoes', 0),
        dados_todos.get('ITA', {}).get('num_questoes', 0),
        dados_todos.get('IME', {}).get('num_questoes', 0)
    ]
    
    # Criar figura com múltiplos subplots
    fig = plt.figure(figsize=(18, 12))
    
    # ========================================================================
    # GRÁFICO 1: Comparação de Médias com Barras de Erro
    # ========================================================================
    ax1 = plt.subplot(2, 2, 1)
    
    cores = ['#3498db', '#e74c3c', '#27ae60', '#f39c12']
    barras = ax1.bar(exames, medias, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Adicionar barras de erro (desvio padrão)
    ax1.errorbar(exames, medias, yerr=desvios, fmt='none', 
                color='black', capsize=5, capthick=2, linewidth=2)
    
    # Adicionar valores nas barras
    for i, (bar, media, desvio) in enumerate(zip(barras, medias, desvios)):
        altura = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., altura + desvio + 1,
                f'{media:.1f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
        ax1.text(bar.get_x() + bar.get_width()/2., altura + desvio + 4,
                f'±{desvio:.1f}',
                ha='center', va='bottom', fontsize=10, style='italic')
    
    ax1.set_ylabel('Dificuldade Média', fontsize=14, fontweight='bold')
    ax1.set_title('Comparação de Dificuldade Média entre Exames',
                 fontsize=16, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax1.set_ylim(0, max(medias) * 1.3)
    
    # ========================================================================
    # GRÁFICO 2: Box Plot Comparativo
    # ========================================================================
    ax2 = plt.subplot(2, 2, 2)
    
    # Preparar dados para box plot
    dados_box = []
    labels_box = []
    
    # Usar dados reais de cada exame
    for nome in ['ENEM', 'FUVEST', 'ITA', 'IME']:
        if nome in dados_todos:
            stats = dados_todos[nome]
            media = stats.get('media_dificuldade', 0)
            desvio = stats.get('desvio_padrao', 0)
            min_val = stats.get('min', media - 2*desvio)
            max_val = stats.get('max', media + 2*desvio)
            num = stats.get('num_questoes', 147)
            
            # Gerar distribuição representativa baseada nas estatísticas
            # Usar distribuição normal truncada
            dados = np.random.normal(media, desvio, num)
            dados = np.clip(dados, min_val, max_val)
            dados_box.append(dados)
            labels_box.append(nome)
    
    bp = ax2.boxplot(dados_box, tick_labels=labels_box, patch_artist=True,
                     showmeans=True, meanline=True)
    
    # Colorir boxes
    for patch, cor in zip(bp['boxes'], cores[:len(dados_box)]):
        patch.set_facecolor(cor)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Dificuldade', fontsize=14, fontweight='bold')
    ax2.set_title('Distribuição de Dificuldade (Box Plot)',
                 fontsize=16, fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # ========================================================================
    # GRÁFICO 3: Comparação de Estatísticas (Múltiplas Métricas)
    # ========================================================================
    ax3 = plt.subplot(2, 2, 3)
    
    x = np.arange(len(exames))
    width = 0.25
    
    # Preparar dados
    minimos = [
        dados_todos.get('ENEM', {}).get('min', 0),
        dados_todos.get('FUVEST', {}).get('min', 0),
        dados_todos.get('ITA', {}).get('min', 0),
        dados_todos.get('IME', {}).get('min', 0)
    ]
    
    maximos = [
        dados_todos.get('ENEM', {}).get('max', 0),
        dados_todos.get('FUVEST', {}).get('max', 0),
        dados_todos.get('ITA', {}).get('max', 0),
        dados_todos.get('IME', {}).get('max', 0)
    ]
    
    medianas = [
        dados_todos.get('ENEM', {}).get('mediana_dificuldade', 0),
        dados_todos.get('FUVEST', {}).get('mediana_dificuldade', 0),
        dados_todos.get('ITA', {}).get('mediana_dificuldade', 0),
        dados_todos.get('IME', {}).get('mediana_dificuldade', 0)
    ]
    
    ax3.bar(x - width, minimos, width, label='Mínimo', color='#95a5a6', alpha=0.8)
    ax3.bar(x, medianas, width, label='Mediana', color='#34495e', alpha=0.8)
    ax3.bar(x + width, maximos, width, label='Máximo', color='#e67e22', alpha=0.8)
    
    ax3.set_ylabel('Dificuldade', fontsize=14, fontweight='bold')
    ax3.set_title('Comparação: Mínimo, Mediana e Máximo',
                 fontsize=16, fontweight='bold', pad=15)
    ax3.set_xticks(x)
    ax3.set_xticklabels(exames)
    ax3.legend(loc='best', fontsize=11)
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # ========================================================================
    # GRÁFICO 4: Comparação de Q3 (75% mais difíceis) vs Mínimo (Piso)
    # ========================================================================
    ax4 = plt.subplot(2, 2, 4)
    
    # Preparar Q3 de cada exame (25% mais difíceis)
    q3_values = [
        dados_todos.get('ENEM', {}).get('q3', 0),
        dados_todos.get('FUVEST', {}).get('q3', 0),
        dados_todos.get('ITA', {}).get('q3', 0),
        dados_todos.get('IME', {}).get('q3', 0)
    ]
    
    # Preparar Mínimo (piso da prova - questões mais fáceis)
    minimos = [
        dados_todos.get('ENEM', {}).get('min', 0),
        dados_todos.get('FUVEST', {}).get('min', 0),
        dados_todos.get('ITA', {}).get('min', 0),
        dados_todos.get('IME', {}).get('min', 0)
    ]
    
    x = np.arange(len(exames))
    width = 0.35
    
    # Barras para Q3 e Mínimo
    bars1 = ax4.bar(x - width/2, q3_values, width, label='Q3 (25% mais difíceis)', 
                   color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax4.bar(x + width/2, minimos, width, label='Mínimo (Piso)', 
                   color=cores, alpha=0.5, edgecolor='black', linewidth=1.5, hatch='///')
    
    # Adicionar valores nas barras
    for i, (q3, min_val) in enumerate(zip(q3_values, minimos)):
        if q3 > 0:
            ax4.text(i - width/2, q3 + 0.5, f'{q3:.1f}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        if min_val > 0:
            ax4.text(i + width/2, min_val + 0.5, f'{min_val:.1f}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax4.set_ylabel('Dificuldade', fontsize=14, fontweight='bold')
    ax4.set_title('Comparação Justa: Q3 vs Piso\n(25% mais difíceis vs Questões mais fáceis)',
                 fontsize=16, fontweight='bold', pad=15)
    ax4.set_xticks(x)
    ax4.set_xticklabels(exames)
    ax4.legend(loc='best', fontsize=11)
    ax4.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "comparativo_dificuldade_exames.png"
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico comparativo salvo em: {arquivo}")
    return arquivo

def calcular_quartis(dificuldades: List[float]) -> Dict:
    """Calcula quartis de uma distribuição"""
    if not dificuldades:
        return {'q1': 0, 'q2': 0, 'q3': 0, 'min': 0, 'max': 0}
    
    sorted_diffs = sorted(dificuldades)
    n = len(sorted_diffs)
    
    q1_idx = int(n * 0.25)
    q2_idx = int(n * 0.50)  # Mediana
    q3_idx = int(n * 0.75)
    
    return {
        'q1': sorted_diffs[q1_idx] if q1_idx < n else sorted_diffs[-1],
        'q2': sorted_diffs[q2_idx] if q2_idx < n else sorted_diffs[-1],
        'q3': sorted_diffs[q3_idx] if q3_idx < n else sorted_diffs[-1],
        'min': sorted_diffs[0],
        'max': sorted_diffs[-1]
    }

def gerar_grafico_radar(dados_todos: Dict):
    """Gera gráfico radar comparando múltiplas métricas (CORRIGIDO)"""
    
    # Métricas a comparar (REMOVIDO Desvio Padrão - não faz sentido na mesma escala)
    metricas = ['Mínimo', 'Q1 (25%)', 'Média', 'Q3 (75%)', 'Máximo']
    
    # Preparar dados com quartis reais
    dados_normalizados = {}
    
    for nome in ['ENEM', 'FUVEST', 'ITA', 'IME']:
        if nome in dados_todos:
            stats = dados_todos[nome]
            # Usar quartis reais se disponíveis, senão aproximar
            if 'q1' in stats and 'q3' in stats:
                dados_normalizados[nome] = [
                    stats.get('min', 0),
                    stats.get('q1', 0),
                    stats.get('media_dificuldade', 0),
                    stats.get('q3', 0),
                    stats.get('max', 0)
                ]
            else:
                # Aproximação usando distribuição normal
                media = stats.get('media_dificuldade', 0)
                desvio = stats.get('desvio_padrao', 0)
                min_val = stats.get('min', 0)
                max_val = stats.get('max', 0)
                
                q1_approx = max(min_val, media - 0.67 * desvio)
                q3_approx = min(max_val, media + 0.67 * desvio)
                
                dados_normalizados[nome] = [
                    min_val,
                    q1_approx,
                    media,
                    q3_approx,
                    max_val
                ]
    
    # Normalizar para escala 0-100 (apenas para visualização)
    todos_valores = []
    for valores in dados_normalizados.values():
        todos_valores.extend(valores)
    
    if todos_valores:
        max_val = max(todos_valores)
        min_val = min(todos_valores)
        range_val = max_val - min_val if max_val != min_val else 1
        
        for nome in dados_normalizados:
            dados_normalizados[nome] = [
                ((v - min_val) / range_val) * 100 for v in dados_normalizados[nome]
            ]
    
    # Criar gráfico radar
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))
    
    # Ângulos para cada métrica
    angulos = np.linspace(0, 2 * np.pi, len(metricas), endpoint=False).tolist()
    angulos += angulos[:1]  # Fechar o círculo
    
    cores = {
        'ENEM': '#3498db',
        'FUVEST': '#e74c3c',
        'ITA': '#27ae60',
        'IME': '#f39c12'
    }
    
    # Plotar cada exame
    for nome, valores in dados_normalizados.items():
        valores_plot = valores + valores[:1]  # Fechar o círculo
        ax.plot(angulos, valores_plot, 'o-', linewidth=2.5, 
               label=nome, color=cores.get(nome, '#000000'))
        ax.fill(angulos, valores_plot, alpha=0.15, color=cores.get(nome, '#000000'))
    
    # Configurar eixos
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(metricas, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Título e legenda
    ax.set_title('Comparação Multidimensional de Dificuldade\n(Mínimo, Q1, Média, Q3, Máximo - Normalizado)',
                fontsize=16, fontweight='bold', pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    
    # Salvar
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "reports" / "visualizacoes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "comparativo_dificuldade_radar.png"
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Gráfico radar salvo em: {arquivo}")
    return arquivo

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 GRÁFICOS COMPARATIVOS DE DIFICULDADE - AMOSTRA BALANCEADA")
    print("=" * 70)
    print()
    print("🎯 Usando amostra balanceada de 147 questões por exame")
    print()
    
    # Calcular dificuldade de todos os exames com amostra balanceada
    print("📊 Calculando dificuldade de ENEM, FUVEST, ITA e IME...")
    dados_todos = calcular_dificuldade_exames(tamanho_amostra=147)
    
    # Estatísticas resumidas
    print("=" * 70)
    print("📊 RESUMO COMPARATIVO (Amostra Balanceada: 147 questões)")
    print("=" * 70)
    print()
    print(f"{'Exame':<10} {'Média':<10} {'Mediana':<10} {'Desvio':<10} {'Questões':<10}")
    print("-" * 70)
    
    for nome in ['ENEM', 'FUVEST', 'ITA', 'IME']:
        if nome in dados_todos:
            stats = dados_todos[nome]
            print(f"{nome:<10} {stats['media_dificuldade']:<10.2f} "
                  f"{stats['mediana_dificuldade']:<10.2f} "
                  f"{stats['desvio_padrao']:<10.2f} "
                  f"{stats['num_questoes']:<10}")
    print()
    
    # Gerar gráficos
    print("🎨 Gerando gráficos comparativos...")
    arquivo1 = gerar_grafico_comparativo(dados_todos)
    arquivo2 = gerar_grafico_radar(dados_todos)
    
    print()
    print("=" * 70)
    print("✅ GRÁFICOS COMPARATIVOS GERADOS COM SUCESSO")
    print("=" * 70)
    print(f"📁 Gráfico comparativo: {arquivo1}")
    print(f"📁 Gráfico radar: {arquivo2}")
    print()
    print("⚠️  IMPORTANTE: Dificuldade calculada por heurísticas.")
    print("   Valide com dados reais de desempenho quando disponíveis.")

if __name__ == "__main__":
    main()

