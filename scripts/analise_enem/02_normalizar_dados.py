#!/usr/bin/env python3
"""
Normaliza dados do ENEM corrigindo problemas encontrados na validação
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def normalizar_questao(questao: dict, ano: int) -> dict:
    """Normaliza uma questão corrigindo problemas comuns"""
    # Normalizar label (minúscula -> maiúscula)
    if 'label' in questao:
        label = str(questao['label']).upper().strip()
        if label in ['A', 'B', 'C', 'D', 'E']:
            questao['label'] = label
    
    # Garantir que alternatives é uma lista
    if 'alternatives' not in questao or not isinstance(questao['alternatives'], list):
        # Tentar extrair de campos A, B, C, D, E
        alternatives = []
        for letra in ['A', 'B', 'C', 'D', 'E']:
            if letra in questao:
                alternatives.append(str(questao[letra]).strip())
        if len(alternatives) == 5:
            questao['alternatives'] = alternatives
    
    # Normalizar área de conhecimento
    if 'area' not in questao or not questao['area']:
        # Tentar inferir do ID ou contexto
        id_str = str(questao.get('id', '')).lower()
        if 'linguagem' in id_str or 'language' in id_str:
            questao['area'] = 'languages'
        elif 'human' in id_str or 'humanas' in id_str:
            questao['area'] = 'human-sciences'
        elif 'natureza' in id_str or 'nature' in id_str:
            questao['area'] = 'natural-sciences'
        elif 'matematica' in id_str or 'math' in id_str:
            questao['area'] = 'mathematics'
    
    # Garantir campos obrigatórios
    if 'exam' not in questao:
        questao['exam'] = str(ano)
    
    if 'id' not in questao:
        questao['id'] = f"enem_{ano}_{questao.get('number', 'unknown')}"
    
    # Limpar strings
    for campo in ['question', 'context']:
        if campo in questao:
            questao[campo] = str(questao[campo]).strip()
    
    return questao

def normalizar_arquivo(jsonl_file: Path) -> tuple[int, int]:
    """Normaliza um arquivo JSONL"""
    questoes_normalizadas = []
    questoes_corrigidas = 0
    
    # Carregar questões
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        questoes = [json.loads(line) for line in f if line.strip()]
    
    # Extrair ano do nome do arquivo
    ano = int(jsonl_file.stem.split('_')[1])
    
    # Normalizar cada questão
    for questao in questoes:
        questao_original = questao.copy()
        questao_normalizada = normalizar_questao(questao, ano)
        
        # Verificar se houve mudanças
        if questao_original != questao_normalizada:
            questoes_corrigidas += 1
        
        questoes_normalizadas.append(questao_normalizada)
    
    # Salvar arquivo normalizado
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for questao in questoes_normalizadas:
            f.write(json.dumps(questao, ensure_ascii=False) + '\n')
    
    return len(questoes_normalizadas), questoes_corrigidas

def main():
    """Função principal"""
    print("=" * 70)
    print("🔧 NORMALIZAÇÃO DE DADOS DO ENEM")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    if not processed_dir.exists():
        print(f"❌ Diretório não encontrado: {processed_dir}")
        return
    
    print("📥 Normalizando arquivos...")
    total_questoes = 0
    total_corrigidas = 0
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes, corrigidas = normalizar_arquivo(jsonl_file)
        total_questoes += questoes
        total_corrigidas += corrigidas
        print(f"  {ano}: {questoes} questões, {corrigidas} corrigidas")
    
    print()
    print("=" * 70)
    print(f"✅ NORMALIZAÇÃO CONCLUÍDA")
    print(f"   Total: {total_questoes} questões")
    print(f"   Corrigidas: {total_corrigidas} questões")
    print("=" * 70)

if __name__ == "__main__":
    main()


