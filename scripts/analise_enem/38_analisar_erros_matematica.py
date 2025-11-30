#!/usr/bin/env python3
"""
Analisa erros de matemática em detalhes
Identifica padrões: geometria, álgebra, probabilidade, etc.
"""
import json
import sys
from pathlib import Path
from collections import defaultdict
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_questoes_matematica():
    """Carrega todas as questões de matemática"""
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    questoes = {}
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    if questao.get('area') == 'mathematics':
                        questoes[questao.get('id', '')] = questao
    
    return questoes

def identificar_topico_matematica(questao: dict) -> list:
    """Identifica tópicos matemáticos na questão"""
    contexto = questao.get('context', '').lower()
    pergunta = questao.get('question', '').lower()
    texto_completo = f"{contexto} {pergunta}"
    
    topicos = []
    
    # Geometria
    if any(palavra in texto_completo for palavra in ['geometria', 'triângulo', 'retângulo', 'círculo', 'área', 'volume', 'perímetro', 'ângulo', 'diagonal', 'raio', 'diâmetro', 'altura', 'base']):
        topicos.append('geometria')
    
    # Álgebra
    if any(palavra in texto_completo for palavra in ['equação', 'equações', 'função', 'funções', 'variável', 'incógnita', 'sistema', 'polinômio', 'raiz', 'gráfico']):
        topicos.append('álgebra')
    
    # Aritmética
    if any(palavra in texto_completo for palavra in ['calcular', 'soma', 'subtração', 'multiplicação', 'divisão', 'porcentagem', 'razão', 'proporção', 'média', 'total']):
        topicos.append('aritmética')
    
    # Probabilidade/Estatística
    if any(palavra in texto_completo for palavra in ['probabilidade', 'chance', 'estatística', 'amostra', 'população', 'desvio', 'média', 'mediana', 'moda', 'distribuição']):
        topicos.append('probabilidade/estatística')
    
    # Trigonometria
    if any(palavra in texto_completo for palavra in ['seno', 'cosseno', 'tangente', 'trigonometria', 'ângulo', 'radiano', 'grau']):
        topicos.append('trigonometria')
    
    # Análise Combinatória
    if any(palavra in texto_completo for palavra in ['combinação', 'permutação', 'arranjo', 'fatorial', 'possibilidades']):
        topicos.append('análise combinatória')
    
    return topicos if topicos else ['outros']

def analisar_erros_detalhado():
    """Analisa erros de matemática em detalhes"""
    print("=" * 70)
    print("🔍 ANÁLISE DETALHADA DE ERROS EM MATEMÁTICA")
    print("=" * 70)
    print()
    
    # Carregar questões
    print("📥 Carregando questões de matemática...")
    questoes = carregar_questoes_matematica()
    print(f"✅ {len(questoes)} questões carregadas")
    print()
    
    # Carregar resultados
    project_root = Path(__file__).parent.parent.parent
    arquivo_resultados = project_root / "results" / "avaliacao_oficial_captions.json"
    
    if not arquivo_resultados.exists():
        print(f"❌ Arquivo de resultados não encontrado: {arquivo_resultados}")
        return
    
    print("📥 Carregando resultados da avaliação...")
    with open(arquivo_resultados, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # O arquivo de resultados não tem detalhes individuais das questões
    # Vamos precisar executar novamente com logging detalhado ou usar cache
    print("⚠️  Arquivo de resultados não contém detalhes individuais")
    print("   Vamos analisar baseado nos dados disponíveis")
    print()
    
    # Estatísticas gerais
    resultados = dados['results']['enem_cot_2024_captions']
    acuracia_math = resultados['mathematics']
    
    print("📊 Estatísticas Gerais:")
    print(f"   Acurácia em Matemática: {acuracia_math*100:.2f}%")
    print(f"   Erro padrão: ±{resultados['mathematics_stderr']*100:.2f}%")
    print()
    
    # Análise por tópico (baseado em todas as questões de matemática)
    print("📚 Análise de Tópicos (todas as questões de matemática):")
    print()
    
    topicos_contagem = defaultdict(int)
    for questao_id, questao in questoes.items():
        topicos = identificar_topico_matematica(questao)
        for topico in topicos:
            topicos_contagem[topico] += 1
    
    print("   Distribuição de tópicos:")
    for topico, count in sorted(topicos_contagem.items(), key=lambda x: x[1], reverse=True):
        porcentagem = (count / len(questoes)) * 100
        print(f"   - {topico.capitalize()}: {count} questões ({porcentagem:.1f}%)")
    
    print()
    print("=" * 70)
    print("💡 RECOMENDAÇÕES:")
    print("=" * 70)
    print()
    print("Para análise mais detalhada, precisamos:")
    print("1. Executar avaliação com logging detalhado")
    print("2. Salvar respostas individuais de cada questão")
    print("3. Comparar respostas corretas vs. respostas da IA")
    print()
    print("Deseja executar avaliação detalhada agora?")
    print("   (Isso vai re-executar a avaliação salvando detalhes)")

if __name__ == "__main__":
    analisar_erros_detalhado()

