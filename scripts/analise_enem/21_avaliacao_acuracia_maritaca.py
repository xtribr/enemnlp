#!/usr/bin/env python3
"""
Avaliação de Acurácia com API Maritaca Sabiá 3.1

Avalia questões do ENEM usando API Maritaca com foco em alcançar 90% de acurácia.
Usa campos semânticos para melhorar a precisão.
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def configurar_api_maritaca():
    """Configura conexão com API Maritaca"""
    import openai
    
    api_key = (
        os.environ.get("CURSORMINIMAC") or
        os.environ.get("MARITALK_API_SECRET_KEY") or
        os.environ.get("MARITACA_API_KEY")
    )
    
    if not api_key:
        print("❌ Chave API não configurada!")
        return None, None
    
    openai.api_base = "https://chat.maritaca.ai/api"
    openai_version = openai.__version__
    major_version = int(openai_version.split('.')[0])
    
    if major_version >= 1:
        client = openai.OpenAI(api_key=api_key, base_url="https://chat.maritaca.ai/api")
        return client, 'v1'
    else:
        openai.api_key = api_key
        return openai, 'v0'

def consultar_maritaca_para_prompt(client, versao: str, area: str, exemplo_questao: Dict = None) -> Optional[str]:
    """Sempre consulta Maritaca para otimizar o prompt"""
    import importlib.util
    
    # Importar módulo que começa com número usando importlib
    modulo_path = Path(__file__).parent / "28_sistema_maritaca_integrado.py"
    spec = importlib.util.spec_from_file_location("sistema_maritaca", modulo_path)
    if spec and spec.loader:
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo.criar_prompt_com_maritaca(client, versao, area, exemplo_questao)
    return None

def formatar_questao_para_maritaca(questao: Dict, usar_campos_semanticos: bool = True, 
                                   client=None, versao=None, usar_consulta_maritaca: bool = True) -> str:
    """Formata questão para avaliação pela API Maritaca com prompt otimizado"""
    contexto = questao.get('context', '').strip()
    pergunta = questao.get('question', '').strip()
    alternativas = questao.get('alternatives', [])
    area = questao.get('area', 'desconhecida')
    campos_semanticos = questao.get('campos_semanticos', [])
    
    # Mapear área para nome completo
    area_nomes = {
        'languages': 'Linguagens, Códigos e suas Tecnologias',
        'human-sciences': 'Ciências Humanas e suas Tecnologias',
        'natural-sciences': 'Ciências da Natureza e suas Tecnologias',
        'mathematics': 'Matemática e suas Tecnologias'
    }
    area_nome = area_nomes.get(area, area)
    
    # SEMPRE consultar Maritaca para otimizar o prompt
    if usar_consulta_maritaca and client and versao:
        # Usar questão atual como exemplo
        prompt_otimizado = consultar_maritaca_para_prompt(client, versao, area, questao)
        if prompt_otimizado:
            # Adicionar questão específica ao prompt otimizado
            prompt_completo = f"""{prompt_otimizado}

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
            for i, alt in enumerate(alternativas, 1):
                letra = chr(64 + i)
                prompt_completo += f"{letra}. {alt}\n"
            
            prompt_completo += """
RESPOSTA FINAL:
Após seguir TODOS os passos da metodologia acima, responda APENAS com a letra da alternativa correta (A, B, C, D ou E).
NÃO inclua explicações, apenas a letra."""
            
            return prompt_completo
    
    # Fallback: instruções baseadas em análises anteriores
    instrucoes_especificas = {
        'mathematics': """
ATENÇÃO CRÍTICA PARA MATEMÁTICA (área com maior dificuldade):
- Questões de matemática frequentemente envolvem múltiplos passos de resolução
- QUEBRE O PROBLEMA EM ETAPAS CLARAS e resolva cada uma individualmente
- Identifique e aplique fórmulas relevantes, mostrando cada substituição de variáveis
- Verifique todos os cálculos aritméticos e algébricos com cuidado
- Preste atenção EXTREMA a detalhes numéricos e unidades de medida
- Use CHECAGEM DIMENSIONAL: elimine alternativas com unidades incorretas
- Use ESTIMATIVAS RÁPIDAS para eliminar opções claramente desproporcionais
- Após resolver, VERIFIQUE se a resposta se encaixa nos dados fornecidos
- Traduza corretamente problemas de palavras em equações matemáticas
- NÃO escolha uma alternativa sem verificar os cálculos passo a passo
""",
        'natural-sciences': """
ATENÇÃO ESPECIAL PARA CIÊNCIAS DA NATUREZA:
- Questões de física, química e biologia requerem conhecimento científico preciso
- Verifique se os conceitos científicos estão corretos
- Preste atenção a relações de causa e efeito
- Elimine alternativas que contradizem princípios científicos fundamentais
""",
        'languages': """
ATENÇÃO ESPECIAL PARA LINGUAGENS:
- Questões de interpretação de texto requerem análise cuidadosa
- Identifique o tema central e a intenção do autor
- Preste atenção a nuances de significado
- Elimine alternativas que não estão diretamente relacionadas ao texto
""",
        'human-sciences': """
ATENÇÃO ESPECIAL PARA CIÊNCIAS HUMANAS:
- Questões de história, geografia, filosofia e sociologia requerem contextualização
- Relacione o conteúdo com o período histórico ou contexto social
- Preste atenção a relações de causa e consequência
- Elimine alternativas anacrônicas ou fora de contexto
"""
    }
    
    # Construir prompt otimizado com chain-of-thought
    prompt = f"""Você é um especialista em avaliações educacionais do ENEM (Exame Nacional do Ensino Médio).

ÁREA DE CONHECIMENTO: {area_nome}
"""
    
    # Adicionar campos semânticos se disponíveis
    if usar_campos_semanticos and campos_semanticos:
        prompt += f"CAMPOS SEMÂNTICOS IDENTIFICADOS: {', '.join(campos_semanticos)}\n"
        prompt += "Use esses campos para contextualizar melhor a questão.\n"
    
    # Adicionar instruções específicas da área
    prompt += instrucoes_especificas.get(area, "")
    
    prompt += f"""
METODOLOGIA DE RESOLUÇÃO OBRIGATÓRIA (siga estes passos em ordem):

PASSO 1 - INTERPRETAÇÃO DO PROBLEMA:
- Leia o contexto completo com atenção total
- Identifique EXATAMENTE o que a pergunta está pedindo
- Sublinhe ou liste mentalmente os dados fornecidos
- Identifique palavras-chave que indicam operações ou conceitos específicos

PASSO 2 - ESCOLHA DA ABORDAGEM:
- Decida qual método, fórmula ou conceito aplicar
- Para matemática: identifique as fórmulas relevantes
- Para ciências: identifique os princípios científicos envolvidos
- Para linguagens/humanas: identifique o tema central e intenção

PASSO 3 - RESOLUÇÃO PASSO A PASSO:
- Quebre o problema em etapas menores e resolva cada uma individualmente
- Para matemática: mostre cada substituição de variáveis e cálculo
- Execute a resolução de forma sistemática
- NÃO pule etapas

PASSO 4 - ELIMINAÇÃO DE ALTERNATIVAS:
Analise CADA alternativa individualmente e elimine as incorretas:
- Checagem Dimensional (matemática/ciências): Verifique se as unidades estão corretas
- Estimativas: Use estimativas rápidas para eliminar opções claramente desproporcionais
- Verificação Conceitual: A alternativa está correta do ponto de vista técnico/conceitual?
- Verificação Contextual: A alternativa faz sentido no contexto apresentado?
- Resposta Direta: A alternativa responde diretamente à pergunta feita?

PASSO 5 - VERIFICAÇÃO FINAL:
- Revise se a resposta faz sentido no contexto do problema
- Verifique se está em conformidade com as unidades de medida (se aplicável)
- Confirme que a resposta responde corretamente à pergunta feita
- NÃO escolha uma alternativa apenas porque parece plausível

PASSO 6 - ESCOLHA FINAL:
- Compare as alternativas restantes cuidadosamente
- Escolha a alternativa que melhor responde à pergunta
- Se não tiver certeza, analise novamente - NÃO escolha B por padrão
- Evite qualquer viés em direção a uma alternativa específica

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

ALTERNATIVAS:
"""
    
    for i, alt in enumerate(alternativas, 1):
        letra = chr(64 + i)  # A, B, C, D, E
        prompt += f"{letra}. {alt}\n"
    
    prompt += """
RESPOSTA FINAL:
Após seguir TODOS os 6 passos da metodologia acima, responda APENAS com a letra da alternativa correta (A, B, C, D ou E).

IMPORTANTE:
- NÃO inclua explicações, apenas a letra
- NÃO escolha B por padrão em caso de incerteza
- Se não tiver certeza após seguir todos os passos, analise novamente
- A resposta deve ser baseada na resolução passo a passo, não em intuição"""
    
    return prompt

def avaliar_questao(client, questao: Dict, versao: str, usar_campos_semanticos: bool = True,
                    client_prompt=None, versao_prompt=None, usar_consulta_maritaca: bool = True) -> Dict:
    """Avalia uma questão usando API Maritaca"""
    prompt = formatar_questao_para_maritaca(questao, usar_campos_semanticos, 
                                           client=client_prompt or client, 
                                           versao=versao_prompt or versao,
                                           usar_consulta_maritaca=usar_consulta_maritaca)
    resposta_correta = questao.get('label', '').upper().strip()
    
    try:
        if versao == 'v1':
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        else:
            response = client.ChatCompletion.create(
                model="sabia-3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.0
            )
            resposta_ia = response.choices[0].message.content.strip().upper()
        
        # Extrair apenas a letra (A, B, C, D, E)
        resposta_ia = resposta_ia[0] if resposta_ia and resposta_ia[0] in ['A', 'B', 'C', 'D', 'E'] else None
        
        acerto = resposta_ia == resposta_correta if resposta_ia else False
        
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': resposta_ia,
            'acerto': acerto,
            'area': questao.get('area', 'desconhecida')
        }
    
    except Exception as e:
        print(f"    ⚠️  Erro: {e}")
        return {
            'id': questao.get('id', ''),
            'resposta_correta': resposta_correta,
            'resposta_ia': None,
            'acerto': False,
            'erro': str(e)
        }

def avaliar_questoes(dados: Dict[int, List[Dict]], 
                    campos_semanticos: Dict = None,
                    anos: List[int] = None,
                    max_questoes_por_ano: int = None,
                    usar_campos_semanticos: bool = True,
                    sempre_consultar_maritaca: bool = True) -> Dict:
    """Avalia questões usando API Maritaca"""
    client, versao = configurar_api_maritaca()
    
    if not client:
        return {}
    
    # Carregar campos semânticos se disponíveis
    if campos_semanticos:
        for ano, dados_ano in campos_semanticos.items():
            if ano in dados:
                questoes_com_campos = {q['id']: q for q in dados_ano['questoes']}
                for questao in dados[ano]:
                    if questao['id'] in questoes_com_campos:
                        questao['campos_semanticos'] = questoes_com_campos[questao['id']].get('campos_semanticos', [])
    
    # Filtrar anos
    anos_para_avaliar = anos if anos else sorted(dados.keys())
    
    print(f"🎯 Objetivo: Alcançar 90% de acurácia")
    print(f"📊 Avaliando {len(anos_para_avaliar)} anos")
    if usar_campos_semanticos:
        print("✅ Usando campos semânticos para melhorar precisão")
    print()
    
    resultados = {}
    total_questoes = 0
    total_acertos = 0
    
    for ano in anos_para_avaliar:
        questoes = dados[ano]
        
        # Limitar questões se especificado
        if max_questoes_por_ano and len(questoes) > max_questoes_por_ano:
            import random
            questoes = random.sample(questoes, max_questoes_por_ano)
        
        print(f"📊 Avaliando {ano} ({len(questoes)} questões)...")
        
        avaliacoes_ano = []
        acertos_ano = 0
        
        for i, questao in enumerate(questoes, 1):
            print(f"  [{i}/{len(questoes)}] {questao.get('id', '')}...", end=' ')
            
            # Sempre usar consulta à Maritaca para otimizar prompt
            avaliacao = avaliar_questao(client, questao, versao, usar_campos_semanticos, 
                                        client_prompt=client, versao_prompt=versao, 
                                        usar_consulta_maritaca=sempre_consultar_maritaca)
            avaliacoes_ano.append(avaliacao)
            
            if avaliacao['acerto']:
                acertos_ano += 1
                print("✅")
            else:
                print(f"❌ (IA: {avaliacao.get('resposta_ia', 'N/A')}, Correta: {avaliacao['resposta_correta']})")
            
            time.sleep(0.5)  # Rate limiting
        
        acuracia_ano = (acertos_ano / len(questoes) * 100) if questoes else 0
        total_questoes += len(questoes)
        total_acertos += acertos_ano
        
        resultados[ano] = {
            'avaliacoes': avaliacoes_ano,
            'estatisticas': {
                'total': len(questoes),
                'acertos': acertos_ano,
                'erros': len(questoes) - acertos_ano,
                'acuracia': acuracia_ano
            }
        }
        
        print(f"  📊 Acurácia {ano}: {acuracia_ano:.2f}% ({acertos_ano}/{len(questoes)})")
        print()
    
    acuracia_geral = (total_acertos / total_questoes * 100) if total_questoes > 0 else 0
    
    print("=" * 70)
    print("📊 RESULTADOS FINAIS")
    print("=" * 70)
    print(f"Total de questões avaliadas: {total_questoes}")
    print(f"Total de acertos: {total_acertos}")
    print(f"Acurácia geral: {acuracia_geral:.2f}%")
    print()
    
    if acuracia_geral >= 90:
        print("🎉 OBJETIVO ALCANÇADO! Acurácia >= 90%")
    else:
        diferenca = 90 - acuracia_geral
        print(f"📈 Faltam {diferenca:.2f}% para alcançar 90% de acurácia")
    
    resultados['_geral'] = {
        'total_questoes': total_questoes,
        'total_acertos': total_acertos,
        'acuracia_geral': acuracia_geral
    }
    
    return resultados

def main():
    """Função principal"""
    print("=" * 70)
    print("🎯 AVALIAÇÃO DE ACURÁCIA - API MARITACA SABIÁ 3.1")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    analises_dir = project_root / "data" / "analises"
    
    # Carregar dados
    print("📥 Carregando dados...")
    dados = {}
    dados_orig = {}  # Manter original para estatísticas
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        dados_orig[ano] = questoes
        dados[ano] = questoes
    
    print(f"✅ {len(dados)} anos carregados")
    
    # Carregar campos semânticos se disponíveis
    campos_semanticos = None
    arquivo_campos = analises_dir / "campos_semanticos_completo.json"
    if arquivo_campos.exists():
        print("📥 Carregando campos semânticos...")
        with open(arquivo_campos, 'r', encoding='utf-8') as f:
            campos_semanticos = json.load(f)
        print("✅ Campos semânticos carregados")
    else:
        print("⚠️  Campos semânticos não encontrados")
        print("   Execute primeiro: 20_mapear_campos_semanticos.py")
    print()
    
    # Configurar avaliação
    # ✅ API com uso ilimitado - avaliar TODAS as questões
    anos_teste = None  # Todos os anos
    max_questoes = None  # Todas as questões
    
    # Filtrar apenas questões com resposta correta (não ANULADO)
    dados_filtrados = {}
    total_com_resposta = 0
    for ano, questoes in dados.items():
        questoes_validas = [q for q in questoes if q.get('label', '').upper() not in ['ANULADO', '']]
        if questoes_validas:
            dados_filtrados[ano] = questoes_validas
            total_com_resposta += len(questoes_validas)
    
    dados = dados_filtrados  # Usar apenas questões com resposta
    
    total_questoes = sum(len(q) for q in dados.values())
    print("✅ CONFIGURAÇÃO: Processando TODAS as questões (API ilimitada)")
    print(f"   Anos: Todos ({len(dados)} anos)")
    print(f"   Questões por ano: Todas (com resposta correta)")
    print(f"   Total: {total_questoes} questões (de {total_com_resposta + sum(len([q for q in dados_orig.get(ano, []) if q.get('label', '').upper() == 'ANULADO']) for ano in dados_orig.keys())} total)")
    print()
    
    # Avaliar
    resultados = avaliar_questoes(
        dados,
        campos_semanticos=campos_semanticos,
        anos=anos_teste,
        max_questoes_por_ano=max_questoes,
        usar_campos_semanticos=True,
        sempre_consultar_maritaca=True  # SEMPRE consultar Maritaca
    )
    
    if resultados:
        # Salvar resultados
        arquivo = analises_dir / "avaliacao_acuracia_maritaca.json"
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Resultados salvos em: {arquivo}")
        print()
        print("=" * 70)
        print("✅ AVALIAÇÃO CONCLUÍDA")
        print("=" * 70)
        print()
        print("💡 Para avaliação completa:")
        print("   1. Ajuste 'anos_teste' e 'max_questoes' no script")
        print("   2. Execute novamente para avaliar mais questões")
        print("   3. Monitore custos da API")

if __name__ == "__main__":
    main()

