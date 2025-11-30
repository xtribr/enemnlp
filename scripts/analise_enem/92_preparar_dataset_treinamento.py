#!/usr/bin/env python3
"""
📚 PREPARAR DATASET DE TREINAMENTO - ENEM (2009-2025)

Prepara dataset formatado para treinamento de modelo NLP usando transformers.

Metodologia correta:
1. Carregar TODOS os dados (2009-2025)
2. Formatar como input/output para treinamento
3. Dividir em treino/validação/teste
4. Salvar em formato adequado para HuggingFace
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import random

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_todas_questoes(processed_dir: Path) -> List[Dict]:
    """Carrega TODAS as questões de 2009-2025"""
    questoes = []
    
    print("📥 Carregando TODAS as questões (2009-2025)...")
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = jsonl_file.stem.replace('enem_', '').replace('_completo', '')
        count = 0
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questao = json.loads(line)
                    # Validar questão
                    if (questao.get('question') and 
                        questao.get('label', '').upper() in ['A', 'B', 'C', 'D', 'E']):
                        questao['ano'] = int(ano) if ano.isdigit() else None
                        questoes.append(questao)
                        count += 1
        
        print(f"   {ano}: {count} questões válidas")
    
    print(f"✅ Total: {len(questoes)} questões carregadas")
    return questoes

def formatar_para_treinamento(questao: Dict) -> Dict:
    """
    Formata questão para treinamento de modelo NLP
    
    Input: Questão completa (contexto + pergunta + alternativas)
    Output: Resposta correta (A, B, C, D, E)
    """
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    resposta_correta = questao.get('label', '').upper().strip()
    
    # Construir texto de entrada
    texto_entrada = ""
    
    if contexto:
        texto_entrada += f"CONTEXTO:\n{contexto}\n\n"
    
    texto_entrada += f"PERGUNTA:\n{pergunta}\n\n"
    
    if alternativas:
        texto_entrada += "ALTERNATIVAS:\n"
        for i, alt in enumerate(alternativas):
            if alt and alt.strip():
                letra = chr(65 + i)  # A, B, C, D, E
                texto_entrada += f"{letra}) {alt}\n"
    
    texto_entrada += "\nQual é a alternativa correta? Responda apenas com A, B, C, D ou E."
    
    return {
        'input': texto_entrada,
        'output': resposta_correta,
        'id': questao.get('id', ''),
        'ano': questao.get('ano'),
        'area': questao.get('area', ''),
        'number': questao.get('number', '')
    }

def dividir_dataset(questoes_formatadas: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Divide dataset em treino/validação/teste
    
    Estratégia temporal:
    - Treino: 2009-2020 (70%)
    - Validação: 2021-2022 (15%)
    - Teste: 2023-2025 (15%)
    """
    treino = []
    validacao = []
    teste = []
    
    for questao in questoes_formatadas:
        ano = questao.get('ano')
        
        if ano is None:
            # Se não tem ano, distribuir aleatoriamente
            rand = random.random()
            if rand < 0.7:
                treino.append(questao)
            elif rand < 0.85:
                validacao.append(questao)
            else:
                teste.append(questao)
        elif 2009 <= ano <= 2020:
            treino.append(questao)
        elif 2021 <= ano <= 2022:
            validacao.append(questao)
        elif 2023 <= ano <= 2025:
            teste.append(questao)
        else:
            # Anos fora do range, adicionar ao treino
            treino.append(questao)
    
    return treino, validacao, teste

def salvar_dataset(dataset: List[Dict], output_file: Path):
    """Salva dataset em formato JSONL"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"💾 {len(dataset)} questões salvas em {output_file.name}")

def main():
    """Função principal"""
    print("=" * 70)
    print("📚 PREPARAÇÃO DE DATASET DE TREINAMENTO - ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    training_dir = project_root / "data" / "training"
    
    # Verificar dados
    if not processed_dir.exists():
        print(f"❌ Diretório não encontrado: {processed_dir}")
        print("   Execute primeiro: python scripts/analise_enem/01_carregar_dados_historico.py")
        return
    
    # Carregar todas as questões
    questoes = carregar_todas_questoes(processed_dir)
    
    if not questoes:
        print("❌ Nenhuma questão encontrada")
        return
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    stats_ano = defaultdict(int)
    stats_area = defaultdict(int)
    
    for q in questoes:
        ano = q.get('ano')
        area = q.get('area', 'unknown')
        if ano:
            stats_ano[ano] += 1
        stats_area[area] += 1
    
    print(f"   Anos: {len(stats_ano)}")
    print(f"   Áreas: {len(stats_area)}")
    for area, count in sorted(stats_area.items()):
        print(f"      {area}: {count} questões")
    
    # Formatar para treinamento
    print("\n🔄 Formatando questões para treinamento...")
    questoes_formatadas = [formatar_para_treinamento(q) for q in questoes]
    print(f"✅ {len(questoes_formatadas)} questões formatadas")
    
    # Dividir dataset
    print("\n📊 Dividindo dataset...")
    treino, validacao, teste = dividir_dataset(questoes_formatadas)
    
    print(f"   Treino: {len(treino)} questões (2009-2020)")
    print(f"   Validação: {len(validacao)} questões (2021-2022)")
    print(f"   Teste: {len(teste)} questões (2023-2025)")
    
    # Salvar datasets
    print("\n💾 Salvando datasets...")
    salvar_dataset(treino, training_dir / "train.jsonl")
    salvar_dataset(validacao, training_dir / "validation.jsonl")
    salvar_dataset(teste, training_dir / "test.jsonl")
    
    # Salvar estatísticas
    stats_file = training_dir / "dataset_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_questoes': len(questoes),
            'treino': len(treino),
            'validacao': len(validacao),
            'teste': len(teste),
            'stats_ano': dict(stats_ano),
            'stats_area': dict(stats_area)
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Estatísticas salvas em {stats_file.name}")
    
    print()
    print("=" * 70)
    print("✅ DATASET PREPARADO COM SUCESSO")
    print("=" * 70)
    print()
    print("📁 Arquivos criados:")
    print(f"   {training_dir / 'train.jsonl'}")
    print(f"   {training_dir / 'validation.jsonl'}")
    print(f"   {training_dir / 'test.jsonl'}")
    print()
    print("💡 Próximo passo:")
    print("   python scripts/analise_enem/93_treinar_modelo_enem.py")

if __name__ == "__main__":
    main()

