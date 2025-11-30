#!/usr/bin/env python3
"""
Validação de dados históricos do ENEM

Verifica integridade, estatísticas e qualidade dos dados carregados.
"""
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def carregar_dados_processados(processed_dir: Path) -> Dict[int, List[Dict]]:
    """Carrega todos os dados processados"""
    dados = {}
    
    for jsonl_file in sorted(processed_dir.glob("enem_*_completo.jsonl")):
        ano = int(jsonl_file.stem.split('_')[1])
        questoes = []
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    questoes.append(json.loads(line))
        
        dados[ano] = questoes
    
    return dados

def validar_estrutura(dados: Dict[int, List[Dict]]) -> Dict[str, Any]:
    """Valida estrutura básica dos dados"""
    problemas = []
    estatisticas = {
        'total_anos': len(dados),
        'total_questoes': sum(len(questoes) for questoes in dados.values()),
        'questoes_por_ano': {},
        'campos_obrigatorios': ['id', 'exam', 'question', 'alternatives', 'label'],
        'campos_faltantes': defaultdict(int),
        'labels_invalidas': 0,
        'alternativas_incompletas': 0
    }
    
    for ano, questoes in dados.items():
        estatisticas['questoes_por_ano'][ano] = len(questoes)
        
        for questao in questoes:
            # Verificar campos obrigatórios
            for campo in estatisticas['campos_obrigatorios']:
                if campo not in questao:
                    estatisticas['campos_faltantes'][campo] += 1
                    problemas.append(f"Ano {ano}: Campo '{campo}' faltando em questão {questao.get('id', 'desconhecido')}")
            
            # Validar label
            if 'label' in questao:
                if questao['label'] not in ['A', 'B', 'C', 'D', 'E']:
                    estatisticas['labels_invalidas'] += 1
                    problemas.append(f"Ano {ano}: Label inválida '{questao['label']}' em {questao.get('id', 'desconhecido')}")
            
            # Validar alternativas
            if 'alternatives' in questao:
                if len(questao['alternatives']) != 5:
                    estatisticas['alternativas_incompletas'] += 1
                    problemas.append(f"Ano {ano}: Alternativas incompletas em {questao.get('id', 'desconhecido')}")
    
    return {
        'estatisticas': estatisticas,
        'problemas': problemas,
        'valido': len(problemas) == 0
    }

def analisar_por_area(dados: Dict[int, List[Dict]]) -> Dict[str, Any]:
    """Analisa distribuição por área de conhecimento"""
    areas_por_ano = defaultdict(lambda: defaultdict(int))
    total_por_area = defaultdict(int)
    
    for ano, questoes in dados.items():
        for questao in questoes:
            area = questao.get('area', 'desconhecida')
            areas_por_ano[ano][area] += 1
            total_por_area[area] += 1
    
    return {
        'por_ano': dict(areas_por_ano),
        'total': dict(total_por_area)
    }

def analisar_complexidade_texto(dados: Dict[int, List[Dict]]) -> Dict[str, Any]:
    """Analisa complexidade textual básica"""
    metricas_por_ano = defaultdict(lambda: {
        'tamanho_medio_questao': [],
        'tamanho_medio_contexto': [],
        'questoes_com_imagens': 0,
        'total_questoes': 0
    })
    
    for ano, questoes in dados.items():
        for questao in questoes:
            metricas = metricas_por_ano[ano]
            metricas['total_questoes'] += 1
            
            # Tamanho da questão
            questao_texto = questao.get('question', '')
            metricas['tamanho_medio_questao'].append(len(questao_texto))
            
            # Tamanho do contexto
            contexto = questao.get('context', '')
            metricas['tamanho_medio_contexto'].append(len(contexto))
            
            # Questões com imagens
            if questao.get('has_images', False) or questao.get('context_images'):
                metricas['questoes_com_imagens'] += 1
    
    # Calcular médias
    resultado = {}
    for ano, metricas in metricas_por_ano.items():
        resultado[ano] = {
            'tamanho_medio_questao': sum(metricas['tamanho_medio_questao']) / len(metricas['tamanho_medio_questao']) if metricas['tamanho_medio_questao'] else 0,
            'tamanho_medio_contexto': sum(metricas['tamanho_medio_contexto']) / len(metricas['tamanho_medio_contexto']) if metricas['tamanho_medio_contexto'] else 0,
            'questoes_com_imagens': metricas['questoes_com_imagens'],
            'percentual_imagens': (metricas['questoes_com_imagens'] / metricas['total_questoes'] * 100) if metricas['total_questoes'] > 0 else 0,
            'total_questoes': metricas['total_questoes']
        }
    
    return resultado

def gerar_relatorio_validacao(validacao: Dict, analise_area: Dict, complexidade: Dict) -> str:
    """Gera relatório de validação formatado"""
    relatorio = []
    relatorio.append("=" * 70)
    relatorio.append("📊 RELATÓRIO DE VALIDAÇÃO - DADOS ENEM")
    relatorio.append("=" * 70)
    relatorio.append("")
    
    # Estatísticas gerais
    stats = validacao['estatisticas']
    relatorio.append("📈 ESTATÍSTICAS GERAIS")
    relatorio.append("-" * 70)
    relatorio.append(f"Total de anos: {stats['total_anos']}")
    relatorio.append(f"Período: {min(stats['questoes_por_ano'].keys())} - {max(stats['questoes_por_ano'].keys())}")
    relatorio.append(f"Total de questões: {stats['total_questoes']:,}")
    relatorio.append(f"Média por ano: {stats['total_questoes'] / stats['total_anos']:.0f} questões")
    relatorio.append("")
    
    # Questões por ano
    relatorio.append("📅 QUESTÕES POR ANO")
    relatorio.append("-" * 70)
    for ano in sorted(stats['questoes_por_ano'].keys()):
        count = stats['questoes_por_ano'][ano]
        barra = "█" * (count // 5)
        relatorio.append(f"  {ano}: {count:3d} questões {barra}")
    relatorio.append("")
    
    # Distribuição por área
    relatorio.append("📚 DISTRIBUIÇÃO POR ÁREA DE CONHECIMENTO")
    relatorio.append("-" * 70)
    for area, total in sorted(analise_area['total'].items()):
        percentual = (total / stats['total_questoes']) * 100
        relatorio.append(f"  {area:20s}: {total:4d} questões ({percentual:5.1f}%)")
    relatorio.append("")
    
    # Complexidade textual
    relatorio.append("📝 COMPLEXIDADE TEXTUAL (Médias)")
    relatorio.append("-" * 70)
    relatorio.append(f"{'Ano':<6} {'Questão':<10} {'Contexto':<10} {'Imagens':<10} {'% Img':<8}")
    relatorio.append("-" * 70)
    for ano in sorted(complexidade.keys()):
        comp = complexidade[ano]
        relatorio.append(
            f"{ano:<6} "
            f"{comp['tamanho_medio_questao']:>8.0f} "
            f"{comp['tamanho_medio_contexto']:>8.0f} "
            f"{comp['questoes_com_imagens']:>8d} "
            f"{comp['percentual_imagens']:>6.1f}%"
        )
    relatorio.append("")
    
    # Problemas encontrados
    if validacao['problemas']:
        relatorio.append("⚠️  PROBLEMAS ENCONTRADOS")
        relatorio.append("-" * 70)
        for problema in validacao['problemas'][:20]:  # Mostrar apenas primeiros 20
            relatorio.append(f"  • {problema}")
        if len(validacao['problemas']) > 20:
            relatorio.append(f"  ... e mais {len(validacao['problemas']) - 20} problemas")
        relatorio.append("")
    else:
        relatorio.append("✅ NENHUM PROBLEMA ENCONTRADO")
        relatorio.append("")
    
    # Validação geral
    relatorio.append("=" * 70)
    if validacao['valido']:
        relatorio.append("✅ VALIDAÇÃO: DADOS VÁLIDOS")
    else:
        relatorio.append(f"⚠️  VALIDAÇÃO: {len(validacao['problemas'])} PROBLEMAS ENCONTRADOS")
    relatorio.append("=" * 70)
    
    return "\n".join(relatorio)

def main():
    """Função principal"""
    print("=" * 70)
    print("🔍 VALIDAÇÃO DE DADOS HISTÓRICOS DO ENEM")
    print("=" * 70)
    print()
    
    # Diretórios
    project_root = Path(__file__).parent.parent.parent
    processed_dir = project_root / "data" / "processed"
    
    if not processed_dir.exists():
        print(f"❌ Diretório não encontrado: {processed_dir}")
        print("   Execute primeiro: 01_carregar_dados_historico.py")
        return
    
    # 1. Carregar dados
    print("📥 Carregando dados processados...")
    dados = carregar_dados_processados(processed_dir)
    print(f"✅ {len(dados)} anos carregados")
    print()
    
    # 2. Validar estrutura
    print("🔍 Validando estrutura dos dados...")
    validacao = validar_estrutura(dados)
    print(f"✅ Validação concluída")
    print()
    
    # 3. Analisar por área
    print("📚 Analisando distribuição por área...")
    analise_area = analisar_por_area(dados)
    print("✅ Análise concluída")
    print()
    
    # 4. Analisar complexidade
    print("📝 Analisando complexidade textual...")
    complexidade = analisar_complexidade_texto(dados)
    print("✅ Análise concluída")
    print()
    
    # 5. Gerar relatório
    relatorio = gerar_relatorio_validacao(validacao, analise_area, complexidade)
    print(relatorio)
    
    # 6. Salvar relatório
    relatorio_file = project_root / "reports" / "validacao_dados_historicos.txt"
    relatorio_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(relatorio_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"💾 Relatório salvo em: {relatorio_file}")
    print()
    
    # 7. Salvar estatísticas em JSON
    stats_file = project_root / "data" / "analises" / "estatisticas_dados.json"
    stats_file.parent.mkdir(parents=True, exist_ok=True)
    
    estatisticas_completas = {
        'validacao': {
            'valido': validacao['valido'],
            'total_problemas': len(validacao['problemas']),
            'estatisticas': validacao['estatisticas']
        },
        'areas': analise_area,
        'complexidade': complexidade
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(estatisticas_completas, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Estatísticas salvas em: {stats_file}")

if __name__ == "__main__":
    main()


