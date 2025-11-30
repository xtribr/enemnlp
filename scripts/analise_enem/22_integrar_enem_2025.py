#!/usr/bin/env python3
"""
Integrar dados do ENEM 2025

Processa e integra os dados do ENEM 2025 (JSON) ao sistema.
"""
import json
import sys
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def processar_questao_2025(questao: Dict, area: str, numero: int) -> Dict:
    """Processa uma questão do formato 2025 para o formato padrão"""
    # Extrair texto de suporte (contexto)
    textos_suporte = questao.get('texts_of_support', [])
    contexto = ' '.join([t.strip() for t in textos_suporte if t.strip()])
    
    # Extrair pergunta
    pergunta = questao.get('question', '').strip()
    
    # Se pergunta estiver vazia, tentar usar textos de suporte como pergunta
    # (algumas questões têm a pergunta no texts_of_support)
    if not pergunta and textos_suporte:
        # Tentar usar o último texto como pergunta se parecer uma pergunta
        ultimo_texto = textos_suporte[-1].strip()
        if ultimo_texto:
            # Se o último texto parece uma pergunta (tem ?) ou é curto, usar como pergunta
            if '?' in ultimo_texto or len(ultimo_texto) < 500:
                pergunta = ultimo_texto
                # Remover do contexto
                contexto = ' '.join([t.strip() for t in textos_suporte[:-1] if t.strip()])
            # Se não parece pergunta mas é o único texto, usar como pergunta mesmo assim
            elif len(textos_suporte) == 1:
                pergunta = ultimo_texto
                contexto = ''
    
    # Extrair alternativas
    alternativas = questao.get('alternatives', [])
    
    # Limpar alternativas (remover prefixos se houver)
    alternativas_limpas = []
    for alt in alternativas:
        if isinstance(alt, str):
            # Remover prefixos como "A. ", "B) ", etc.
            alt_limpa = alt.strip()
            if alt_limpa and alt_limpa[0] in ['A', 'B', 'C', 'D', 'E'] and len(alt_limpa) > 2:
                if alt_limpa[1] in ['.', ')', ':']:
                    alt_limpa = alt_limpa[2:].strip()
            alternativas_limpas.append(alt_limpa)
        else:
            alternativas_limpas.append(str(alt).strip())
    
    # Extrair ID
    questao_id = questao.get('id', f'questao_{numero}')
    
    # Mapear área
    area_map = {
        'linguagens_humanas': {
            'linguagens': ['languages', 'linguagens'],
            'humanas': ['human-sciences', 'humanas']
        },
        'natureza_matematica': {
            'natureza': ['natural-sciences', 'natureza'],
            'matematica': ['mathematics', 'matematica']
        }
    }
    
    # Determinar área específica (tentar inferir do conteúdo)
    area_especifica = None
    if 'linguagens' in area.lower() or 'humanas' in area.lower():
        # Primeiro 45 questões são linguagens, depois humanas
        if numero <= 45:
            area_especifica = 'languages'
        else:
            area_especifica = 'human-sciences'
    elif 'natureza' in area.lower():
        # Se já foi identificado como natureza, usar diretamente
        area_especifica = 'natural-sciences'
    elif 'matematica' in area.lower():
        # Se já foi identificado como matemática, usar diretamente
        area_especifica = 'mathematics'
    
    # Se não conseguiu inferir, usar padrão
    if not area_especifica:
        if 'linguagens' in area.lower():
            area_especifica = 'languages'
        elif 'humanas' in area.lower():
            area_especifica = 'human-sciences'
        elif 'natureza' in area.lower():
            area_especifica = 'natural-sciences'
        elif 'matematica' in area.lower():
            area_especifica = 'mathematics'
        else:
            area_especifica = 'desconhecida'
    
    # Criar questão normalizada
    questao_normalizada = {
        'id': f'enem_2025_{area_especifica}_{numero}',
        'exam': '2025',
        'area': area_especifica,
        'number': str(numero),
        'context': contexto,
        'question': pergunta,
        'alternatives': alternativas_limpas[:5],  # Garantir máximo de 5
        'label': 'ANULADO',  # Não temos a resposta correta no JSON
        'has_images': False  # Assumir que não há imagens por enquanto
    }
    
    # Validar questão - aceitar se tiver pelo menos contexto ou pergunta
    if not questao_normalizada['question'] and not questao_normalizada['context']:
        return None
    
    # Se não tem pergunta mas tem contexto, usar contexto como pergunta
    if not questao_normalizada['question'] and questao_normalizada['context']:
        questao_normalizada['question'] = questao_normalizada['context']
        questao_normalizada['context'] = ''
    
    # Aceitar questões com pelo menos 1 alternativa (preencher até 5)
    if len(questao_normalizada['alternatives']) == 0:
        # Se não tem alternativas, criar 5 vazias
        questao_normalizada['alternatives'] = [''] * 5
    elif len(questao_normalizada['alternatives']) < 5:
        # Preencher com strings vazias se necessário
        while len(questao_normalizada['alternatives']) < 5:
            questao_normalizada['alternatives'].append('')
    
    # Aceitar questão mesmo se tiver menos de 5 alternativas válidas
    # (melhor ter questão incompleta do que não ter nada)
    return questao_normalizada

def carregar_e_processar_2025(data_dir: Path) -> List[Dict]:
    """Carrega e processa todos os dados de 2025"""
    questoes_2025 = []
    
    # Arquivo 1: Linguagens e Humanas
    arquivo_lh = data_dir / "enem_2025_linguagens_humanas.json"
    if arquivo_lh.exists():
        print(f"📥 Carregando {arquivo_lh.name}...")
        with open(arquivo_lh, 'r', encoding='utf-8') as f:
            dados_lh = json.load(f)
        
        # Processar questões
        for i, questao in enumerate(dados_lh, 1):
            questao_proc = processar_questao_2025(questao, 'linguagens_humanas', i)
            if questao_proc:
                questoes_2025.append(questao_proc)
        
        print(f"  ✅ {len(dados_lh)} questões processadas")
    
    # Arquivo 2: Natureza e Matemática
    arquivo_nm = data_dir / "enem_2025_natureza_matematica.json"
    if arquivo_nm.exists():
        print(f"📥 Carregando {arquivo_nm.name}...")
        with open(arquivo_nm, 'r', encoding='utf-8') as f:
            dados_nm = json.load(f)
        
        # Processar questões (continuar numeração)
        inicio_num = len(questoes_2025) + 1
        for i, questao in enumerate(dados_nm, 1):
            # Para natureza_matematica, as primeiras 45 questões são Natureza
            # Usar número relativo dentro do arquivo para determinar área
            numero_relativo = i
            numero_absoluto = inicio_num + i - 1
            
            # Determinar área baseado na posição relativa no arquivo
            if numero_relativo <= 45:
                area_arquivo = 'natureza'
            else:
                area_arquivo = 'matematica'
            
            questao_proc = processar_questao_2025(questao, area_arquivo, numero_absoluto)
            if questao_proc:
                questoes_2025.append(questao_proc)
        
        print(f"  ✅ {len(dados_nm)} questões processadas")
    
    return questoes_2025

def salvar_dados_2025(questoes: List[Dict], output_dir: Path):
    """Salva dados de 2025 no formato padrão"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arquivo = output_dir / "enem_2025_completo.jsonl"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        for questao in questoes:
            f.write(json.dumps(questao, ensure_ascii=False) + '\n')
    
    print(f"💾 {len(questoes)} questões salvas em {arquivo.name}")
    
    # Estatísticas por área
    areas_count = {}
    for questao in questoes:
        area = questao.get('area', 'desconhecida')
        areas_count[area] = areas_count.get(area, 0) + 1
    
    print("\n📊 Distribuição por área:")
    for area, count in sorted(areas_count.items()):
        print(f"   {area:20s}: {count:3d} questões")

def main():
    """Função principal"""
    print("=" * 70)
    print("📥 INTEGRAÇÃO DE DADOS ENEM 2025")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "enem"
    processed_dir = project_root / "data" / "processed"
    
    # Carregar e processar dados de 2025
    print("🔄 Processando dados de 2025...")
    questoes_2025 = carregar_e_processar_2025(data_dir)
    
    if not questoes_2025:
        print("❌ Nenhuma questão processada")
        return
    
    print(f"\n✅ Total: {len(questoes_2025)} questões processadas")
    
    # Salvar dados processados
    print("\n💾 Salvando dados processados...")
    salvar_dados_2025(questoes_2025, processed_dir)
    
    print()
    print("=" * 70)
    print("✅ INTEGRAÇÃO DE DADOS 2025 CONCLUÍDA")
    print("=" * 70)
    print()
    print("⚠️  NOTA: As questões de 2025 não têm respostas corretas (label)")
    print("   Elas foram marcadas como 'ANULADO' até que as respostas sejam adicionadas")
    print()
    print("💡 Próximos passos:")
    print("   1. Adicionar respostas corretas quando disponíveis")
    print("   2. Executar análises com os novos dados")

if __name__ == "__main__":
    main()


