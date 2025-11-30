#!/usr/bin/env python3
"""
📸 Extração de Questões ENEM 2025 a partir de Imagens
======================================================

Este script processa as descrições das imagens da prova ENEM 2025
e extrai as questões no formato padrão do projeto.

Uso:
    python 47_extrair_questoes_2025_imagens.py
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

# =============================================================================
# DADOS EXTRAÍDOS DAS IMAGENS - LINGUAGENS 2025 (01-45)
# =============================================================================

# Questões extraídas das descrições das imagens fornecidas
QUESTOES_LINGUAGENS_2025 = [
    # Questões 01-05 (Inglês)
    {
        "id": "QUESTÃO 01",
        "numero": 1,
        "area": "languages",
        "context": "",
        "question": "Glory Ames, from the White Earth reservation, is frustrated that despite the presence of several indigenous reservations near Moorhead, local Halloween stores still feature a western section with costumes such as \"pow wow princess\". Even worse, despite a long-running debate about racism and cultural appropriation, often prompted by backlash against celebrities and politicians for donning offensive costumes, people continue to wear such costumes. Last Halloween, Ames spotted a photo on Instagram of a girl dressed as a Native American with a bullet in her forehead. She immediately reported it to the social media platform and had it removed. \"They blatantly take certain aspects of our culture, race, religion, and use it for their advantage and ignore the people living it\", said Ames. Ao abordar um aspecto da celebração do Halloween, esse texto tem por objetivo",
        "alternatives": [
            "denunciar a violência contra crianças indígenas.",
            "descrever costumes tradicionais em celebrações indígenas.",
            "valorizar as vestimentas características dos povos originários.",
            "criticar a exploração indevida de elementos da identidade indígena.",
            "sugerir ações de combate ao preconceito contra os povos originários."
        ],
        "label": "D",
        "source": "LIU, M. C. M. Disponível em: www.washingtonpost.com. Acesso em: 12 maio 2024 (adaptado)."
    },
    {
        "id": "QUESTÃO 02",
        "numero": 2,
        "area": "languages",
        "context": "",
        "question": "My idea of philosophy is that if it is not relevant to human problems, if it does not tell us how we can go about eradicating some of the misery in this world, then it is not worth the name of philosophy. I think Socrates made a very profound statement when he asserted that philosophy is to teach us proper living. In this day and age \"proper living\" means liberation from the urgent problems of poverty, economic necessity and indoctrination, mental oppression. Nesse texto, ao discorrer sobre a relevância da filosofia, a escritora Angela Davis tem por objetivo",
        "alternatives": [
            "criticá-la pela restrição temática.",
            "vinculá-la ao universo acadêmico.",
            "afastá-la da abordagem socrática.",
            "aproximá-la dos problemas sociais.",
            "responsabilizá-la pela pobreza humana."
        ],
        "label": "D",
        "source": "DAVIS, A. Lectures on Liberation. Washington: Smithsonian Libraries, 1971 (adaptado)."
    },
    {
        "id": "QUESTÃO 03",
        "numero": 3,
        "area": "languages",
        "context": "",
        "question": "Remember the sky that you were born under, know each of the star's stories. Remember the moon, know who she is. Remember the sun's birth at dawn. [...] Remember your birth, how your mother struggled to give you form and breath [...] Remember the earth whose skin you are: red earth, black earth, yellow earth, white earth brown earth, we are earth. Remember the plants, trees, animal life who all have their tribes, their families, their histories, too [...] Remember you are all people and all people are you. Remember you are this universe and this universe is you. Remember all is in motion, is growing, is you. Nesse poema, de uma autora de ascendência indígena, o eu lírico ressalta a",
        "alternatives": [
            "potência dos astros celestes.",
            "origem das plantas e dos animais.",
            "importância do apego à terra natal.",
            "relação entre seres humanos e natureza.",
            "conexão entre o tempo real e o tempo imaginário."
        ],
        "label": "D",
        "source": "HARJO, J. She Had Some Horses. Londres: W. Norton & Company, 1983 (fragmento)."
    },
    {
        "id": "QUESTÃO 04",
        "numero": 4,
        "area": "languages",
        "context": "",
        "question": "It is true that all children are special, simply because they are children. But most adults are not special, and children end up as adults pretty quickly. Life then can be difficult and even disappointing. The shock of this may account for the emergence of the \"snowflake generation\" of university students, who are so delicate they can't handle controversial ideas being put forward in their lectures. The roots of this fragility run deep in modern culture. So, an approach of the world that states: \"Life is wonderful, you're special and, if you are a good boy/girl, life will be amazing forever\" is not a message designed to aid bouncing back from failure or confronting catastrophe. Resilience is not about feeding ego — telling your children how wonderful they are — but strengthening it. Nesse texto, a expressão \"snowflake generation\" é usada para",
        "alternatives": [
            "abordar obstáculos impostos a universitários.",
            "destacar mensagens de incentivo a estudantes.",
            "estimular ações proativas em situações de emergência.",
            "retratar relações conflituosas em ambiente universitário.",
            "apontar posturas de uma juventude avessa a contrariedades."
        ],
        "label": "E",
        "source": "LOTT, T. Disponível em: www.theguardian.com. Acesso em: 10 dez. 2017 (adaptado)."
    },
    {
        "id": "QUESTÃO 05",
        "numero": 5,
        "area": "languages",
        "context": "",
        "question": "Nesse texto, a pergunta \"What is sleep?\", em uma das embalagens do produto, está relacionada ao(à)",
        "alternatives": [
            "escassez de horas de sono.",
            "estímulo a um descanso de qualidade.",
            "gasto com bebidas que combatem a insônia.",
            "consumo de bebidas que causam dependência.",
            "necessidade de um produto que provoque o sono."
        ],
        "label": "A",
        "source": "Disponível em: https://pt.foursquare.com. Acesso em: 14 maio 2024.",
        "has_image": True,
        "image_description": "Fotografia de uma cafeteria/padaria. No primeiro plano, uma vitrine de vidro contém dois muffins de mirtilo em um forro de papel marrom, com um pequeno rótulo branco na frente dizendo \"Blueberry Muffins\". Atrás da vitrine, em um balcão, há três copos de papel brancos de tamanhos diferentes. O copo da esquerda, rotulado \"16 ounce\", tem a pergunta \"WHAT IS SLEEP?\" escrita em letras grandes, negras e sans-serif. O copo do meio, rotulado \"12 ounce\", tem \"SLEPT 5-7 HOURS\" escrito. O copo da direita, rotulado \"8 ounce\", tem \"SLEPT 8-10 HOURS\" escrito."
    },
    # Questões 06-10: Texto "De próprio punho"
    {
        "id": "QUESTÃO 06",
        "numero": 6,
        "area": "languages",
        "context": "Texto 'De próprio punho' - A escrita e suas tecnologias sofrem interessantes metamorfoses, numa ciranda que vai do simples bilhete aos originais de um livro...",
        "question": "No que diz respeito ao gênero bilhete, a autora dessa crônica",
        "alternatives": [
            "ressalta a formalidade na comunicação com as pessoas de sua convivência.",
            "critica a ansiedade causada pela velocidade da comunicação.",
            "expressa a obrigatoriedade de concisão nas anotações.",
            "questiona a prática da escrita de próprio punho.",
            "apresenta a diversidade de usos no cotidiano."
        ],
        "label": "E",
        "source": "RIBEIRO, A. E. Disponível em: https://rascunho.com.br. Acesso em: 16 jan. 2024 (adaptado)."
    },
    {
        "id": "QUESTÃO 07",
        "numero": 7,
        "area": "languages",
        "context": "Texto 'De próprio punho'",
        "question": "O elemento que caracteriza esse texto como uma crônica é a",
        "alternatives": [
            "defesa das opiniões da autora sobre um tema de interesse coletivo.",
            "exposição sobre o uso de tecnologias nas práticas de escrita atuais.",
            "abordagem de fatos do contexto pessoal em uma perspectiva reflexiva.",
            "utilização de recursos linguísticos para a interlocução direta com o leitor.",
            "apresentação de acontecimentos segundo a ordem de sucessão no tempo."
        ],
        "label": "C",
        "source": "RIBEIRO, A. E. Disponível em: https://rascunho.com.br. Acesso em: 16 jan. 2024 (adaptado)."
    },
    {
        "id": "QUESTÃO 08",
        "numero": 8,
        "area": "languages",
        "context": "Texto 'De próprio punho'",
        "question": "Nesse texto, o que caracteriza a escrita \"de próprio punho\" é a letra manuscrita, enquanto a escrita digital é ilustrada pelo(a)",
        "alternatives": [
            "utilização de tecnologias diversificadas.",
            "desenvolvimento de novos recursos de escrita.",
            "possibilidade de interações mediadas por telas.",
            "diversidade de fontes tipográficas que estão disponíveis.",
            "delimitação dos espaços onde a produção textual ocorre."
        ],
        "label": "D",
        "source": "RIBEIRO, A. E. Disponível em: https://rascunho.com.br. Acesso em: 16 jan. 2024 (adaptado)."
    },
    {
        "id": "QUESTÃO 09",
        "numero": 9,
        "area": "languages",
        "context": "Texto 'De próprio punho'",
        "question": "A autora conclui que as novas tecnologias de escrita",
        "alternatives": [
            "evoluem para facilitar a vida cotidiana.",
            "alcançam diferentes realidades sociais.",
            "coexistem com outras já estabelecidas.",
            "promovem maior agilidade na comunicação.",
            "surgem nos contextos em que são necessárias."
        ],
        "label": "C",
        "source": "RIBEIRO, A. E. Disponível em: https://rascunho.com.br. Acesso em: 16 jan. 2024 (adaptado)."
    },
    {
        "id": "QUESTÃO 10",
        "numero": 10,
        "area": "languages",
        "context": "Texto 'De próprio punho'",
        "question": "O recurso linguístico usado para marcar a síntese da opinião da autora sobre a temática desenvolvida foi o(a)",
        "alternatives": [
            "emprego da primeira pessoa em \"Estranhei muito na primeira vez que escutei a expressão 'de próprio punho'\". (l. 1)",
            "utilização de locução adverbial em \"Na verdade, o que importava era a autenticidade da minha caligrafia\". (l. 3-4)",
            "uso de pronome possessivo em \"Minha letra, hoje, tem uma espécie de alternância\". (l. 5-6)",
            "adoção de termo autorreflexivo em \"No escritório, costumo ser mais suave comigo mesma\". (l. 30)",
            "substituição da expressão \"Do punho ao pixel\" (l. 44) pela expressão \"o punho e o pixel\". (l. 45)"
        ],
        "label": "E",
        "source": "RIBEIRO, A. E. Disponível em: https://rascunho.com.br. Acesso em: 16 jan. 2024 (adaptado)."
    },
    # Questões 11-45 (continuar extraindo das imagens)
    # Por enquanto, vou criar a estrutura e depois podemos adicionar mais
]

# =============================================================================
# FUNÇÕES DE PROCESSAMENTO
# =============================================================================

def normalizar_questao(questao: Dict, numero_global: int) -> Dict:
    """Normaliza uma questão para o formato padrão do projeto."""
    
    area = questao.get('area', 'languages')
    
    questao_normalizada = {
        'id': f'enem_2025_{area}_{numero_global}',
        'exam': '2025',
        'area': area,
        'number': str(numero_global),
        'context': questao.get('context', ''),
        'question': questao.get('question', '').strip(),
        'alternatives': questao.get('alternatives', []),
        'label': questao.get('label', 'ANULADO').upper(),
        'has_images': questao.get('has_image', False),
        'source': questao.get('source', '')
    }
    
    # Adicionar descrição de imagem se houver
    if questao.get('image_description'):
        questao_normalizada['image_description'] = questao.get('image_description')
    
    return questao_normalizada


def processar_questoes_linguas(questoes: List[Dict]) -> List[Dict]:
    """Processa questões de Linguagens (01-45)."""
    questoes_processadas = []
    
    for i, q in enumerate(questoes, 1):
        questao_norm = normalizar_questao(q, i)
        if questao_norm['question'] or questao_norm['context']:
            questoes_processadas.append(questao_norm)
    
    return questoes_processadas


def salvar_questoes(questoes: List[Dict], arquivo: Path):
    """Salva questões em formato JSONL."""
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        for q in questoes:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"✅ {len(questoes)} questões salvas em {arquivo}")


def main():
    """Função principal."""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "data" / "enem"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("📸 EXTRAÇÃO DE QUESTÕES ENEM 2025 - LINGUAGENS")
    print("=" * 70)
    print()
    
    # Processar questões de Linguagens
    print("📝 Processando questões de Linguagens...")
    questoes_ling = processar_questoes_linguas(QUESTOES_LINGUAGENS_2025)
    
    print(f"✅ {len(questoes_ling)} questões processadas")
    print()
    
    # Estatísticas
    print("📊 Estatísticas:")
    print(f"   Total de questões: {len(questoes_ling)}")
    
    # Verificar questões com imagens
    com_imagens = sum(1 for q in questoes_ling if q.get('has_images', False))
    print(f"   Questões com imagens: {com_imagens}")
    
    # Verificar questões com gabarito
    com_gabarito = sum(1 for q in questoes_ling if q.get('label') != 'ANULADO')
    print(f"   Questões com gabarito: {com_gabarito}")
    print()
    
    # Salvar
    arquivo_ling = output_dir / "enem_2025_linguagens_extraido.jsonl"
    salvar_questoes(questoes_ling, arquivo_ling)
    
    print()
    print("=" * 70)
    print("✅ EXTRAÇÃO CONCLUÍDA")
    print("=" * 70)
    print()
    print("📝 Próximos passos:")
    print("   1. Aguardar imagens de Natureza e Matemática")
    print("   2. Processar todas as questões juntas")
    print("   3. Integrar com o sistema existente")
    print()
    print("💡 Nota: Este é um script inicial. Complete as questões 11-45")
    print("   baseado nas imagens fornecidas.")


if __name__ == "__main__":
    main()
