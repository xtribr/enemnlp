#!/usr/bin/env python3
"""
📋 Extrair Questões de Natureza (91-135) e Matemática (136-180) do ENEM 2025
================================================================================

Este script extrai e normaliza as questões de Ciências da Natureza (91-135) e
Matemática (136-180) do arquivo enem_2025_natureza_matematica.json e das imagens
fornecidas, salvando em formato JSONL padronizado.

Uso:
    python 53_extrair_natureza_matematica_2025.py
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# =============================================================================
# CONFIGURAÇÕES - Labels corretas das questões
# =============================================================================

# Labels corretas das questões de Natureza (91-135)
LABELS_NATUREZA_2025 = {
    91: "C", 92: "B", 93: "D", 94: "D", 95: "C",
    96: "D", 97: "A", 98: "E", 99: "A", 100: "A",
    101: "C", 102: "C", 103: "C", 104: "B", 105: "B",
    106: "C", 107: "E", 108: "A", 109: "E", 110: "E",
    111: "B", 112: "D", 113: "E", 114: "D", 115: "C",
    116: "A", 117: "B", 118: "B", 119: "B", 120: "D",
    121: "E", 122: "C", 123: "D", 124: "C", 125: "B",
    126: "A", 127: "C", 128: "D", 129: "A", 130: "C",
    131: "A", 132: "D", 133: "D", 134: "C", 135: "C"
}

# Labels corretas das questões de Matemática (136-180)
LABELS_MATEMATICA_2025 = {
    136: "C", 137: "C", 138: "C", 139: "B", 140: "E",
    141: "B", 142: "D", 143: "B", 144: "B", 145: "B",
    146: "C", 147: "B", 148: "C", 149: "B", 150: "C",
    151: "B", 152: "D", 153: "D", 154: "D", 155: "A",
    156: "A", 157: "E", 158: "C", 159: "E", 160: "B",
    161: "D", 162: "B", 163: "E", 164: "C", 165: "D",
    166: "D", 167: "A", 168: "A", 169: "E", 170: "A",
    171: "A", 172: "B", 173: "C", 174: "E", 175: "A",
    176: "D", 177: "A", 178: "B", 179: "D", 180: "C"
}

# =============================================================================
# QUESTÕES EXTRAÍDAS DAS IMAGENS - Natureza (91-135)
# =============================================================================

QUESTOES_NATUREZA_IMAGENS = [
    {
        "numero": 91,
        "context": "TEXTO I: As mariposas - As mariposas voam em torno da lâmpada para se aquecerem. TEXTO II: As mariposas são atraídas pela luz (fototaxia) e o calor das lâmpadas incandescentes pode aquecê-las. O poema descreve uma consequência, não a causa.",
        "question": "Nesse contexto, o processo de transferência de calor para as mariposas que independe da presença de fluidos é a",
        "alternatives": [
            "reflexão.",
            "refração.",
            "irradiação.",
            "dispersão.",
            "convecção."
        ],
        "label": "C"
    },
    {
        "numero": 92,
        "question": "Os sapinhos-ponta-de-flecha da América Central e do Sul têm veneno que vem da alimentação de formigas e cupins que consomem plantas tóxicas. Esses anfíbios são usados para envenenar dardos por caçadores nativos. Quando capturados, criados em condições artificiais ou nascidos em cativeiro, não são tóxicos. A perda da capacidade de se obter a toxina nos nascidos em cativeiro é causada pela",
        "alternatives": [
            "diferença de umidade entre os ambientes.",
            "ausência de alimentação natural.",
            "adaptação ao novo ambiente.",
            "mudança de comportamento.",
            "variabilidade genética."
        ],
        "label": "B"
    },
    {
        "numero": 93,
        "question": "O antígeno utilizado na vacina causa um efeito protetor contra o vírus porque",
        "alternatives": [
            "mata o vírus pela ligação.",
            "aglutina o vírus por associação.",
            "contém imunoglobulinas de defesa.",
            "induz a produção de proteínas neutralizadoras.",
            "mantém a quantidade de anticorpos preexistentes."
        ],
        "label": "D",
        "has_image": True,
        "image_description": "Diagrama mostrando o processo de produção de vacina: isolamento de vírus, inativação, aplicação da vacina e produção de anticorpos."
    },
    {
        "numero": 94,
        "question": "O Cerrado apresenta ampla diversidade natural de espécies vegetais. O ser humano tem modificado esse ambiente pela introdução de plantas exóticas, como o capim-gordura, nativo da África, utilizado para pastagem. Essa espécie se espalha amplamente devido à sua agressividade e poder competitivo. Em longo prazo, essa ação do homem pode gerar qual consequência?",
        "alternatives": [
            "Diversificar nichos ecológicos.",
            "Assorear as nascentes do bioma.",
            "Dificultar a infiltração de água na terra.",
            "Diminuir as espécies nativas do bioma.",
            "Contribuir com a redução das queimadas."
        ],
        "label": "D"
    },
    {
        "numero": 95,
        "question": "O monstro-de-gila é um lagarto do deserto dos Estados Unidos. Para sobreviver à escassez de alimentos, ele desenvolveu adaptações, incluindo um hormônio que controla os níveis de açúcar no sangue, o que tem implicações para pessoas com diabetes. Animais do mesmo grupo taxonômico podem ter adaptações semelhantes em ambientes semelhantes. Nessas condições, lagartos com características adaptativas semelhantes seriam mais prováveis de serem encontrados em qual região do Brasil?",
        "alternatives": [
            "Cerrado",
            "Pampas",
            "Caatinga",
            "Restinga",
            "Pantanal"
        ],
        "label": "C"
    },
    {
        "numero": 96,
        "question": "O processo de purificação de água que remove os sais dissolvidos é usado em laboratórios de química, indústrias (como solvente) e baterias de carros. Esse tipo de água não é adequado para consumo, pois pode causar problemas de saúde como deficiência iônica e diarreia. Qual é o nome desse tipo de água?",
        "alternatives": [
            "dura",
            "pesada",
            "sanitária",
            "destilada",
            "oxigenada"
        ],
        "label": "D"
    },
    {
        "numero": 97,
        "question": "Por que os olhos ficam vermelhos em algumas fotografias? Em fotos antigas, as pessoas às vezes têm olhos vermelhos porque a luz do flash da câmera atinge diretamente o globo ocular e é refletida por uma região rica em vasos sanguíneos. Por que esse efeito é mais comum à noite ou em locais com pouca luz, relacionando-se com a pupila?",
        "alternatives": [
            "dilatada, chega mais luz à retina",
            "retraída, chega mais luz vermelha à retina",
            "retraída, chega mais luz vermelha aos bastonetes",
            "retraída, chegam menos luzes azul e verde aos cones",
            "dilatada, chegam menos luzes azul e verde aos bastonetes"
        ],
        "label": "A"
    },
    {
        "numero": 98,
        "question": "O sashimi (filé de peixe cru) de baiacu é uma iguaria no Japão, mas sua ingestão pode causar morte por parada respiratória devido a uma potente neurotoxina termoestável (tetrodotoxina) produzida e armazenada nas gônadas e vísceras. Qual ação poderia prevenir essa intoxicação?",
        "alternatives": [
            "Criar os peixes em cativeiro",
            "Realizar a pesca com redes",
            "Consumir peixes cozidos ou fritos",
            "Preparar o peixe em condições adequadas de higiene",
            "Manusear o peixe sem provocar o rompimento dos órgãos internos"
        ],
        "label": "E"
    },
    {
        "numero": 99,
        "question": "Uma doença causada pela deficiência da enzima lipase ácida, em que as células do indivíduo afetado não degradam o colesterol esterificado nem os triglicerídeos, levando ao acúmulo desses compostos em vários órgãos, especialmente no fígado. Qual estrutura celular cuja insuficiência funcional resulta nessa doença?",
        "alternatives": [
            "Lisossomos",
            "Ribossomos",
            "Mitocôndrias",
            "Peroxissomos",
            "Retículo endoplasmático liso"
        ],
        "label": "A"
    },
    {
        "numero": 100,
        "question": "O CO₂ atmosférico aumentou 50%, e a temperatura está agora cerca de 1,2 °C mais quente do que no século XIX. É necessário desacelerar a taxa de aumento da temperatura para evitar as piores consequências das mudanças climáticas, visando manter o aquecimento global em 1,5 °C até 2100. Sem ações adicionais, o planeta pode aquecer mais de 2 °C até o final do século, e os países precisam implementar ações mitigadoras para reduzir as emissões e os níveis de CO₂. Qual ação mitigadora ajuda a remover esse gás da atmosfera, reduzindo seus níveis?",
        "alternatives": [
            "Plantar mais árvores",
            "Instalar mais usinas eólicas",
            "Ampliar o uso de energia solar",
            "Manter os combustíveis fósseis no solo",
            "Produzir menos resíduos sólidos urbanos"
        ],
        "label": "A"
    },
    {
        "numero": 101,
        "question": "Os espectros de fotoluminescência do sensor no início e no final do tratamento estão esboçados no gráfico:",
        "alternatives": [
            "Gráfico A: espectro final com menor intensidade, sem mudança de comprimento de onda",
            "Gráfico B: espectro final deslocado para maior comprimento de onda",
            "Gráfico C: espectro final deslocado para menor comprimento de onda (maior frequência)",
            "Gráfico D: espectro final idêntico ao inicial",
            "Gráfico E: espectro final com menor intensidade e deslocado para menor comprimento de onda"
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Gráfico de fotoluminescência mostrando espectro inicial (linha sólida) e final (linha tracejada). O espectro final está deslocado para menor comprimento de onda (maior frequência), indicando mudança de cor de vermelho-laranja para verde."
    },
    {
        "numero": 102,
        "question": "Qual alternativa representa a proporção fenotípica da prole resultante do cruzamento entre indivíduos da primeira geração?",
        "alternatives": [
            "A: Todos com duas manchas",
            "B: Todos com uma faixa",
            "C: Três com duas manchas, um com uma faixa",
            "D: Dois com duas manchas, dois com uma faixa",
            "E: Um com duas manchas, três com uma faixa"
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Diagrama de herança genética mostrando cruzamento de insetos: macho com duas manchas x fêmea com uma faixa produz primeira geração com duas manchas. Cruzamento da primeira geração produz 3:1 (três com duas manchas, um com uma faixa)."
    },
    {
        "numero": 103,
        "question": "O comportamento da força de atrito entre a caixa e o chão no plano inclinado é representado em:",
        "alternatives": [
            "Gráfico A: força constante que diminui e depois aumenta",
            "Gráfico B: força que aumenta e depois diminui abruptamente",
            "Gráfico C: força constante",
            "Gráfico D: força alta constante que diminui linearmente",
            "Gráfico E: força baixa que aumenta e depois diminui"
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Gráfico mostrando força de atrito constante ao longo do tempo durante o arrasto da caixa no plano inclinado."
    },
    {
        "numero": 104,
        "question": "Nessa situação, qual ponto da tela será atingido pelo feixe de elétrons?",
        "alternatives": [
            "1",
            "2",
            "3",
            "4",
            "5"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Diagrama de tubo de imagem mostrando feixe de elétrons sendo defletido por campo elétrico e atingindo ponto 2 na tela."
    },
    {
        "numero": 105,
        "question": "Esse fenômeno e a característica associada à voz da Mônica são, respectivamente,",
        "alternatives": [
            "reflexão e comprimento de onda.",
            "ressonância e frequência.",
            "interferência e velocidade.",
            "ressonância e timbre.",
            "reflexão e amplitude."
        ],
        "label": "B",
        "has_image": True,
        "image_description": "História em quadrinhos da Turma da Mônica mostrando Mônica gritando e quebrando copos de cristal por ressonância."
    },
    {
        "numero": 106,
        "question": "O frasco contendo cânfora apresenta a fórmula molecular:",
        "alternatives": [
            "C9H16O",
            "C9H17O",
            "C10H16O",
            "C10H16O2",
            "C10H18O2"
        ],
        "label": "C"
    },
    {
        "numero": 107,
        "question": "Para o ecossistema aquático, a ineficiência do sistema de água de refrigeração tem como consequência a",
        "alternatives": [
            "diminuição do pH.",
            "liberação de gases poluentes.",
            "contaminação por combustíveis.",
            "liberação de elementos radioativos.",
            "diminuição da solubilidade do gás oxigênio."
        ],
        "label": "E",
        "has_image": True,
        "image_description": "Diagrama de usina termonuclear mostrando circuito primário, secundário e sistema de água de refrigeração."
    },
    {
        "numero": 108,
        "question": "Em 1909, as representações das substâncias ácido nítrico e cloreto de cálcio, tendo por base essas informações e seguindo a mesma lógica, seriam, respectivamente:",
        "alternatives": [
            "HAzO³ e CaCl²",
            "HAz³O e Ca²Cl",
            "H³AzO⁴ e CaCl",
            "HAz³O e KCl²",
            "HAzO² e KCl"
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Fotografia de 1909 mostrando quadro de química com fórmulas antigas usando 'Az' para nitrogênio."
    },
    {
        "numero": 109,
        "question": "O LCC técnico é produzido por meio de uma reação orgânica do tipo",
        "alternatives": [
            "hidrólise.",
            "fenilação.",
            "esterificação.",
            "hidrogenação.",
            "descarboxilação."
        ],
        "label": "E"
    },
    {
        "numero": 110,
        "question": "A massa de cobalto-60, em miligrama, que restará ao final desse tempo é mais próxima de",
        "alternatives": [
            "2,00 mg.",
            "1,00 mg.",
            "0,40 mg.",
            "0,13 mg.",
            "0,06 mg."
        ],
        "label": "E"
    },
    {
        "numero": 111,
        "question": "Dar destino sustentável às sobras, conforme apresentado na etapa 4, ajuda a evitar a",
        "alternatives": [
            "bioacumulação de toxinas em plantas.",
            "eutrofização dos corpos de água.",
            "destruição da camada de ozônio.",
            "ocorrência de inversão térmica.",
            "produção de chuva ácida."
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Diagrama do processo de biodigestão mostrando etapas: excrementos animais, decomposição, produção de metano e uso de sobras como fertilizante."
    },
    {
        "numero": 112,
        "question": "Esse alimento contribui para diminuir a carência associada a qual doença?",
        "alternatives": [
            "Hemofilia.",
            "Escorbuto.",
            "Raquitismo.",
            "Cegueira noturna.",
            "Anemia perniciosa."
        ],
        "label": "D"
    },
    {
        "numero": 113,
        "question": "A configuração adequada do circuito e o valor do resistor de proteção, em relação ao valor da resistência do equipamento, são:",
        "alternatives": [
            "Circuito em paralelo, R_p = 0,2 R_c",
            "Circuito em paralelo, R_p = 1,2 R_c",
            "Circuito em série, R_p = 1,2 R_c",
            "Circuito em série, R_p = 2,2 R_c",
            "Circuito em série, R_p = 0,2 R_c"
        ],
        "label": "E",
        "has_image": True,
        "image_description": "Diagrama de circuito elétrico mostrando fonte de tensão, resistor de proteção em série e equipamento."
    },
    {
        "numero": 114,
        "question": "A massa de alumínio, em quilograma, estimada pela engenheira é mais próxima de",
        "alternatives": [
            "2,7 kg.",
            "3,0 kg.",
            "4,1 kg.",
            "4,5 kg.",
            "5,0 kg."
        ],
        "label": "D"
    },
    {
        "numero": 115,
        "question": "O valor médio estimado para o ruído produzido por essas pessoas, na posição central desse estádio hipotético, foi de",
        "alternatives": [
            "60 dB.",
            "104 dB.",
            "140 dB.",
            "400 dB.",
            "800 dB."
        ],
        "label": "C"
    },
    {
        "numero": 116,
        "question": "Na utilização desse dispositivo, a retenção do óleo ocorre",
        "alternatives": [
            "no surfactante.",
            "na camada superior de polímero.",
            "nas nanopartículas de sílica.",
            "na camada inferior de polímero.",
            "na malha de aço."
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Diagrama esquemático do dispositivo de filtragem mostrando camadas: surfactante, polímero superior, nanopartículas de sílica, polímero inferior e malha de aço."
    },
    {
        "numero": 117,
        "question": "Do ponto de vista das interações químicas, qual desses hormônios apresenta maior solubilidade em ambientes aquáticos?",
        "alternatives": [
            "Estradiol.",
            "Estriol.",
            "Estrona.",
            "Novestrol.",
            "Noretindrona."
        ],
        "label": "B"
    },
    {
        "numero": 118,
        "question": "Nesse sistema, o menor tempo de resposta, em milissegundo, que garante a detecção de um possível invasor é mais próximo de",
        "alternatives": [
            "30 ms",
            "70 ms",
            "300 ms",
            "400 ms",
            "700 ms"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Diagrama de sistema de alarme mostrando transmissor, receptor e diferentes velocidades de movimento de invasores."
    },
    {
        "numero": 119,
        "question": "Dentre as opções apresentadas, o tratamento correto para minimizar esse problema é usar",
        "alternatives": [
            "água",
            "vinagre",
            "óleo de soja",
            "sal de cozinha",
            "bicarbonato de sódio"
        ],
        "label": "B"
    },
    {
        "numero": 120,
        "question": "O uso do campo magnético variável tem a finalidade de",
        "alternatives": [
            "imantar o material da panela por indução",
            "movimentar os átomos de ferro concentrados no fundo da panela",
            "emitir radiação eletromagnética, aquecendo a panela através do vidro cerâmico",
            "induzir corrente elétrica na parte inferior da panela, aquecendo-a por efeito Joule",
            "gerar um fluxo de corrente de convecção no ar contido entre a região da bobina e o vidro cerâmico"
        ],
        "label": "D",
        "has_image": True,
        "image_description": "Diagrama de fogão de indução mostrando bobina, campo magnético variável e panela sendo aquecida por efeito Joule."
    },
    {
        "numero": 121,
        "question": "Na fotossíntese oxigênica, qual composto desempenha função análoga à do H₂S?",
        "alternatives": [
            "ATP",
            "NADPH",
            "Oxigênio",
            "Clorofila",
            "Água"
        ],
        "label": "E"
    },
    {
        "numero": 122,
        "question": "A seleção adaptativa nesses ambientes favorece a ocorrência de espécies",
        "alternatives": [
            "exóticas.",
            "migratórias.",
            "endêmicas.",
            "dominantes.",
            "generalistas."
        ],
        "label": "C"
    },
    {
        "numero": 123,
        "question": "Após o sistema atingir o equilíbrio químico, como a formação do TiCl₄ pode ser favorecida?",
        "alternatives": [
            "Aumentando a pressão total do sistema.",
            "Diminuindo a temperatura do sistema.",
            "Aumentando a pressão parcial de O₂.",
            "Aumentando a pressão parcial de Cl₂.",
            "Variando a quantidade de TiO₂."
        ],
        "label": "D"
    },
    {
        "numero": 124,
        "question": "A altura máxima, em metro, de empilhamento do produto que essa laje é capaz de suportar é",
        "alternatives": [
            "0,16 m.",
            "0,50 m.",
            "0,80 m.",
            "1,60 m.",
            "8,00 m."
        ],
        "label": "C"
    },
    {
        "numero": 125,
        "question": "O diagrama que representa o circuito construído pelo eletrotécnico é:",
        "alternatives": [
            "Diagrama A: 136 V, 3.2 Ω",
            "Diagrama B: 120 V, 2.4 Ω",
            "Diagrama C: 120 V, 5.3 Ω",
            "Diagrama D: 102 V, 2.4 Ω",
            "Diagrama E: 102 V, 5.3 Ω"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Diagrama de circuito elétrico mostrando painéis fotovoltaicos conectados em série, gerando 120 V e 2.4 Ω."
    },
    {
        "numero": 126,
        "question": "Os potenciais padrão de diferença para as reações que representam, respectivamente, o escurecimento e a limpeza do objeto de prata são",
        "alternatives": [
            "+0,54 V e +2,37 V.",
            "+1,92 V e +0,99 V.",
            "-0,15 V e +5,43 V.",
            "+2,61 V e +1,29 V.",
            "+0,15 V e -1,29 V."
        ],
        "label": "A"
    },
    {
        "numero": 127,
        "question": "A massa aproximada, em grama, de bicarbonato de amônio que o chef deve utilizar é",
        "alternatives": [
            "2,3 g.",
            "3,5 g.",
            "5,9 g.",
            "6,8 g.",
            "8,9 g."
        ],
        "label": "C"
    },
    {
        "numero": 128,
        "question": "As componentes do vetor velocidade v que o piloto deve estabelecer em relação ao ar para que o avião alcance a posição esperada no tempo dado, considerando o vento, são",
        "alternatives": [
            "230 km/h para Leste, 180 km/h para Sul e 9 km/h para baixo.",
            "230 km/h para Leste, 180 km/h para Norte e 9 km/h para cima.",
            "200 km/h para Oeste, 200 km/h para Norte e 10 km/h para cima.",
            "170 km/h para Leste, 220 km/h para Norte e 11 km/h para cima.",
            "170 km/h para Leste, 180 km/h para Norte e 11 km/h para cima."
        ],
        "label": "D",
        "has_image": True,
        "image_description": "Diagrama 3D mostrando sistema de coordenadas com avião, posição alvo e componentes de velocidade."
    },
    {
        "numero": 129,
        "question": "O gráfico que representa essa situação descrita é:",
        "alternatives": [
            "Gráfico A: linha contínua com maior energia de ativação, linha pontilhada com menor energia de ativação",
            "Gráfico B: linha contínua com maior energia de ativação, linha pontilhada com menor energia de ativação",
            "Gráfico C: linha contínua com maior energia de ativação, linha pontilhada com menor energia de ativação",
            "Gráfico D: linha contínua com maior energia de ativação, linha pontilhada com menor energia de ativação",
            "Gráfico E: linha contínua com maior energia de ativação, linha pontilhada com menor energia de ativação"
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Gráfico de energia mostrando reação sem enzima (linha contínua, maior energia de ativação) e com enzima (linha pontilhada, menor energia de ativação)."
    },
    {
        "numero": 130,
        "question": "Os sensores com maior sensibilidade são",
        "alternatives": [
            "1 e 2.",
            "1 e 3.",
            "2 e 3.",
            "2 e 4.",
            "2 e 5."
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Gráfico de resistência vs temperatura mostrando cinco sensores, sendo os sensores 2 e 3 com maior inclinação (maior sensibilidade)."
    },
    {
        "numero": 131,
        "question": "Para qual doença o ácido úsnico é mais indicado para controle?",
        "alternatives": [
            "esquistossomose.",
            "febre amarela.",
            "coqueluche.",
            "tuberculose.",
            "dengue."
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Tabela mostrando testes do ácido úsnico contra diferentes organismos, com alta eficiência contra vermes platelmintos (esquistossomose)."
    },
    {
        "numero": 132,
        "question": "Qual característica do carvão ativado explica a sua maior eficiência nesse processo?",
        "alternatives": [
            "Massa",
            "Dureza",
            "Densidade",
            "Superfície",
            "Condutividade"
        ],
        "label": "D",
        "has_image": True,
        "image_description": "Diagrama comparando carvão comum e carvão ativado, mostrando maior porosidade e área superficial no carvão ativado."
    },
    {
        "numero": 133,
        "question": "Estarão presentes no organismo geneticamente modificado os genes do",
        "alternatives": [
            "metabolismo de E. coli, apenas.",
            "ciclo circadiano de E. coli, apenas.",
            "metabolismo de S. elongatus e do ciclo circadiano de E. coli.",
            "ciclo circadiano de S. elongatus e do metabolismo de E. coli.",
            "ciclo circadiano de S. elongatus e do ciclo circadiano de E. coli."
        ],
        "label": "D"
    },
    {
        "numero": 134,
        "question": "O aumento na taxa de mortalidade dessas aves estava associado a uma redução na",
        "alternatives": [
            "dilatação do papo.",
            "reposição de penas das asas.",
            "secreção da glândula uropigial.",
            "formação da membrana natatória.",
            "largura das cavidades de ossos pneumáticos."
        ],
        "label": "C"
    },
    {
        "numero": 135,
        "question": "Considerando a ordem das tentativas, quantas atividades a estudante conseguiu realizar sem queimar o fusível?",
        "alternatives": [
            "4",
            "3",
            "2",
            "1",
            "0"
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Imagem de régua de tomadas e tabela com potências de aparelhos elétricos."
    },
]

# =============================================================================
# QUESTÕES EXTRAÍDAS DAS IMAGENS - Matemática (136-180)
# =============================================================================

QUESTOES_MATEMATICA_IMAGENS = [
    {
        "numero": 136,
        "question": "Nessas condições, a quantidade mínima necessária de policiais a serem alocados ao longo dessa ciclovia para torná-la protegida é",
        "alternatives": [
            "4.",
            "8.",
            "15.",
            "30.",
            "60."
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Diagrama de ciclovia circular com raio de 1 km, mostrando região protegida de 200 m ao redor de um ponto P."
    },
    {
        "numero": 137,
        "question": "Qual é a quantidade de S₁, em litro, que será retirada?",
        "alternatives": [
            "0,0050",
            "0,0100",
            "0,5000",
            "4,9775",
            "5,0000"
        ],
        "label": "C"
    },
    {
        "numero": 138,
        "question": "Utilizando o mesmo caminhão da entrega anterior, qual é o volume mínimo de gasolina, em litro, que a distribuidora deverá enviar para garantir a entrega da quantidade encomendada nesse novo pedido?",
        "alternatives": [
            "20 100",
            "20 200",
            "20 300",
            "20 400",
            "20 600"
        ],
        "label": "C"
    },
    {
        "numero": 139,
        "question": "A velocidade de referência, em megabyte por segundo, a ser adotada por essa empresa é",
        "alternatives": [
            "360.",
            "370.",
            "380.",
            "390.",
            "400."
        ],
        "label": "B"
    },
    {
        "numero": 140,
        "question": "Qual desses produtos deve ser o escolhido pela estudante?",
        "alternatives": [
            "Batata chips.",
            "Palitos salgados.",
            "Biscoito multigrãos.",
            "Biscoito de polvilho.",
            "Biscoito de água e sal."
        ],
        "label": "E"
    },
    {
        "numero": 141,
        "question": "Qual é a quantidade de cores utilizadas para pintar o protótipo?",
        "alternatives": [
            "9",
            "8",
            "6",
            "4",
            "3"
        ],
        "label": "B"
    },
    {
        "numero": 142,
        "question": "A partir do instante t₁, em que se inicia a prática meditativa, o comportamento da frequência respiratória, em relação ao tempo,",
        "alternatives": [
            "mantém-se constante.",
            "é diretamente proporcional ao tempo.",
            "é inversamente proporcional ao tempo.",
            "diminui até o instante t₂, a partir do qual se torna constante.",
            "diminui de forma proporcional ao tempo, tanto entre t₁ e t₂ quanto após t₂."
        ],
        "label": "D",
        "has_image": True,
        "image_description": "Gráfico mostrando frequência respiratória diminuindo de f₁ para f₂ entre t₁ e t₂, depois constante."
    },
    {
        "numero": 143,
        "question": "Qual é a diferença, em segundo, entre a marca de referência e a marca estabelecida por Usain Bolt em 2009?",
        "alternatives": [
            "0,02",
            "0,42",
            "0,52",
            "1,02",
            "1,42"
        ],
        "label": "B"
    },
    {
        "numero": 144,
        "question": "A figura que apresenta as projeções ortogonais desse cubo nos três planos coordenados após esses movimentos é",
        "alternatives": [
            "Figura A: projeções na posição inicial",
            "Figura B: projeções em x=-2, y=6, z=-3",
            "Figura C: projeções com z positivo",
            "Figura D: projeções com x positivo",
            "Figura E: projeções com y negativo"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Sistema de coordenadas 3D mostrando cubo e suas projeções ortogonais nos planos xy, yz e xz após movimentos."
    },
    {
        "numero": 145,
        "question": "Segundo os dados do infográfico, ao se escolher aleatoriamente um internauta brasileiro no período ao qual se refere a reportagem, a probabilidade de ele ser um homem que acessa alguma rede social é",
        "alternatives": [
            "30/90",
            "36/100",
            "40/100",
            "40/90",
            "46/90"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Infográfico mostrando que 90% dos internautas brasileiros acessam redes sociais, sendo 60% mulheres e 40% homens."
    },
    {
        "numero": 146,
        "question": "Nessas condições, qual será a capacidade, em metro cúbico, do cilindro escolhido por essa pessoa?",
        "alternatives": [
            "10",
            "14",
            "17",
            "21",
            "25"
        ],
        "label": "C"
    },
    {
        "numero": 147,
        "question": "Qual é a equação da trajetória em que o herói poderá se movimentar sem ser atacado?",
        "alternatives": [
            "y = -3x + 20",
            "y = -3x + 16",
            "y = -3x - 20",
            "y = 3x + 16",
            "y = 3x - 16"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Plano cartesiano mostrando quadrilátero STUV com pontos S(6,2), T, U, V(8,6) e trajetória equidistante dos vilões."
    },
    {
        "numero": 148,
        "question": "O gênero de livro do qual o gerente deverá encomendar mais exemplares é",
        "alternatives": [
            "ficção, pois é o que apresenta maior demanda.",
            "biografia, pois é o gênero que tem a menor demanda.",
            "autoajuda, pois a quantidade em estoque é inferior à demanda.",
            "biografia, pois é o gênero que tem a menor quantidade de livros em estoque.",
            "romance, pois é o que apresenta o menor estoque de livros de autores brasileiros."
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Gráfico de barras e linha mostrando estoque e demanda por gênero de livro: Ficção, Autoajuda, Romance, Biografia."
    },
    {
        "numero": 149,
        "question": "Segundo essa estimativa, o número de matrículas no curso de francês para o ano de 2025 será",
        "alternatives": [
            "2.",
            "12.",
            "20.",
            "22.",
            "40."
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Gráfico de pizza (2023) e gráfico de barras (2024) mostrando distribuição de matrículas por idioma: Inglês, Espanhol, Francês, Alemão."
    },
    {
        "numero": 150,
        "question": "A opção que indica o deslocamento de maior comprimento realizado pelo carrinho de brinquedo é",
        "alternatives": [
            "I.",
            "II.",
            "III.",
            "IV.",
            "V."
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Cinco diagramas mostrando deslocamentos com escalas diferentes: I (1:100, 9cm), II (1:300, 5cm), III (1:600, 5cm), IV (1:700, 3cm), V (1:1000, 2cm)."
    },
    {
        "numero": 151,
        "question": "Quantos vértices tem esse poliedro?",
        "alternatives": [
            "21",
            "25",
            "55",
            "80",
            "110"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Imagens 3D e planificação da cúpula pentagonal giralongada (sólido de Johnson) mostrando faces regulares."
    },
    {
        "numero": 152,
        "question": "O número de tijolos fabricados diariamente após o aumento da capacidade de produção é",
        "alternatives": [
            "800.",
            "1080.",
            "1200.",
            "1800.",
            "2520."
        ],
        "label": "D"
    },
    {
        "numero": 153,
        "question": "O código de identificação desse visitante é",
        "alternatives": [
            "0109082.",
            "0281090.",
            "1010982.",
            "2081090.",
            "2810910."
        ],
        "label": "D"
    },
    {
        "numero": 154,
        "question": "A probabilidade de que todos os candidatos tenham recebido de volta os envelopes com os seus respectivos celulares é",
        "alternatives": [
            "1/2",
            "1/10",
            "1/16",
            "1/24",
            "1/256"
        ],
        "label": "D"
    },
    {
        "numero": 155,
        "question": "Qual é a quantidade de estudantes no ensino médio dessa escola?",
        "alternatives": [
            "720",
            "360",
            "320",
            "288",
            "240"
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Gráfico de barras por série e gráfico de pizza por modalidade esportiva, com Basquete = 80 estudantes."
    },
    {
        "numero": 156,
        "question": "A direção e o tempo aproximado de navegação que o dono da embarcação deve utilizar são, respectivamente,",
        "alternatives": [
            "135 e 7 horas e 15 minutos.",
            "45 e 7 horas e 15 minutos.",
            "135 e 12 horas.",
            "135 e 6 horas.",
            "45 e 6 horas."
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Rosa dos ventos e diagrama mostrando rotas planejada (P-Q-R) e executada (P-S-T) com direções e tempos."
    },
    {
        "numero": 157,
        "question": "O grupo escolhido foi o",
        "alternatives": [
            "1.",
            "2.",
            "3.",
            "4.",
            "5."
        ],
        "label": "E",
        "has_image": True,
        "image_description": "Tabela com dados estatísticos de grupos de mulheres: menor idade, maior idade, média, mediana, moda, desvio padrão."
    },
    {
        "numero": 158,
        "question": "Para que consiga repetir nessa corrida seu melhor pace em corridas de 5 km, seu tempo, no 5º trecho, deve ser quantos segundos menor do que o que ele gastou para percorrer o 4º trecho?",
        "alternatives": [
            "1",
            "2",
            "8",
            "9",
            "15"
        ],
        "label": "C",
        "has_image": True,
        "image_description": "Diagrama de corrida de 5 km mostrando tempos acumulados e por trecho, com melhor pace de 281 s/km."
    },
    {
        "numero": 159,
        "question": "A expressão algébrica que representa a função D(T) é",
        "alternatives": [
            "D = 2.5 + tg[30(T - (5 - 2π)/2)]",
            "D = 4 + tg[30(T + 5/2)]",
            "D = 4 + tg[2.5(T + (5 + 2π)/2)]",
            "D = 30 + tg[1/2(T - 5)]",
            "D = 30 + tg[1/2(T - 5/2)]"
        ],
        "label": "E",
        "has_image": True,
        "image_description": "Gráfico mostrando função D(T) com assíntotas verticais e ponto (2.5, 30)."
    },
    {
        "numero": 160,
        "question": "O quarteirão onde se encontra a casa de João é representado pelo quadrado com a letra",
        "alternatives": [
            "P",
            "Q",
            "R",
            "S",
            "T"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Grade 5x5 representando quarteirões com letras P, Q, R, S, T e casa do amigo marcada com 'A'."
    },
    {
        "numero": 161,
        "question": "Para que no mês seguinte a empresa atinja a meta, a quantidade mínima de toneladas de plástico que devem ser produzidas a partir de reciclagem deverá ser",
        "alternatives": [
            "135",
            "140",
            "155",
            "160",
            "175"
        ],
        "label": "D"
    },
    {
        "numero": 162,
        "question": "O número de diretorias distintas que podem ser formadas por esses 10 casais é",
        "alternatives": [
            "10 x 9 x 8",
            "20 x 18 x 16",
            "20 x 19 x 18",
            "10 x 9 x 8 x 2",
            "20 x 18 x 16 x 2"
        ],
        "label": "B"
    },
    {
        "numero": 163,
        "question": "Qual é a escala em que esse desenho representa a obra?",
        "alternatives": [
            "1:1,5",
            "1:2,25",
            "1:10",
            "1:100",
            "1:150"
        ],
        "label": "E",
        "has_image": True,
        "image_description": "Desenho de sol com raios, dimensões de 20 cm, amplificado por 30 m na obra real."
    },
    {
        "numero": 164,
        "question": "A relação obtida entre T e F nesse estudo foi",
        "alternatives": [
            "T = 1,59 + F",
            "F = 1,59 + T",
            "T/F = 1,59",
            "F/T = 1,59",
            "F * T = 1,59"
        ],
        "label": "C"
    },
    {
        "numero": 165,
        "question": "O valor da mensalidade reajustada, em real, é",
        "alternatives": [
            "185,60.",
            "226,09.",
            "245,20.",
            "268,93.",
            "285,60."
        ],
        "label": "D"
    },
    {
        "numero": 166,
        "question": "O número de copos que ele consegue servir com um recipiente completamente cheio de sorvete é",
        "alternatives": [
            "5.",
            "8.",
            "50.",
            "80.",
            "800."
        ],
        "label": "D"
    },
    {
        "numero": 167,
        "question": "O gráfico de linhas que representa a produção de soja dessa propriedade, em tonelada, nessas cinco safras é",
        "alternatives": [
            "Gráfico A: 400, 330, 562.5, 562.5, 500",
            "Gráfico B: 40, 30, 45, 45, 50 (produtividade)",
            "Gráfico C: 200, 220, 250, 250, 200 (área)",
            "Gráfico D: valores não correspondentes",
            "Gráfico E: valores não correspondentes"
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Tabela com área cultivada e produtividade por safra, e gráfico de linhas mostrando produção total em toneladas."
    },
    {
        "numero": 168,
        "question": "Qual é o volume de ouro, em centímetro cúbico, necessário para a confecção dessas medalhas?",
        "alternatives": [
            "288",
            "297",
            "567",
            "990",
            "1134"
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Diagrama de medalha cilíndrica com diâmetro 6 cm, altura 3 mm, com prisma quadrado interno (base ABCD)."
    },
    {
        "numero": 169,
        "question": "O jogador que tem a maior probabilidade de vitória é",
        "alternatives": [
            "Artur, com probabilidade de 2/3",
            "João, com probabilidade de 4/9",
            "Artur, com probabilidade de 91/216",
            "João, com probabilidade de 91/216",
            "Artur, com probabilidade de 125/216"
        ],
        "label": "E"
    },
    {
        "numero": 170,
        "question": "A unidade de medida da luminância de um objeto é",
        "alternatives": [
            "cd/m²",
            "m²/cd",
            "cd/m",
            "m/cd",
            "m/cd²"
        ],
        "label": "A"
    },
    {
        "numero": 171,
        "question": "Ao final da rodada n, qual é a expressão algébrica que representa o número de moedas do jogador na posição 1?",
        "alternatives": [
            "103 + 4n",
            "103 + 3n",
            "100 + 4n",
            "100 + 3n",
            "99 + 4n"
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Diagrama circular mostrando quatro posições com transferências de moedas: posição 1 → 2 (1 moeda), 2 → 3 (2 moedas), 3 → 4 (3 moedas), 4 → 1 (4 moedas)."
    },
    {
        "numero": 172,
        "question": "Qual foi a diferença, em real, entre os gastos totais com gasolina e com GNV?",
        "alternatives": [
            "4",
            "8",
            "14",
            "21",
            "30"
        ],
        "label": "B",
        "has_image": True,
        "image_description": "Dois gráficos mostrando rendimento (km/m³ para GNV e km/L para gasolina) em função da velocidade, ambos a 60 km/h."
    },
    {
        "numero": 173,
        "question": "A autoescola que será contratada é a",
        "alternatives": [
            "I, com o custo total de R$ 1 400,00.",
            "II, com o custo total de R$ 280,00.",
            "II, com o custo total de R$ 1 300,00.",
            "III, com o custo total de R$ 460,00.",
            "III, com o custo total de R$ 1 200,00."
        ],
        "label": "C"
    },
    {
        "numero": 174,
        "question": "A quantidade máxima de garrafas que serão colocadas nessa caixa, garantindo um funcionamento eficiente, é igual a",
        "alternatives": [
            "10.",
            "8.",
            "4.",
            "3.",
            "2."
        ],
        "label": "E",
        "has_image": True,
        "image_description": "Diagrama de caixa de descarga com dimensões 2,5 dm x 1,5 dm x 2 dm, mostrando boia e volume mínimo de 5 L."
    },
    {
        "numero": 175,
        "question": "A aresta da base das novas caixas deve ser, no mínimo, quantos centímetros maior do que a das caixas originais?",
        "alternatives": [
            "4",
            "12",
            "16",
            "18",
            "20"
        ],
        "label": "A"
    },
    {
        "numero": 176,
        "question": "O maior valor a ser escolhido para K é",
        "alternatives": [
            "10^0.5",
            "10^8",
            "10^2.5 / 84",
            "10^2.5 / 99",
            "25 x 10^-2"
        ],
        "label": "D"
    },
    {
        "numero": 177,
        "question": "O projeto a ser aprovado é o",
        "alternatives": [
            "Projeto 1, com área de seção transversal de 67,5 m².",
            "Projeto 2, com área de seção transversal de 121,5 m².",
            "Projeto 1, com área de seção transversal de 135 m².",
            "Projeto 2, com área de seção transversal de 243 m².",
            "Qualquer um dos dois, pois possuem áreas de seção transversal iguais."
        ],
        "label": "A",
        "has_image": True,
        "image_description": "Dois projetos de túneis: Projeto 1 com dois túneis semicirculares (12m e 6m) e Projeto 2 com um túnel misto (18m)."
    },
    {
        "numero": 178,
        "question": "A quantidade n de parcelas da opção 1 é",
        "alternatives": [
            "18",
            "24",
            "30",
            "42",
            "48"
        ],
        "label": "B"
    },
    {
        "numero": 179,
        "question": "O número de formas distintas de distribuir os presentes é",
        "alternatives": [
            "36",
            "53",
            "300",
            "360",
            "560"
        ],
        "label": "D"
    },
    {
        "numero": 180,
        "question": "A distância total percorrida por esse jogador durante sua participação na partida, em quilômetro, é",
        "alternatives": [
            "4,5",
            "6,0",
            "7,5",
            "9,0",
            "12,0"
        ],
        "label": "C"
    },
]

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

def processar_questao_json(questao_raw: Dict, numero: int, area: str) -> Optional[Dict]:
    """Processa uma questão do formato JSON bruto para o formato padrão."""
    
    # Extrair question e alternatives
    question_raw = questao_raw.get('question', '').strip()
    alternatives_raw = questao_raw.get('alternatives', [])
    texts_of_support = questao_raw.get('texts_of_support', [])
    
    # Processar contexto (texts_of_support)
    contexto = ' '.join([limpar_texto(t) for t in texts_of_support if t and limpar_texto(t)])
    
    # Processar pergunta
    pergunta = limpar_texto(question_raw)
    
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
        alt_str = re.sub(r'CIÊNCIAS.*$', '', alt_str, flags=re.IGNORECASE)
        alt_str = re.sub(r'MATEMÁTICA.*$', '', alt_str, flags=re.IGNORECASE)
        alt_str = re.sub(r'CADERNO.*$', '', alt_str, flags=re.IGNORECASE)
        alt_str = limpar_texto(alt_str)
        if alt_str and len(alt_str) > 2:  # Alternativa deve ter pelo menos 3 caracteres
            alternativas_limpas.append(alt_str)
    
    # Limpar pergunta também
    pergunta = re.sub(r'ENEM2025.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = re.sub(r'CIÊNCIAS.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = re.sub(r'MATEMÁTICA.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = re.sub(r'CADERNO.*$', '', pergunta, flags=re.IGNORECASE)
    pergunta = limpar_texto(pergunta)
    
    # Se não temos pergunta nem contexto, criar placeholder
    if not pergunta and not contexto:
        pergunta = f"[QUESTÃO {numero} - DADOS NÃO DISPONÍVEIS NO JSON ORIGINAL]"
        contexto = ""
    
    # Se não temos alternativas válidas, criar placeholders
    if len(alternativas_limpas) < 2:
        if pergunta or contexto:
            alternativas_limpas = [''] * 5
        else:
            return None
    
    # Garantir 5 alternativas
    while len(alternativas_limpas) < 5:
        alternativas_limpas.append('')
    alternativas_limpas = alternativas_limpas[:5]
    
    # Obter label
    if area == 'natural-sciences':
        label = LABELS_NATUREZA_2025.get(numero, 'ANULADO').upper()
    else:
        label = LABELS_MATEMATICA_2025.get(numero, 'ANULADO').upper()
    
    # Marcar questões incompletas
    is_incomplete = '[DADOS NÃO DISPONÍVEIS' in pergunta or len([a for a in alternativas_limpas if a]) < 2
    
    # Criar questão normalizada
    questao_normalizada = {
        'id': f'enem_2025_{area}_{numero}',
        'exam': '2025',
        'area': area,
        'number': str(numero),
        'context': contexto,
        'question': pergunta,
        'alternatives': alternativas_limpas,
        'label': label,
        'has_images': False,
        'incomplete': is_incomplete
    }
    
    return questao_normalizada

def processar_questao_imagem(questao: Dict, numero: int, area: str) -> Dict:
    """Processa uma questão extraída das imagens para o formato padrão."""
    
    questao_norm = {
        'id': f'enem_2025_{area}_{numero}',
        'exam': '2025',
        'area': area,
        'number': str(numero),
        'context': questao.get('context', ''),
        'question': questao.get('question', '').strip(),
        'alternatives': questao.get('alternatives', [])[:5],
        'label': questao.get('label', 'ANULADO').upper(),
        'has_images': questao.get('has_image', False),
        'incomplete': False
    }
    
    # Adicionar descrição de imagem se houver
    if questao.get('image_description'):
        questao_norm['image_description'] = questao.get('image_description')
    
    # Garantir 5 alternativas
    while len(questao_norm['alternatives']) < 5:
        questao_norm['alternatives'].append('')
    
    return questao_norm

def carregar_questoes_json(arquivo_json: Path, area: str, inicio: int, fim: int) -> List[Dict]:
    """Carrega e processa questões do arquivo JSON."""
    print(f"📥 Carregando arquivo: {arquivo_json}")
    
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(f"✅ Arquivo carregado! Total de itens: {len(dados)}")
    
    # Filtrar questões do range especificado
    questoes = []
    for item in dados:
        id_str = item.get('id', '')
        numero = extrair_numero_questao(id_str)
        
        if numero and inicio <= numero <= fim:
            questao_processada = processar_questao_json(item, numero, area)
            if questao_processada:
                questoes.append(questao_processada)
    
    # Ordenar por número
    questoes.sort(key=lambda x: int(x['number']))
    
    print(f"✅ {len(questoes)} questões de {area} processadas ({inicio}-{fim})")
    
    return questoes

def main():
    """Função principal."""
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "enem"
    
    # Arquivo de entrada
    arquivo_entrada = data_dir / "enem_2025_natureza_matematica.json"
    
    if not arquivo_entrada.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        print("   Execute primeiro a extração das questões de Natureza e Matemática")
        sys.exit(1)
    
    todas_questoes = []
    
    # ========================================================================
    # PROCESSAR NATUREZA (91-135)
    # ========================================================================
    print("\n" + "=" * 70)
    print("📋 PROCESSANDO CIÊNCIAS DA NATUREZA (91-135)")
    print("=" * 70)
    
    # Carregar do JSON
    questoes_natureza_json = carregar_questoes_json(arquivo_entrada, 'natural-sciences', 91, 135)
    
    # Processar questões das imagens (prioridade sobre JSON se disponível)
    questoes_natureza_imagens = []
    for q_img in QUESTOES_NATUREZA_IMAGENS:
        questao_norm = processar_questao_imagem(q_img, q_img['numero'], 'natural-sciences')
        questoes_natureza_imagens.append(questao_norm)
    
    # Combinar: usar questões das imagens quando disponíveis, senão usar do JSON
    questoes_natureza_final = {}
    for q in questoes_natureza_json:
        num = int(q['number'])
        questoes_natureza_final[num] = q
    
    for q in questoes_natureza_imagens:
        num = int(q['number'])
        questoes_natureza_final[num] = q  # Imagens têm prioridade
    
    questoes_natureza = sorted(questoes_natureza_final.values(), key=lambda x: int(x['number']))
    todas_questoes.extend(questoes_natureza)
    
    print(f"✅ Total de Natureza: {len(questoes_natureza)} questões")
    
    # ========================================================================
    # PROCESSAR MATEMÁTICA (136-180)
    # ========================================================================
    print("\n" + "=" * 70)
    print("📋 PROCESSANDO MATEMÁTICA (136-180)")
    print("=" * 70)
    
    # Carregar do JSON
    questoes_matematica_json = carregar_questoes_json(arquivo_entrada, 'mathematics', 136, 180)
    
    # Processar questões das imagens (prioridade sobre JSON se disponível)
    questoes_matematica_imagens = []
    for q_img in QUESTOES_MATEMATICA_IMAGENS:
        questao_norm = processar_questao_imagem(q_img, q_img['numero'], 'mathematics')
        questoes_matematica_imagens.append(questao_norm)
    
    # Combinar: usar questões das imagens quando disponíveis, senão usar do JSON
    questoes_matematica_final = {}
    for q in questoes_matematica_json:
        num = int(q['number'])
        questoes_matematica_final[num] = q
    
    for q in questoes_matematica_imagens:
        num = int(q['number'])
        questoes_matematica_final[num] = q  # Imagens têm prioridade
    
    questoes_matematica = sorted(questoes_matematica_final.values(), key=lambda x: int(x['number']))
    todas_questoes.extend(questoes_matematica)
    
    print(f"✅ Total de Matemática: {len(questoes_matematica)} questões")
    
    # ========================================================================
    # SALVAR RESULTADOS
    # ========================================================================
    print("\n" + "=" * 70)
    print("💾 SALVANDO RESULTADOS")
    print("=" * 70)
    
    # Salvar Natureza
    arquivo_natureza = data_dir / "enem_2025_natureza_imagens.jsonl"
    with open(arquivo_natureza, 'w', encoding='utf-8') as f:
        for q in questoes_natureza:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f"✅ {len(questoes_natureza)} questões de Natureza salvas em {arquivo_natureza.name}")
    
    # Salvar Matemática
    arquivo_matematica = data_dir / "enem_2025_matematica_imagens.jsonl"
    with open(arquivo_matematica, 'w', encoding='utf-8') as f:
        for q in questoes_matematica:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f"✅ {len(questoes_matematica)} questões de Matemática salvas em {arquivo_matematica.name}")
    
    # Salvar arquivo consolidado
    arquivo_completo = data_dir / "enem_2025_natureza_matematica_imagens.jsonl"
    with open(arquivo_completo, 'w', encoding='utf-8') as f:
        for q in todas_questoes:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    print(f"✅ {len(todas_questoes)} questões totais salvas em {arquivo_completo.name}")
    
    # ========================================================================
    # ESTATÍSTICAS
    # ========================================================================
    print("\n" + "=" * 70)
    print("📊 ESTATÍSTICAS")
    print("=" * 70)
    
    # Estatísticas por área
    for area_nome, questoes_area in [('Natureza', questoes_natureza), ('Matemática', questoes_matematica)]:
        print(f"\n{area_nome}:")
        print(f"  Total: {len(questoes_area)} questões")
        questoes_com_label = sum(1 for q in questoes_area if q['label'] != 'ANULADO')
        print(f"  Com label: {questoes_com_label}/{len(questoes_area)}")
        questoes_com_imagem = sum(1 for q in questoes_area if q.get('has_images', False))
        print(f"  Com imagens: {questoes_com_imagem}/{len(questoes_area)}")
        questoes_incompletas = sum(1 for q in questoes_area if q.get('incomplete', False))
        if questoes_incompletas > 0:
            print(f"  ⚠️  Incompletas: {questoes_incompletas}")
    
    # Verificar cobertura
    print("\n" + "=" * 70)
    print("📋 COBERTURA")
    print("=" * 70)
    
    nums_natureza = sorted([int(q['number']) for q in questoes_natureza])
    nums_matematica = sorted([int(q['number']) for q in questoes_matematica])
    
    faltantes_natureza = [n for n in range(91, 136) if n not in nums_natureza]
    faltantes_matematica = [n for n in range(136, 181) if n not in nums_matematica]
    
    print(f"\nNatureza (91-135):")
    print(f"  Extraídas: {len(nums_natureza)} questões")
    if nums_natureza:
        print(f"  Range: {nums_natureza[0]}-{nums_natureza[-1]}")
    if faltantes_natureza:
        print(f"  ⚠️  Faltantes: {len(faltantes_natureza)} questões ({faltantes_natureza[:10]}{'...' if len(faltantes_natureza) > 10 else ''})")
    else:
        print(f"  ✅ Completo!")
    
    print(f"\nMatemática (136-180):")
    print(f"  Extraídas: {len(nums_matematica)} questões")
    if nums_matematica:
        print(f"  Range: {nums_matematica[0]}-{nums_matematica[-1]}")
    if faltantes_matematica:
        print(f"  ⚠️  Faltantes: {len(faltantes_matematica)} questões ({faltantes_matematica[:10]}{'...' if len(faltantes_matematica) > 10 else ''})")
    else:
        print(f"  ✅ Completo!")
    
    print("\n" + "=" * 70)
    print("✅ PROCESSAMENTO CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    main()

