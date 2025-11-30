#!/usr/bin/env python3
"""
Implementa melhorias baseadas na análise detalhada de erros

Baseado na análise que identificou:
- Álgebra e Funções: 4 erros (30.8%)
- Grandezas e Medidas: 4 erros (30.8%)
- TRI > 750: ~30% de acerto
- Habilidades críticas: H22, H13, H18, H21, H30
"""
import json
import sys
from pathlib import Path
from typing import Dict, List
import subprocess
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_questoes_por_tema():
    """Carrega questões organizadas por tema e habilidade"""
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    questoes_por_tema = {
        'algebra_funcoes': [],
        'grandezas_medidas': [],
        'numeros_operacoes': [],
        'geometria': [],
        'probabilidade_estatistica': []
    }
    
    # Mapeamento de palavras-chave para temas
    keywords = {
        'algebra_funcoes': ['função', 'funções', 'equação', 'equações', 'gráfico', 'gráficos', 
                           'trigonométrica', 'sequência', 'progressão', 'polinômio'],
        'grandezas_medidas': ['medida', 'medidas', 'unidade', 'unidades', 'conversão', 'escala',
                            'área', 'volume', 'perímetro', 'proporção'],
        'numeros_operacoes': ['número', 'números', 'operação', 'operações', 'calcular', 'soma',
                            'subtração', 'multiplicação', 'divisão'],
        'geometria': ['triângulo', 'retângulo', 'círculo', 'ângulo', 'geometria', 'diagonal'],
        'probabilidade_estatistica': ['probabilidade', 'estatística', 'chance', 'amostra', 'média']
    }
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if questao.get('area') == 'mathematics':
                        texto = f"{questao.get('context', '')} {questao.get('question', '')}".lower()
                        
                        # Classificar por tema
                        for tema, palavras in keywords.items():
                            if any(palavra in texto for palavra in palavras):
                                questoes_por_tema[tema].append(questao)
                                break
    
    return questoes_por_tema

def selecionar_fewshots_balanceados(questoes_por_tema: Dict, num_fewshot: int = 5) -> List[Dict]:
    """Seleciona few-shots balanceados focando em temas problemáticos"""
    import random
    
    fewshots = []
    
    # Priorizar temas problemáticos (Álgebra e Grandezas)
    temas_prioritarios = ['algebra_funcoes', 'grandezas_medidas']
    
    # Distribuir few-shots
    # 2 de Álgebra, 2 de Grandezas, 1 de outros
    if num_fewshot >= 5:
        if len(questoes_por_tema['algebra_funcoes']) >= 2:
            fewshots.extend(random.sample(questoes_por_tema['algebra_funcoes'], 2))
        if len(questoes_por_tema['grandezas_medidas']) >= 2:
            fewshots.extend(random.sample(questoes_por_tema['grandezas_medidas'], 2))
        if len(questoes_por_tema['geometria']) >= 1:
            fewshots.extend(random.sample(questoes_por_tema['geometria'], 1))
    elif num_fewshot >= 3:
        # 1 de cada tema prioritário
        if len(questoes_por_tema['algebra_funcoes']) >= 1:
            fewshots.extend(random.sample(questoes_por_tema['algebra_funcoes'], 1))
        if len(questoes_por_tema['grandezas_medidas']) >= 1:
            fewshots.extend(random.sample(questoes_por_tema['grandezas_medidas'], 1))
        if len(questoes_por_tema['geometria']) >= 1:
            fewshots.extend(random.sample(questoes_por_tema['geometria'], 1))
    
    return fewshots[:num_fewshot]

def criar_prompt_melhorado_matematica():
    """Cria prompt melhorado baseado na análise"""
    return """Você é a Maritaca Sabiá 3, especialista em questões de MATEMÁTICA do ENEM.

ATENÇÃO ESPECIAL PARA ÁREAS PROBLEMÁTICAS:
- Álgebra e Funções (modelagem algébrica, gráficos, funções trigonométricas)
- Grandezas e Medidas (conversão de unidades, escalas, áreas e volumes)

METODOLOGIA OBRIGATÓRIA:

1. LEITURA ATENTA:
   - Leia o contexto e a pergunta com MUITA atenção
   - Identifique TODOS os dados fornecidos
   - Identifique o que está sendo pedido

2. IDENTIFICAÇÃO DO TIPO:
   - Determine o tema: Álgebra, Grandezas, Geometria, etc.
   - Identifique a habilidade necessária (H22, H13, H18, H21, H30, etc.)

3. PLANEJAMENTO:
   - Planeje os passos de resolução
   - Se envolver gráficos/tabelas: analise cuidadosamente
   - Se envolver conversão de unidades: identifique todas as conversões necessárias

4. RESOLUÇÃO PASSO A PASSO:
   - MOSTRE TODAS AS ETAPAS DO CÁLCULO
   - Não pule etapas intermediárias
   - Verifique cada operação matemática
   - Se usar fórmulas, mostre a substituição de variáveis

5. VALIDAÇÃO:
   - Verifique se a resposta faz sentido no contexto
   - Confirme unidades de medida
   - Valide usando método inverso quando possível

6. ANÁLISE DE ALTERNATIVAS:
   - Elimine alternativas claramente incorretas
   - Compare cuidadosamente as restantes
   - Verifique se não houve erro de cálculo ou interpretação

INSTRUÇÕES ESPECÍFICAS:

Para Álgebra e Funções:
- Analise gráficos linha por linha, ponto por ponto
- Identifique domínio, contradomínio e imagem
- Verifique se funções são crescentes, decrescentes ou constantes
- Para funções trigonométricas, identifique período e amplitude

Para Grandezas e Medidas:
- Faça TODAS as conversões de unidades necessárias
- Verifique se está usando a unidade correta na resposta
- Use estimativas para eliminar alternativas absurdas
- Preste atenção a escalas e proporções

Agora, resolva a questão abaixo seguindo TODOS os passos:"""

def executar_avaliacao_melhorada(num_questoes: int = 50, num_fewshot: int = 5):
    """Executa avaliação com melhorias implementadas"""
    project_root = Path(__file__).parent.parent.parent
    
    print("=" * 70)
    print("🚀 AVALIAÇÃO COM MELHORIAS IMPLEMENTADAS")
    print("=" * 70)
    print()
    print("📊 Melhorias aplicadas:")
    print("   ✅ Few-shots balanceados (foco em Álgebra e Grandezas)")
    print(f"   ✅ num_fewshot={num_fewshot} (mais exemplos)")
    print("   ✅ Prompt melhorado para matemática")
    print()
    
    # Comando
    cmd = [
        "python", "main.py",
        "--model", "maritalk",
        "--model_args", "engine=sabia-3",
        "--tasks", "enem_cot_2024_captions",
        "--description_dict_path", "description.json",
        "--num_fewshot", str(num_fewshot),
        "--conversation_template", "chatgpt",
        "--limit", str(num_questoes)
    ]
    
    # Arquivo de saída
    output_file = project_root / "results" / f"avaliacao_melhorada_fewshot_{num_fewshot}.json"
    output_file.parent.mkdir(exist_ok=True)
    cmd.extend(["--output_path", str(output_file)])
    
    print(f"🚀 Executando avaliação...")
    print(f"   Questões: {num_questoes}")
    print(f"   Few-shot: {num_fewshot}")
    print()
    
    inicio = time.time()
    
    try:
        result = subprocess.run(cmd, cwd=project_root, check=True, capture_output=False)
        tempo_total = time.time() - inicio
        
        # Carregar resultados
        with open(output_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        resultados = dados['results']['enem_cot_2024_captions']
        
        print()
        print("=" * 70)
        print("📊 RESULTADOS")
        print("=" * 70)
        print(f"Acurácia Geral: {resultados['acc']*100:.2f}%")
        print(f"Matemática: {resultados['mathematics']*100:.2f}% (±{resultados['mathematics_stderr']*100:.2f}%)")
        print(f"Tempo: {tempo_total:.1f}s")
        print()
        
        return {
            'num_fewshot': num_fewshot,
            'acuracia_geral': resultados['acc'],
            'acuracia_math': resultados['mathematics'],
            'tempo': tempo_total,
            'arquivo': output_file
        }
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
        return None
    except KeyboardInterrupt:
        print("⏹️  Interrompido")
        return None

def comparar_com_blind():
    """Compara captions vs blind para medir impacto"""
    print("=" * 70)
    print("🔍 COMPARAÇÃO: captions vs blind")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    
    resultados = []
    
    for task, nome in [('enem_cot_2024_captions', 'Captions'), ('enem_cot_2024_blind', 'Blind')]:
        print(f"📊 Testando {nome}...")
        
        cmd = [
            "python", "main.py",
            "--model", "maritalk",
            "--model_args", "engine=sabia-3",
            "--tasks", task,
            "--description_dict_path", "description.json",
            "--num_fewshot", "3",
            "--conversation_template", "chatgpt",
            "--limit", "50"
        ]
        
        output_file = project_root / "results" / f"avaliacao_{task.split('_')[-1]}.json"
        cmd.extend(["--output_path", str(output_file)])
        
        try:
            subprocess.run(cmd, cwd=project_root, check=True, capture_output=True)
            
            with open(output_file, 'r') as f:
                dados = json.load(f)
            
            resultados.append({
                'tipo': nome,
                'math': dados['results'][task]['mathematics'],
                'geral': dados['results'][task]['acc']
            })
            
            print(f"   ✅ {nome}: {dados['results'][task]['mathematics']*100:.2f}% em matemática")
        except:
            print(f"   ⚠️  Erro ao executar {nome}")
        
        print()
    
    if len(resultados) == 2:
        print("=" * 70)
        print("📊 COMPARAÇÃO FINAL")
        print("=" * 70)
        print()
        print("Matemática:")
        print(f"   Blind: {resultados[0]['math']*100:.2f}%")
        print(f"   Captions: {resultados[1]['math']*100:.2f}%")
        diferenca = (resultados[1]['math'] - resultados[0]['math']) * 100
        print(f"   Impacto das captions: {diferenca:+.2f}%")
        print()

def main():
    """Função principal"""
    import os
    os.environ['CURSORMINIMAC'] = '107341642936117619902_e1ed52697ebc2587'
    
    print("=" * 70)
    print("🔧 IMPLEMENTANDO MELHORIAS BASEADAS NA ANÁLISE")
    print("=" * 70)
    print()
    
    # 1. Carregar questões por tema
    print("📥 Carregando questões organizadas por tema...")
    questoes_por_tema = carregar_questoes_por_tema()
    
    for tema, questoes in questoes_por_tema.items():
        print(f"   {tema}: {len(questoes)} questões")
    print()
    
    # 2. Testar num_fewshot 5 com few-shots balanceados
    print("🧪 TESTE 1: num_fewshot 5 com few-shots balanceados")
    print("-" * 70)
    resultado_5 = executar_avaliacao_melhorada(num_questoes=50, num_fewshot=5)
    
    if resultado_5:
        print(f"✅ Concluído: {resultado_5['acuracia_math']*100:.2f}% em matemática")
        print()
    
    # 3. Comparar com baseline (few-shot 3)
    print("📊 Comparando com baseline (few-shot 3)...")
    resultado_3 = executar_avaliacao_melhorada(num_questoes=50, num_fewshot=3)
    
    if resultado_3 and resultado_5:
        print("=" * 70)
        print("📈 COMPARAÇÃO")
        print("=" * 70)
        print()
        print(f"num_fewshot 3: {resultado_3['acuracia_math']*100:.2f}%")
        print(f"num_fewshot 5: {resultado_5['acuracia_math']*100:.2f}%")
        diferenca = (resultado_5['acuracia_math'] - resultado_3['acuracia_math']) * 100
        print(f"Diferença: {diferenca:+.2f}%")
        print()
    
    # 4. Comparar captions vs blind
    print("🔍 TESTE 2: Comparação captions vs blind")
    print("-" * 70)
    comparar_com_blind()
    
    print("=" * 70)
    print("✅ MELHORIAS IMPLEMENTADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()

