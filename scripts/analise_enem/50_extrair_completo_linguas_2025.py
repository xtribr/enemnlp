#!/usr/bin/env python3
"""
📸 Extração Completa de Questões ENEM 2025 - Linguagens
========================================================

Extrai TODAS as questões de Linguagens (01-45) das imagens fornecidas.

Uso:
    python 50_extrair_completo_linguas_2025.py
"""

import json
from pathlib import Path
from typing import Dict, List

# =============================================================================
# TODAS AS QUESTÕES DE LINGUAGENS (01-45) EXTRAÍDAS DAS IMAGENS
# =============================================================================

QUESTOES_LINGUAGENS_2025 = [
    # 01-05: Inglês
    {
        "numero": 1,
        "question": "Glory Ames, from the White Earth reservation, is frustrated that despite the presence of several indigenous reservations near Moorhead, local Halloween stores still feature a western section with costumes such as \"pow wow princess\". Even worse, despite a long-running debate about racism and cultural appropriation, often prompted by backlash against celebrities and politicians for donning offensive costumes, people continue to wear such costumes. Last Halloween, Ames spotted a photo on Instagram of a girl dressed as a Native American with a bullet in her forehead. She immediately reported it to the social media platform and had it removed. \"They blatantly take certain aspects of our culture, race, religion, and use it for their advantage and ignore the people living it\", said Ames. Ao abordar um aspecto da celebração do Halloween, esse texto tem por objetivo",
        "alternatives": [
            "denunciar a violência contra crianças indígenas.",
            "descrever costumes tradicionais em celebrações indígenas.",
            "valorizar as vestimentas características dos povos originários.",
            "criticar a exploração indevida de elementos da identidade indígena.",
            "sugerir ações de combate ao preconceito contra os povos originários."
        ],
        "label": "D"
    },
    {
        "numero": 2,
        "question": "My idea of philosophy is that if it is not relevant to human problems, if it does not tell us how we can go about eradicating some of the misery in this world, then it is not worth the name of philosophy. I think Socrates made a very profound statement when he asserted that philosophy is to teach us proper living. In this day and age \"proper living\" means liberation from the urgent problems of poverty, economic necessity and indoctrination, mental oppression. Nesse texto, ao discorrer sobre a relevância da filosofia, a escritora Angela Davis tem por objetivo",
        "alternatives": [
            "criticá-la pela restrição temática.",
            "vinculá-la ao universo acadêmico.",
            "afastá-la da abordagem socrática.",
            "aproximá-la dos problemas sociais.",
            "responsabilizá-la pela pobreza humana."
        ],
        "label": "D"
    },
    {
        "numero": 3,
        "question": "Remember the sky that you were born under, know each of the star's stories. Remember the moon, know who she is. Remember the sun's birth at dawn. [...] Remember your birth, how your mother struggled to give you form and breath [...] Remember the earth whose skin you are: red earth, black earth, yellow earth, white earth brown earth, we are earth. Remember the plants, trees, animal life who all have their tribes, their families, their histories, too [...] Remember you are all people and all people are you. Remember you are this universe and this universe is you. Remember all is in motion, is growing, is you. Nesse poema, de uma autora de ascendência indígena, o eu lírico ressalta a",
        "alternatives": [
            "potência dos astros celestes.",
            "origem das plantas e dos animais.",
            "importância do apego à terra natal.",
            "relação entre seres humanos e natureza.",
            "conexão entre o tempo real e o tempo imaginário."
        ],
        "label": "D"
    },
    {
        "numero": 4,
        "question": "It is true that all children are special, simply because they are children. But most adults are not special, and children end up as adults pretty quickly. Life then can be difficult and even disappointing. The shock of this may account for the emergence of the \"snowflake generation\" of university students, who are so delicate they can't handle controversial ideas being put forward in their lectures. The roots of this fragility run deep in modern culture. So, an approach of the world that states: \"Life is wonderful, you're special and, if you are a good boy/girl, life will be amazing forever\" is not a message designed to aid bouncing back from failure or confronting catastrophe. Resilience is not about feeding ego — telling your children how wonderful they are — but strengthening it. Nesse texto, a expressão \"snowflake generation\" é usada para",
        "alternatives": [
            "abordar obstáculos impostos a universitários.",
            "destacar mensagens de incentivo a estudantes.",
            "estimular ações proativas em situações de emergência.",
            "retratar relações conflituosas em ambiente universitário.",
            "apontar posturas de uma juventude avessa a contrariedades."
        ],
        "label": "E"
    },
    {
        "numero": 5,
        "question": "Nesse texto, a pergunta \"What is sleep?\", em uma das embalagens do produto, está relacionada ao(à)",
        "alternatives": [
            "escassez de horas de sono.",
            "estímulo a um descanso de qualidade.",
            "gasto com bebidas que combatem a insônia.",
            "consumo de bebidas que causam dependência.",
            "necessidade de um produto que provoque o sono."
        ],
        "label": "A",
        "has_image": True
    },
    # 06-10: Texto "De próprio punho"
    {
        "numero": 6,
        "context": "Texto 'De próprio punho'",
        "question": "No que diz respeito ao gênero bilhete, a autora dessa crônica",
        "alternatives": [
            "ressalta a formalidade na comunicação com as pessoas de sua convivência.",
            "critica a ansiedade causada pela velocidade da comunicação.",
            "expressa a obrigatoriedade de concisão nas anotações.",
            "questiona a prática da escrita de próprio punho.",
            "apresenta a diversidade de usos no cotidiano."
        ],
        "label": "E"
    },
    {
        "numero": 7,
        "context": "Texto 'De próprio punho'",
        "question": "O elemento que caracteriza esse texto como uma crônica é a",
        "alternatives": [
            "defesa das opiniões da autora sobre um tema de interesse coletivo.",
            "exposição sobre o uso de tecnologias nas práticas de escrita atuais.",
            "abordagem de fatos do contexto pessoal em uma perspectiva reflexiva.",
            "utilização de recursos linguísticos para a interlocução direta com o leitor.",
            "apresentação de acontecimentos segundo a ordem de sucessão no tempo."
        ],
        "label": "C"
    },
    {
        "numero": 8,
        "context": "Texto 'De próprio punho'",
        "question": "Nesse texto, o que caracteriza a escrita \"de próprio punho\" é a letra manuscrita, enquanto a escrita digital é ilustrada pelo(a)",
        "alternatives": [
            "utilização de tecnologias diversificadas.",
            "desenvolvimento de novos recursos de escrita.",
            "possibilidade de interações mediadas por telas.",
            "diversidade de fontes tipográficas que estão disponíveis.",
            "delimitação dos espaços onde a produção textual ocorre."
        ],
        "label": "D"
    },
    {
        "numero": 9,
        "context": "Texto 'De próprio punho'",
        "question": "A autora conclui que as novas tecnologias de escrita",
        "alternatives": [
            "evoluem para facilitar a vida cotidiana.",
            "alcançam diferentes realidades sociais.",
            "coexistem com outras já estabelecidas.",
            "promovem maior agilidade na comunicação.",
            "surgem nos contextos em que são necessárias."
        ],
        "label": "C"
    },
    {
        "numero": 10,
        "context": "Texto 'De próprio punho'",
        "question": "O recurso linguístico usado para marcar a síntese da opinião da autora sobre a temática desenvolvida foi o(a)",
        "alternatives": [
            "emprego da primeira pessoa em \"Estranhei muito na primeira vez que escutei a expressão 'de próprio punho'\". (l. 1)",
            "utilização de locução adverbial em \"Na verdade, o que importava era a autenticidade da minha caligrafia\". (l. 3-4)",
            "uso de pronome possessivo em \"Minha letra, hoje, tem uma espécie de alternância\". (l. 5-6)",
            "adoção de termo autorreflexivo em \"No escritório, costumo ser mais suave comigo mesma\". (l. 30)",
            "substituição da expressão \"Do punho ao pixel\" (l. 44) pela expressão \"o punho e o pixel\". (l. 45)"
        ],
        "label": "E"
    },
    # 11-17: Extraídas das imagens
    {
        "numero": 11,
        "context": "— Vejo, disse ele com algum acanhamento, que o doutor não é nenhum pé-rapado, mas nunca é bom facilitar... Minha filha Nocência fez 18 anos pelo Natal, e é rapariga que pela feição parece moça de cidade, muito ariscazinha de modos, mas bonita e boa deveras... Coitada, foi criada sem mãe, e aqui nestes fundões. [...] — Ora muito que bem, continuou Pereira caindo aos poucos na habitual garrulice, quando vi a menina tomar corpo, tratei logo de casá-la. — Ah! é casada? perguntou Cirino. — Isto é, é e não é. A coisa está apalavrada. Por aqui costuma labutar no costeio do gado para São Paulo um homem de mão-cheia, que talvez o sr. conheça... o Manecão Doca... — Não, respondeu Cirino abanando a cabeça. — Pois isso é um homem às direitas, desempenado e trabucador como ele só... fura estes sertões todos e vem tangendo pontes de gado que metem pasmo. Também dizem que tem bichado muito e ajuntado cobre grosso, o que é possível, porque não é gastador nem dado a mulheres. Uma feita que estava aqui de pousada... olhe, mesmo neste lugar onde estava mecê inda agorinha, falei-lhe em casamento... isto é, dei-lhe uns toques... porque os pais devem tomar isso a si para bem de suas famílias; não acha? — Boa dúvida, aprovou Cirino, dou-lhe toda a razão; era do seu dever.",
        "question": "Art. 26-A. Nos estabelecimentos de ensino fundamental e médio, oficiais e particulares, torna-se obrigatório o ensino sobre História e Cultura Afro-Brasileira. § 1º O conteúdo programático a que se refere o caput deste artigo incluirá o estudo da História da África e dos Africanos, a luta dos negros no Brasil, a cultura negra brasileira e o negro na formação da sociedade nacional, resgatando a contribuição do povo negro nas áreas social, econômica e política pertinentes à História do Brasil. § 2º Os conteúdos referentes à História e Cultura Afro-Brasileira serão ministrados no âmbito de todo o currículo escolar, em especial nas áreas de Educação Artística e de Literatura e História Brasileiras. O emprego da norma-padrão é justificado nesse texto",
        "alternatives": [
            "pela especialização de seu público-alvo.",
            "pela relevância cultural de seu conteúdo.",
            "pelos contextos pedagógicos em que circula.",
            "pela importância para os grupos étnico-raciais.",
            "pelas características do gênero a que pertence."
        ],
        "label": "E"
    },
    {
        "numero": 12,
        "question": "O Ministério do Esporte no Brasil lançou o programa Maré Inclusiva, em 2024, ano dos Jogos Paralímpicos de Paris. Esse programa visa ampliar as oportunidades para pessoas com deficiência que desejam praticar o surf. O parasurf é a prática do surf adaptada para permitir que pessoas com deficiência pratiquem o esporte em todas as suas categorias, modalidades e manifestações. Para a Secretaria Nacional do Paradesporto, a iniciativa é mais do que um programa de esporte, é uma iniciativa que busca transformar vidas e promover a inclusão por meio do parasurf, criando um legado de igualdade e respeito. De acordo com esse texto, o programa voltado ao estímulo da prática do parasurf evidencia a",
        "alternatives": [
            "adesão de diferentes países a programas inclusivos.",
            "preocupação política em atender a demandas paralímpicas.",
            "importância de uma política pública esportiva para a inclusão.",
            "eficiência das iniciativas de inclusão em megaeventos esportivos.",
            "escassez de investimento em práticas corporais de aventura na natureza."
        ],
        "label": "C"
    },
    {
        "numero": 13,
        "context": "— Vejo, disse ele com algum acanhamento, que o doutor não é nenhum pé-rapado, mas nunca é bom facilitar... Minha filha Nocência fez 18 anos pelo Natal, e é rapariga que pela feição parece moça de cidade, muito ariscazinha de modos, mas bonita e boa deveras... Coitada, foi criada sem mãe, e aqui nestes fundões. [...] — Ora muito que bem, continuou Pereira caindo aos poucos na habitual garrulice, quando vi a menina tomar corpo, tratei logo de casá-la. — Ah! é casada? perguntou Cirino. — Isto é, é e não é. A coisa está apalavrada. Por aqui costuma labutar no costeio do gado para São Paulo um homem de mão-cheia, que talvez o sr. conheça... o Manecão Doca... — Não, respondeu Cirino abanando a cabeça. — Pois isso é um homem às direitas, desempenado e trabucador como ele só... fura estes sertões todos e vem tangendo pontes de gado que metem pasmo. Também dizem que tem bichado muito e ajuntado cobre grosso, o que é possível, porque não é gastador nem dado a mulheres. Uma feita que estava aqui de pousada... olhe, mesmo neste lugar onde estava mecê inda agorinha, falei-lhe em casamento... isto é, dei-lhe uns toques... porque os pais devem tomar isso a si para bem de suas famílias; não acha? — Boa dúvida, aprovou Cirino, dou-lhe toda a razão; era do seu dever.",
        "question": "Nesse trecho, ao se referir à sua filha, o pai de Inocência reproduz os ideais românticos, presentes na",
        "alternatives": [
            "valorização do ambiente rural na formação moral da mulher.",
            "figura decorativa da mulher ante o protagonismo masculino.",
            "equivalência de origem social para a harmonia do casal.",
            "importância do dote como condição para o casamento.",
            "aura de mistério sobre a identidade da jovem."
        ],
        "label": "B"
    },
    {
        "numero": 14,
        "question": "Nesse cartaz publicitário, os recursos verbais e não verbais constroem um argumento que objetiva",
        "alternatives": [
            "divulgar a obra de Fernando Pessoa no Brasil.",
            "valorizar a realização de eventos literários no país.",
            "ressaltar o impacto da leitura na vida das pessoas.",
            "fomentar o turismo cultural na cidade de São Paulo.",
            "evidenciar a influência de Pessoa na literatura brasileira."
        ],
        "label": "C",
        "has_image": True
    },
    {
        "numero": 15,
        "question": "O retrato como gênero da pintura ocidental ficou vinculado às elites, tornando invisíveis as populações que não faziam parte do círculo dominante. Num país de tradição escravocrata e colonizado por europeus como o Brasil, pouquíssimas pessoas negras e indígenas foram retratadas em pintura, e menos ainda identificadas com seus nomes nos retratos. Daí a importância, para a história da arte e para a história brasileira, dos retratos de Dalton Paula. Ao dar protagonismo a Zeferina e a João de Deus Nascimento, o artista Dalton Paula evidencia que a(s)",
        "alternatives": [
            "arte pode promover formas de afirmação de identidade social.",
            "comunidades periféricas passam a adquirir o gênero retrato.",
            "personagens retratadas simbolizam a sociedade brasileira.",
            "pintura funciona como instrumento de ascensão social.",
            "imagens tradicionais preservam memórias afetivas."
        ],
        "label": "A",
        "has_image": True
    },
    {
        "numero": 16,
        "question": "Símbolos Eu e tu, ante a noite e o amplo desdobramento do mar, fero, a estourar de encontro à rocha nua... Um símbolo descubro aqui, neste momento esta rocha, este mar... a minha vida e a tua. O mar vem, o mar vai, nele há o gesto violento de quem maltrata e, após, se arrepende e recua. Como compreendo bem da rocha o sentimento! São muito iguais, por certo, a minha mágoa e a sua. Contemplo neste quadro a nossa triste vida; tu és dúbio mar que, na sua inconsciência, tem carinhos de amor e fúrias de demência! Eu sou a dor estanque, a dor empedernida, sou rocha a emergir de um côncavo de areia, imóvel, muda, isenta e alheia ao mar, alheia. Nesse soneto, os traços da estética simbolista são resgatados pelo eu lírico ao",
        "alternatives": [
            "rejeitar as emoções de \"amor\" e \"mágoa\".",
            "expressar a dubiedade do olhar sobre o outro.",
            "representar o \"eu\" e o \"tu\" como sujeitos volúveis.",
            "associar a sua inconsciência a elementos da natureza.",
            "metaforizar o conflito amoroso nas imagens de \"mar\" e \"rocha\"."
        ],
        "label": "E"
    },
    {
        "numero": 17,
        "question": "Antes do inverno chegar. Ela tinha olhinhos brilhantes. Os mesmos de antes. Antes da fome. Antes das 17 mudanças de cidade. Dos sete filhos e dos muitos anos de trabalho dentro e fora de casa. Ela fazia ambrosia, bolo de fubá e pedacinhos de queijo. Antes do inverno, ela plantava flores novas e diferentes para nos esperar nas próximas férias de verão. Ela tinha o jeito de menina. Menina sapeca, correndo na grama seca do cerrado. O mesmo jeito de antes. Antes do marido (e mesmo com o marido). Antes do cansaço dos anos. Antes da dureza do trato com a terra. Ela tinha histórias. Compridas, curtas, divertidas e verdadeiras. Mas isso foi antes. Antes das lembranças se bagunçarem feito bolas coloridas de Natal esperando para serem montadas na árvore. Eu era sua neta. Antes do Alzheimer chegar, eu era sua neta. Mas ela é e sempre será minha avó. A narradora, ao resgatar memórias da história de vida da avó, faz uso recorrente da locução \"antes de\". Esse termo colabora para a progressão temática na medida em que",
        "alternatives": [
            "relaciona eventos ocorridos simultaneamente.",
            "estabelece uma comparação entre as lembranças.",
            "ressalta fatos que ressignificam o momento presente.",
            "sinaliza uma sequência que denota ações consecutivas.",
            "apresenta uma explicação para as memórias resgatadas."
        ],
        "label": "C"
    },
    # 18-21: Extraídas das imagens
    {
        "numero": 18,
        "question": "Com 20 anos de experiência no futebol de alto rendimento, Marina, ex-jogadora da seleção brasileira de futebol, salienta que, por trás do espetáculo apresentado nas mídias, com mensagens de motivação e superação, o esporte não é tão inclusivo assim. \"É esta análise que devemos fazer: aqueles atletas que estão ali estão trazendo uma alta performance a partir dos seus limites\", explica. Para a profissional, é preciso analisar com cautela \"a ideia romântica que a mídia passa para os telespectadores\". A realidade é muito mais dura do que as imagens espetaculosas que principalmente a televisão busca transmitir para a audiência. \"Por trás existe um ser humano, a gente não pode nunca esquecer isso. Aquela pessoa treinou insistentemente para estar ali, durante meses, semanas e temporadas. Duas vezes ao dia, de duas a quatro horas\", pondera Marina. Atualmente, as crianças e os jovens vislumbram o sucesso profissional e a boa-vida financeira de poucos atletas que se destacam e estampam os meios de comunicação. Tudo parece ser muito mais fácil do que realmente é quando apenas as conquistas são mostradas. Nesse texto, a visão crítica de uma ex-atleta de futebol revela que",
        "alternatives": [
            "os meios de comunicação invisibilizam as dificuldades presentes no esporte.",
            "o treinamento atlético de alto nível é desestimulante para os indivíduos.",
            "o trabalho contínuo é desvalorizado no contexto esportivo profissional.",
            "as ações de incentivo financeiro a jovens atletas são precárias.",
            "as publicações da mídia esportiva rotulam atletas iniciantes."
        ],
        "label": "A"
    },
    {
        "numero": 19,
        "question": "No predomínio das mulheres pretas brasileiras nos Jogos Olímpicos de 2024, uma coisa chamou a atenção no pódio: elas valorizam a parte psicológica. As duas medalhistas de ouro, a judoca Beatriz Souza e a ginasta Rebeca Andrade, ressaltam, em várias entrevistas, a importância da saúde mental. Em uma dessas entrevistas, Rebeca sinaliza: \"Acho que não é só sobre vencer a Simone, é sobre vencer a mim mesma. A minha briga está na minha cabeça, não está com outras pessoas. Para conseguir fazer as minhas apresentações, preciso controlar a minha cabeça, o meu corpo, e essa é a briga\". Na mesma linha, a skatista Rayssa Leal exalta a necessidade da terapia, e a Seleção Brasileira de Futebol de Mulheres tem o suporte psicológico como reforço no treinamento. Nesse texto, as atletas brasileiras defendem o(a)",
        "alternatives": [
            "investimento na modernização de equipamentos.",
            "subordinação do treinamento físico ao mental.",
            "estímulo à competição entre adversárias.",
            "aprimoramento da expressão corporal.",
            "importância da saúde emocional."
        ],
        "label": "E"
    },
    {
        "numero": 20,
        "question": "A característica fundamental no aprendizado das práticas rituais nos candomblés é o processo iniciático e participante. Durante o período de reclusão em terreiros ou rocas, o iniciado passa por uma série de ritos esotéricos (banhos rituais, raspagem da cabeça etc.), ao mesmo tempo em que começa a adquirir um complexo código de símbolos materiais (substâncias, folhas, frutos, raízes etc.) e de gestos associados a um repertório linguístico específico das cerimônias que se desenrolam nos contextos sagrados em geral e em cada terreiro em particular. Esse repertório linguístico, genericamente chamado de \"língua de santo\" na Bahia, compreende uma terminologia religiosa operacional, de caráter mágico-semântico e de aparente forma portuguesa, mas que repousa sobre sistemas lexicais de diferentes línguas africanas que provavelmente foram faladas no Brasil escravocrata, vindo a constituir uma língua ritual, que se acredita pertencer à nação do vodum, do orixá ou do inquice, e não a determinada nação africana política atual. A \"língua de santo\" tem sua importância para o patrimônio linguístico brasileiro por",
        "alternatives": [
            "apresentar uma carga semântica mítica.",
            "conservar elementos dos falares dos escravizados.",
            "resgatar expressões portuguesas do período colonial.",
            "decodificar o ritual religioso dos nossos antepassados.",
            "favorecer a compreensão do léxico africano contemporâneo."
        ],
        "label": "B"
    },
    {
        "numero": 21,
        "question": "O meu medo é entrar na faculdade e tirar zero eu que nunca fui bom de matemática fraco no inglês eu que nunca gostei de química geografia e português o que é que eu faço agora hein mãe não sei. [...] O meu medo é a vida piorar e eu não conseguir arranjar emprego nem de faxineiro nem de porteiro nem de ajudante de pedreiro e o pessoal dizer que o governo já fez o que pôde já pôde o que fez já deu a sua cota de participação hein mãe não sei. O meu medo é que mesmo com diploma debaixo do braço andando por aí desiludido e desempregado o policial me olhe de cara feia e eu acabe fazendo uma burrice sei lá uma besteira será que eu vou ter direito a uma cela especial hein mãe não sei. Nesse texto, a reiteração dos medos e das angústias do narrador exprime",
        "alternatives": [
            "inseguranças sobre o futuro familiar.",
            "dilemas resultantes de seu fracasso escolar.",
            "incertezas centradas em sua condição social.",
            "hesitações em relação à sua formação profissional.",
            "preocupações com as políticas públicas assistenciais."
        ],
        "label": "C"
    },
    # 22-45: Continuar extraindo das imagens fornecidas
    {
        "numero": 22,
        "context": "TEXTO I: Origem, tradição e resistência - Foi sentada em seu banco de quartzo que a avó do universo, moradora da Maloca do Céu, criou os homens, os animais, a terra e as águas. O banco foi entregue aos ancestrais dos atuais Tukano, que passaram a reproduzi-lo em madeira. O mito Tukano — povo do noroeste da Amazônia que ainda hoje fabrica os bancos em seu estilo tradicional — indica o lugar dos bancos entre os objetos sagrados, ao mesmo tempo parte do universo primitivo e fonte do poder de criação. A presença nos mitos de origem de alguns povos atesta a antiguidade da arte de talhar bancos: os primeiros registros do uso desses objetos entre ameríndios das terras baixas da América do Sul, do Caribe e da América Central datam de, pelo menos, 4 mil anos.",
        "question": "Os textos I e II demonstram, na confecção dos bancos, uma íntima relação de sacralidade entre o ser humano e a natureza, perceptível por meio da",
        "alternatives": [
            "representação realista de animais, mostrando o domínio do homem sobre a natureza.",
            "manutenção da herança cultural, atribuindo nova função aos elementos da fauna.",
            "anulação dos traços que permitem reconhecer o animal representado.",
            "presença de grafismos na forma animal representada no banco.",
            "criação de figuras fantásticas baseadas em formas animais."
        ],
        "label": "D",
        "has_image": True
    },
    {
        "numero": 23,
        "context": "TEXTO I: Os trabalhos da exposição Adriana Varejão: suturas, fissuras, ruínas colocam em pauta o exame da história visual, das tradições iconográficas europeias e do fazer artístico ocidental. O corte, a rachadura, o talho e a fissura são elementos de narrativas recorrentes nos trabalhos da artista desde 1992. As produções recentes incluem pinturas tridimensionais de grande escala das séries Ruínas de charque e Línguas.",
        "question": "A utilização de recursos visuais como suturas, cortes e ruínas por Adriana Varejão, na obra Azulejaria em carne viva, remete à(s)",
        "alternatives": [
            "sobreposição da cultura brasileira à arte portuguesa.",
            "manutenção da representação realista na arte brasileira.",
            "violências desencadeadas pelo processo colonial brasileiro.",
            "desigualdades nos incentivos à produção artística brasileira.",
            "negligência na conservação do patrimônio arquitetônico luso-brasileiro."
        ],
        "label": "C",
        "has_image": True
    },
    {
        "numero": 24,
        "question": "Nesse cartaz, a utilização de frases que projetam a vida profissional de duas crianças tem como objetivo",
        "alternatives": [
            "sugerir a arrecadação de fundos para o sustento de povos originários no país.",
            "sensibilizar a sociedade sobre os benefícios decorrentes do combate ao racismo.",
            "indicar a importância da orientação vocacional na educação de crianças no Brasil.",
            "chamar a atenção sobre a necessidade de ações voltadas para a educação infantil.",
            "valorizar o trabalho de agências internacionais na luta contra a discriminação racial."
        ],
        "label": "B",
        "has_image": True
    },
    {
        "numero": 25,
        "question": "Passando por aqui para lembrar algumas palavras, frases e expressões que nos infernizaram em 2023. Inclusive passando por aqui. Se você for proativo, vai achar que é o novo normal. Estarão na sua zona de conforto. Mas, se for reativo como eu, vai achar que é uma narrativa que precisa ser ressignificada. É uma questão de empatia. É sobre entregar um discurso mais robusto e empoderado. Sei bem que não tenho lugar de fala para harmonizar certos pontos fora da curva e que preciso aplicar toda a minha resiliência para fazer um realinhamento. O nível de fitness está hoje num sarrafo muito alto. O fato é que acho cringe essas falas fora da caixinha. Aliás, falar cringe já é meio cringe. Preciso usar a superação para me reinventar e entender que resenha não tem mais a ver com futebol, é qualquer papo, desde que latente. Pensando bem, não é tão difícil. Frases feitas são aquelas que entram por um ouvido e saem pelo outro sem um estágio intermediário no cérebro. A boca fala por conta própria, dispensando-nos de pensar. E não tem problema nisso. Ou as ditas frases se incorporam à língua ou morrem e nascem outras. A língua é assim. Simples assim. Nesse texto, a estratégia empregada para criticar a constante exposição a palavras, frases e expressões automatizadas é o(a)",
        "alternatives": [
            "menção feita à efemeridade de alguns usos linguísticos aleatórios.",
            "subjetividade marcada pela reflexão que se desenvolve em primeira pessoa.",
            "efeito estilístico da repetição intencional da palavra \"assim\" no último parágrafo.",
            "sedução sugerida pelo envolvimento direto do leitor marcado nos usos de \"você\" e \"sua\".",
            "humor gerado pelo uso das estruturas linguísticas que são objeto da reflexão desenvolvida."
        ],
        "label": "E"
    },
    # Continuar com as demais questões das imagens...
    # Por enquanto, vou processar o que temos e aguardar mais imagens
]

# =============================================================================
# FUNÇÕES
# =============================================================================

def normalizar_questao(questao: Dict, numero: int) -> Dict:
    """Normaliza uma questão para o formato padrão."""
    questao_norm = {
        'id': f'enem_2025_languages_{numero}',
        'exam': '2025',
        'area': 'languages',
        'number': str(numero),
        'context': questao.get('context', ''),
        'question': questao.get('question', '').strip(),
        'alternatives': questao.get('alternatives', [])[:5],
        'label': questao.get('label', 'ANULADO').upper(),
        'has_images': questao.get('has_image', False)
    }
    
    while len(questao_norm['alternatives']) < 5:
        questao_norm['alternatives'].append('')
    
    return questao_norm


def main():
    """Função principal."""
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "data" / "enem"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("📸 EXTRAÇÃO DE QUESTÕES ENEM 2025 - LINGUAGENS")
    print("=" * 70)
    print()
    
    questoes_processadas = []
    for q in QUESTOES_LINGUAGENS_2025:
        numero = q.get('numero', 0)
        if 1 <= numero <= 45:
            questao_norm = normalizar_questao(q, numero)
            if questao_norm['question'] or questao_norm['context']:
                questoes_processadas.append(questao_norm)
    
    questoes_processadas.sort(key=lambda x: int(x['number']))
    
    print(f"✅ {len(questoes_processadas)} questões processadas")
    print()
    
    print("📊 Estatísticas:")
    print(f"   Total: {len(questoes_processadas)}")
    print(f"   Com imagens: {sum(1 for q in questoes_processadas if q.get('has_images', False))}")
    print(f"   Com gabarito: {sum(1 for q in questoes_processadas if q.get('label') != 'ANULADO')}")
    
    numeros = sorted([int(q['number']) for q in questoes_processadas])
    if numeros:
        print(f"   Questões: {numeros[0]}-{numeros[-1]}")
        faltantes = [i for i in range(1, 46) if i not in numeros]
        if faltantes:
            print(f"   ⚠️  Faltantes: {len(faltantes)} questões ({faltantes[:5]}{'...' if len(faltantes) > 5 else ''})")
    print()
    
    arquivo = output_dir / "enem_2025_linguagens_imagens.jsonl"
    with open(arquivo, 'w', encoding='utf-8') as f:
        for q in questoes_processadas:
            f.write(json.dumps(q, ensure_ascii=False) + '\n')
    
    print(f"💾 Salvo em: {arquivo}")
    print()
    print("⏳ Aguardando mais imagens para completar Linguagens (18-45)")
    print("   e depois Natureza e Matemática")


if __name__ == "__main__":
    main()

