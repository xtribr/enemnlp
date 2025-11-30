#!/usr/bin/env python3
"""
Integra questões do dataset Alvorada-bench para treino

Carrega questões de FUVEST, ITA, IME, UNICAMP e converte para formato padrão,
indicando o exame de origem.
"""
import json
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from datasets import load_dataset
except ImportError:
    print("❌ Biblioteca 'datasets' não instalada")
    print("   Instale com: pip install datasets")
    sys.exit(1)

def mapear_area_alvorada(subject: str) -> str:
    """Mapeia área do Alvorada-bench para formato padrão"""
    subject_lower = subject.lower()
    
    # Mapeamento de áreas
    if any(x in subject_lower for x in ['português', 'portugues', 'língua', 'lingua', 'literatura', 'linguagens']):
        return 'languages'
    elif any(x in subject_lower for x in ['história', 'historia', 'geografia', 'filosofia', 'sociologia', 'humanas']):
        return 'human-sciences'
    elif any(x in subject_lower for x in ['física', 'fisica', 'química', 'quimica', 'biologia', 'natureza', 'ciências', 'ciencias']):
        return 'natural-sciences'
    elif any(x in subject_lower for x in ['matemática', 'matematica', 'matemática', 'math']):
        return 'mathematics'
    else:
        return 'unknown'

def converter_questao_alvorada(q: Dict, exam_type: str) -> Dict:
    """Converte questão do formato Alvorada-bench para formato padrão"""
    
    # Extrair dados
    question_id = q.get('question_id', '')
    question_statement = q.get('question_statement', '').strip()
    correct_answer = q.get('correct_answer', '').strip().upper()
    
    # Alternativas
    alternatives = []
    for letter in ['a', 'b', 'c', 'd', 'e']:
        alt_key = f'alternative_{letter}'
        alt_value = q.get(alt_key)
        if alt_value is not None:
            alt_value = str(alt_value).strip()
            if alt_value:
                alternatives.append(alt_value)
    
    # Área
    subject = q.get('subject', '')
    area = mapear_area_alvorada(subject)
    
    # Metadados
    exam_name = q.get('exam_name', '')
    exam_year = q.get('exam_year', '')
    
    # Criar questão no formato padrão
    questao = {
        'id': question_id,
        'exam': str(exam_year) if exam_year else 'unknown',
        'exam_type': exam_type,  # fuvest, ita, ime, unicamp
        'exam_name': exam_name,
        'area': area,
        'subject': subject,  # Manter subject original
        'number': q.get('question_number', ''),
        'context': '',  # Alvorada-bench não tem contexto separado
        'question': question_statement,
        'alternatives': alternatives[:5],  # Garantir máximo de 5
        'label': correct_answer if correct_answer in ['A', 'B', 'C', 'D', 'E'] else 'UNKNOWN',
        'has_images': False,  # Assumir que não há imagens
        'source': 'alvorada-bench'  # Marcar origem
    }
    
    # Validar questão
    if not questao['question']:
        return None
    
    if len(questao['alternatives']) < 5:
        # Preencher com strings vazias se necessário
        while len(questao['alternatives']) < 5:
            questao['alternatives'].append('')
    
    return questao

def carregar_questoes_alvorada(exam_types: List[str] = None) -> Dict[str, List[Dict]]:
    """Carrega questões do Alvorada-bench por tipo de exame"""
    
    if exam_types is None:
        # Excluir ENEM pois já temos
        exam_types = ['fuvest', 'ita', 'ime', 'unicamp']
    
    print("📥 Carregando dataset Alvorada-bench...")
    dataset = load_dataset("HenriqueGodoy/Alvorada-bench", "questions", split="train")
    print(f"✅ Dataset carregado! Total: {len(dataset)} questões")
    print()
    
    questoes_por_exame = {}
    
    for exam_type in exam_types:
        print(f"📊 Processando {exam_type.upper()}...")
        
        # Filtrar questões do tipo
        questoes_exame = dataset.filter(
            lambda x: x.get('exam_type', '').lower() == exam_type.lower()
        )
        
        print(f"   Total encontrado: {len(questoes_exame)} questões")
        
        # Converter questões
        questoes_convertidas = []
        for q in questoes_exame:
            questao_conv = converter_questao_alvorada(q, exam_type)
            if questao_conv:
                questoes_convertidas.append(questao_conv)
        
        questoes_por_exame[exam_type] = questoes_convertidas
        print(f"   ✅ {len(questoes_convertidas)} questões convertidas")
        
        # Estatísticas
        if questoes_convertidas:
            areas = {}
            for q in questoes_convertidas:
                area = q.get('area', 'unknown')
                areas[area] = areas.get(area, 0) + 1
            
            print(f"   Distribuição por área:")
            for area, count in sorted(areas.items()):
                print(f"      {area}: {count} questões")
        
        print()
    
    return questoes_por_exame

def salvar_questoes_treino(questoes_por_exame: Dict[str, List[Dict]], output_dir: Path):
    """Salva questões de treino por exame"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    total_questoes = 0
    
    for exam_type, questoes in questoes_por_exame.items():
        if not questoes:
            continue
        
        # Salvar por exame
        arquivo_exame = output_dir / f"treino_{exam_type}.jsonl"
        
        with open(arquivo_exame, 'w', encoding='utf-8') as f:
            for q in questoes:
                f.write(json.dumps(q, ensure_ascii=False) + '\n')
        
        print(f"💾 {exam_type.upper()}: {len(questoes)} questões salvas em {arquivo_exame.name}")
        total_questoes += len(questoes)
        
        # Salvar também um arquivo consolidado
        arquivo_consolidado = output_dir / "treino_alvorada_bench_completo.jsonl"
        with open(arquivo_consolidado, 'w', encoding='utf-8') as f:
            for exam, questoes_exam in questoes_por_exame.items():
                for q in questoes_exam:
                    f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print()
    print(f"✅ Total: {total_questoes} questões de treino salvas")
    print(f"📁 Arquivo consolidado: {output_dir / 'treino_alvorada_bench_completo.jsonl'}")
    
    return total_questoes

def main():
    """Função principal"""
    print("=" * 70)
    print("📚 INTEGRAÇÃO DE QUESTÕES DE TREINO - ALVORADA-BENCH")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "data" / "treino"
    
    # Carregar questões
    questoes_por_exame = carregar_questoes_alvorada()
    
    # Salvar questões
    print("💾 Salvando questões de treino...")
    total = salvar_questoes_treino(questoes_por_exame, output_dir)
    
    print()
    print("=" * 70)
    print("✅ INTEGRAÇÃO CONCLUÍDA")
    print("=" * 70)
    print()
    print("📊 Resumo:")
    for exam_type, questoes in questoes_por_exame.items():
        print(f"   {exam_type.upper()}: {len(questoes)} questões")
    print(f"\n   Total: {total} questões de treino")
    print()
    print("💡 As questões estão marcadas com:")
    print("   - exam_type: tipo do exame (fuvest, ita, ime, unicamp)")
    print("   - exam_name: nome completo do exame")
    print("   - source: 'alvorada-bench'")
    print()
    print("📁 Arquivos salvos em: data/treino/")

if __name__ == "__main__":
    main()

