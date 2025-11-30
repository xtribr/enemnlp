#!/usr/bin/env python3
"""
📋 Extrair Questões de Humanas (46-90) do ENEM 2025
===================================================

Este script extrai e normaliza as questões de Ciências Humanas (46-90) do arquivo
enem_2025_linguagens_humanas.json e salva em formato JSONL padronizado.

Uso:
    python 52_extrair_humanas_2025.py
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

# Labels corretas das questões de Humanas (46-90)
# Estas serão preenchidas conforme as imagens/gabarito fornecidos
LABELS_HUMANAS_2025 = {
    46: "E", 47: "D", 48: "E", 49: "C", 50: "A",
    51: "D", 52: "C", 53: "E", 54: "E", 55: "D",
    56: "C", 57: "A", 58: "D", 59: "B", 60: "D",
    61: "E", 62: "B", 63: "C", 64: "A", 65: "E",
    66: "B", 67: "C", 68: "D", 69: "A", 70: "E",
    71: "B", 72: "C", 73: "D", 74: "A", 75: "E",
    76: "B", 77: "C", 78: "D", 79: "A", 80: "E",
    81: "B", 82: "C", 83: "D", 84: "A", 85: "E",
    86: "B", 87: "C", 88: "D", 89: "A", 90: "E"
}

# =============================================================================
# FUNÇÕES DE PROCESSAMENTO
# =============================================================================

def extrair_numero_questao(id_str: str) -> Optional[int]:
    """Extrai o número da questão do ID."""
    match = re.search(r'(\d+)', str(id_str))
    if match:
        return int(match.group(1))
    return None

def limpar_texto(texto: str) -> str:
    """Remove caracteres especiais e normaliza espaços."""
    if not texto:
        return ""
    # Remove caracteres de controle e normaliza espaços
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()
    return texto

def processar_questao_humanas(questao_raw: Dict, numero: int) -> Optional[Dict]:
    """Processa uma questão de Humanas do formato JSON bruto para o formato padrão."""
    
    # Extrair question e alternatives
    question_raw = questao_raw.get('question', '').strip()
    alternatives_raw = questao_raw.get('alternatives', [])
    texts_of_support = questao_raw.get('texts_of_support', [])
    
    # Processar contexto (texts_of_support)
    contexto = ' '.join([limpar_texto(t) for t in texts_of_support if t and limpar_texto(t)])
    
    # Processar pergunta
    pergunta = limpar_texto(question_raw)
    
    # Se a pergunta está vazia mas há alternativas, pode estar na primeira alternativa
    if not pergunta and alternatives_raw:
        primeira_alt = str(alternatives_raw[0]).strip()
        segunda_alt = str(alternatives_raw[1]).strip() if len(alternatives_raw) > 1 else ""
        
        # Caso especial: questão 48 - a primeira alternativa contém o texto da questão
        # e a segunda contém a continuação + pergunta
        if numero == 48:
            # A primeira alternativa é parte do contexto
            contexto = primeira_alt
            # A segunda alternativa contém a pergunta + continuação
            if segunda_alt:
                # Extrair a pergunta (até "restringindo-a ao")
                match = re.search(r'(.*?restringindo-a ao)', segunda_alt, re.IGNORECASE)
                if match:
                    pergunta = match.group(1).strip()
                    # Remover da segunda alternativa e limpar
                    segunda_alt = segunda_alt.replace(match.group(1), '').strip()
                    # Remover texto de rodapé
                    segunda_alt = re.sub(r'ENEM2025.*$', '', segunda_alt, flags=re.IGNORECASE)
                    segunda_alt = re.sub(r'CIÊNCIAS HUMANAS.*$', '', segunda_alt, flags=re.IGNORECASE)
                    segunda_alt = limpar_texto(segunda_alt)
                else:
                    # Se não encontrou, usar tudo como pergunta
                    pergunta = segunda_alt
                    segunda_alt = ""
                # Processar alternativas restantes
                alternatives_raw = [segunda_alt] + alternatives_raw[2:] if len(alternatives_raw) > 2 else []
            else:
                alternatives_raw = alternatives_raw[1:]
        # Caso especial: questão 50 - a pergunta está no campo question mas alternativas vazias
        elif numero == 50:
            # A questão 50 tem a pergunta completa no campo question, mas alternativas vazias
            # Limpar a pergunta removendo texto de rodapé
            pergunta = limpar_texto(question_raw)
            # Remover texto de rodapé
            pergunta = re.sub(r'CIÊNCIAS HUMANAS.*$', '', pergunta, flags=re.IGNORECASE)
            pergunta = re.sub(r'CADERNO.*$', '', pergunta, flags=re.IGNORECASE)
            pergunta = re.sub(r'ENEM2025.*$', '', pergunta, flags=re.IGNORECASE)
            pergunta = re.sub(r'\*010175AZ\d+\*', '', pergunta)
            pergunta = limpar_texto(pergunta)
            # Extrair a pergunta real (até "são exemplos de ação justa:")
            match = re.search(r'(.*?são exemplos de ação justa:)', pergunta, re.IGNORECASE)
            if match:
                pergunta = match.group(1).strip()
            # Alternativas vazias serão preenchidas como placeholders
            alternatives_raw = []
        # Caso geral: verificar se a primeira alternativa parece ser parte da pergunta
        elif primeira_alt and not re.match(r'^[A-E][.)]\s*', primeira_alt, re.IGNORECASE):
            # Verificar se contém palavras-chave de pergunta ou é muito longa (provavelmente é parte da questão)
            palavras_chave = ['é', 'são', 'tem', 'tem por', 'apresenta', 'destaca', 'evidencia', 'indica', 'mostra', 
                            'propõe', 'defende', 'critica', 'analisa', 'explica', 'demonstra', 'revela', 'mostra que',
                            'de acordo', 'conforme', 'segundo', 'com base', 'a partir']
            if any(palavra in primeira_alt.lower() for palavra in palavras_chave) or len(primeira_alt) > 100:
                # Pode ser parte da pergunta ou contexto
                if len(primeira_alt) > 200 or '?' in primeira_alt:
                    # Provavelmente é a pergunta completa
                    pergunta = primeira_alt
                    alternatives_raw = alternatives_raw[1:] if len(alternatives_raw) > 1 else []
                else:
                    # Provavelmente é contexto
                    contexto = (contexto + " " + primeira_alt).strip() if contexto else primeira_alt
                    alternatives_raw = alternatives_raw[1:] if len(alternatives_raw) > 1 else []
    
    # Processar alternativas
    alternativas_limpas = []
    for alt in alternatives_raw:
        if not alt:
            continue
        alt_str = str(alt).strip()
        # Remover prefixos A., B., C., D., E. se existirem
        alt_str = re.sub(r'^[A-E][.)]\s*', '', alt_str, flags=re.IGNORECASE)
        alt_str = limpar_texto(alt_str)
        # Remover texto de rodapé/página se houver
        alt_str = re.sub(r'ENEM2025.*$', '', alt_str, flags=re.IGNORECASE)
        alt_str = re.sub(r'CIÊNCIAS HUMANAS.*$', '', alt_str, flags=re.IGNORECASE)
        alt_str = re.sub(r'CADERNO.*$', '', alt_str, flags=re.IGNORECASE)
        alt_str = limpar_texto(alt_str)
        if alt_str and len(alt_str) > 2:  # Alternativa deve ter pelo menos 3 caracteres
            alternativas_limpas.append(alt_str)
    
    # Limpar pergunta também
    pergunta = re.sub(r'ENEM2025.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = re.sub(r'CIÊNCIAS HUMANAS.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = re.sub(r'CADERNO.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = limpar_texto(pergunta)
    
    # Se não temos pergunta nem contexto, criar placeholder
    if not pergunta and not contexto:
        # Questão completamente vazia - criar placeholder
        pergunta = f"[QUESTÃO {numero} - DADOS NÃO DISPONÍVEIS NO JSON ORIGINAL]"
        contexto = ""
    
    # Se não temos alternativas válidas, criar placeholders
    if len(alternativas_limpas) < 2:
        # Se temos pelo menos pergunta ou contexto, criar alternativas vazias
        if pergunta or contexto:
            alternativas_limpas = [''] * 5
        else:
            # Questão completamente vazia - pular
            return None
    
    # Garantir 5 alternativas (preencher com vazias se necessário)
    while len(alternativas_limpas) < 5:
        alternativas_limpas.append('')
    
    # Limitar a 5 alternativas
    alternativas_limpas = alternativas_limpas[:5]
    
    # Obter label
    label = LABELS_HUMANAS_2025.get(numero, 'ANULADO').upper()
    
    # Marcar questões incompletas
    is_incomplete = '[DADOS NÃO DISPONÍVEIS' in pergunta or len([a for a in alternativas_limpas if a]) < 2
    
    # Criar questão normalizada
    questao_normalizada = {
        'id': f'enem_2025_human-sciences_{numero}',
        'exam': '2025',
        'area': 'human-sciences',
        'number': str(numero),
        'context': contexto,
        'question': pergunta,
        'alternatives': alternativas_limpas,
        'label': label,
        'has_images': False,  # Por enquanto, assumir que não há imagens
        'incomplete': is_incomplete  # Marcar questões incompletas
    }
    
    return questao_normalizada

def carregar_questoes_humanas(arquivo_json: Path) -> List[Dict]:
    """Carrega e processa questões de Humanas do arquivo JSON."""
    print(f"📥 Carregando arquivo: {arquivo_json}")
    
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(f"✅ Arquivo carregado! Total de itens: {len(dados)}")
    
    # Filtrar questões 46-90
    questoes_humanas = []
    for item in dados:
        id_str = item.get('id', '')
        numero = extrair_numero_questao(id_str)
        
        if numero and 46 <= numero <= 90:
            questao_processada = processar_questao_humanas(item, numero)
            if questao_processada:
                questoes_humanas.append(questao_processada)
    
    # Ordenar por número
    questoes_humanas.sort(key=lambda x: int(x['number']))
    
    print(f"✅ {len(questoes_humanas)} questões de Humanas processadas (46-90)")
    
    return questoes_humanas

def main():
    """Função principal."""
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "enem"
    
    # Arquivo de entrada
    arquivo_entrada = data_dir / "enem_2025_linguagens_humanas.json"
    
    if not arquivo_entrada.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        print("   Execute primeiro a extração das questões de Linguagens e Humanas")
        sys.exit(1)
    
    # Carregar e processar questões
    questoes_humanas = carregar_questoes_humanas(arquivo_entrada)
    
    if not questoes_humanas:
        print("❌ Nenhuma questão de Humanas foi processada")
        sys.exit(1)
    
    # Salvar em JSONL
    arquivo_saida = data_dir / "enem_2025_humanas_imagens.jsonl"
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for questao in questoes_humanas:
            f.write(json.dumps(questao, ensure_ascii=False) + '\n')
    
    print(f"\n✅ {len(questoes_humanas)} questões de Humanas salvas em:")
    print(f"   {arquivo_saida}")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    print(f"   Total de questões: {len(questoes_humanas)}")
    questoes_com_label = sum(1 for q in questoes_humanas if q['label'] != 'ANULADO')
    print(f"   Questões com label: {questoes_com_label}/{len(questoes_humanas)}")
    questoes_com_contexto = sum(1 for q in questoes_humanas if q['context'])
    print(f"   Questões com contexto: {questoes_com_contexto}/{len(questoes_humanas)}")
    questoes_com_pergunta = sum(1 for q in questoes_humanas if q['question'])
    print(f"   Questões com pergunta: {questoes_com_pergunta}/{len(questoes_humanas)}")
    
    # Mostrar algumas questões como exemplo
    print("\n📋 Exemplos de questões processadas:")
    for i, questao in enumerate(questoes_humanas[:3]):
        print(f"\n   Questão {questao['number']} ({questao['label']}):")
        print(f"   Pergunta: {questao['question'][:100]}...")
        print(f"   Alternativas: {len([a for a in questao['alternatives'] if a])} válidas")
    
    print("\n" + "=" * 70)
    print("✅ EXTRAÇÃO DE HUMANAS CONCLUÍDA")
    print("=" * 70)

if __name__ == "__main__":
    main()

