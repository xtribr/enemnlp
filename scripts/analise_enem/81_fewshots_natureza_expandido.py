#!/usr/bin/env python3
"""
🔬 Few-Shots Expandidos para Natureza

Cria banco expandido de few-shots para Ciências da Natureza
para reduzir gap de -9.09% vs GPT-4o.

Objetivo: Aumentar de 84.09% para 93%+
"""

from typing import List, Dict

FEW_SHOTS_NATUREZA_EXPANDIDO = [
    # Física - Mecânica
    {
        'question': 'Um objeto de massa 2 kg é acelerado por uma força de 10 N. Qual é a aceleração?',
        'alternatives': ['A) 2 m/s²', 'B) 5 m/s²', 'C) 10 m/s²', 'D) 20 m/s²', 'E) 50 m/s²'],
        'response': 'Usando F = ma: 10 = 2a → a = 5 m/s². Resposta: B'
    },
    {
        'question': 'Um carro percorre 100 km em 2 horas. Qual é a velocidade média?',
        'alternatives': ['A) 25 km/h', 'B) 50 km/h', 'C) 75 km/h', 'D) 100 km/h', 'E) 200 km/h'],
        'response': 'Velocidade média = distância/tempo = 100 km / 2 h = 50 km/h. Resposta: B'
    },
    # Física - Termodinâmica
    {
        'question': 'Se a temperatura de um gás aumenta de 27°C para 127°C, quantas vezes aumenta a energia cinética média?',
        'alternatives': ['A) 1.33', 'B) 1.5', 'C) 2', 'D) 2.5', 'E) 4'],
        'response': 'Convertendo para Kelvin: 27°C = 300K, 127°C = 400K. Razão = 400/300 = 1.33. Resposta: A'
    },
    # Química - Estequiometria
    {
        'question': 'Na reação 2H₂ + O₂ → 2H₂O, quantos mols de água são produzidos a partir de 4 mols de H₂?',
        'alternatives': ['A) 2', 'B) 4', 'C) 6', 'D) 8', 'E) 10'],
        'response': 'Proporção: 2 mols H₂ produzem 2 mols H₂O. Então 4 mols H₂ produzem 4 mols H₂O. Resposta: B'
    },
    {
        'question': 'Qual é a massa molar do CO₂? (C=12, O=16)',
        'alternatives': ['A) 28 g/mol', 'B) 32 g/mol', 'C) 44 g/mol', 'D) 56 g/mol', 'E) 60 g/mol'],
        'response': 'Massa molar = 12 + 2(16) = 12 + 32 = 44 g/mol. Resposta: C'
    },
    # Química - Soluções
    {
        'question': 'Uma solução tem concentração de 0.5 mol/L e volume de 2 L. Quantos mols há na solução?',
        'alternatives': ['A) 0.25', 'B) 0.5', 'C) 1.0', 'D) 1.5', 'E) 2.0'],
        'response': 'n = C × V = 0.5 mol/L × 2 L = 1.0 mol. Resposta: C'
    },
    # Biologia - Genética
    {
        'question': 'Em um cruzamento Aa × Aa, qual a probabilidade de nascer aa?',
        'alternatives': ['A) 0%', 'B) 25%', 'C) 50%', 'D) 75%', 'E) 100%'],
        'response': 'Cruzamento Aa × Aa: AA (25%), Aa (50%), aa (25%). Probabilidade de aa = 25%. Resposta: B'
    },
    # Biologia - Ecologia
    {
        'question': 'Em uma cadeia alimentar: produtor → consumidor primário → consumidor secundário. Se há 1000 kcal no produtor, quantas kcal chegam ao consumidor secundário? (eficiência 10%)',
        'alternatives': ['A) 1 kcal', 'B) 10 kcal', 'C) 100 kcal', 'D) 500 kcal', 'E) 1000 kcal'],
        'response': 'Produtor: 1000 kcal → Consumidor primário: 100 kcal (10%) → Consumidor secundário: 10 kcal (10%). Resposta: B'
    },
    # Gráficos e Tabelas
    {
        'question': 'Um gráfico mostra que a velocidade aumenta linearmente de 0 a 20 m/s em 10 segundos. Qual é a aceleração?',
        'alternatives': ['A) 0.5 m/s²', 'B) 1 m/s²', 'C) 2 m/s²', 'D) 5 m/s²', 'E) 10 m/s²'],
        'response': 'Aceleração = Δv/Δt = (20-0)/(10-0) = 20/10 = 2 m/s². Resposta: C'
    },
    {
        'question': 'Uma tabela mostra pH de diferentes soluções. Qual tem maior acidez?',
        'alternatives': ['A) pH = 7', 'B) pH = 5', 'C) pH = 3', 'D) pH = 9', 'E) pH = 11'],
        'response': 'Menor pH = maior acidez. pH = 3 é o menor, logo mais ácido. Resposta: C'
    },
    # Unidades e Conversões
    {
        'question': 'Converta 2 km para metros.',
        'alternatives': ['A) 20 m', 'B) 200 m', 'C) 2000 m', 'D) 20000 m', 'E) 200000 m'],
        'response': '1 km = 1000 m, então 2 km = 2 × 1000 = 2000 m. Resposta: C'
    },
    {
        'question': 'Um objeto tem massa de 500 g. Qual é a massa em kg?',
        'alternatives': ['A) 0.05 kg', 'B) 0.5 kg', 'C) 5 kg', 'D) 50 kg', 'E) 500 kg'],
        'response': '1 kg = 1000 g, então 500 g = 500/1000 = 0.5 kg. Resposta: B'
    },
    # Relações Causa-Efeito
    {
        'question': 'O que acontece com a pressão de um gás quando o volume diminui (temperatura constante)?',
        'alternatives': ['A) Aumenta', 'B) Diminui', 'C) Permanece constante', 'D) Primeiro aumenta depois diminui', 'E) Não é possível determinar'],
        'response': 'Lei de Boyle: P × V = constante. Se V diminui, P aumenta. Resposta: A'
    },
    {
        'question': 'Em uma reação exotérmica, o que acontece com a temperatura do sistema?',
        'alternatives': ['A) Aumenta', 'B) Diminui', 'C) Permanece constante', 'D) Oscila', 'E) Não há relação'],
        'response': 'Reação exotérmica libera calor, então a temperatura aumenta. Resposta: A'
    },
    # Análise de Dados Científicos
    {
        'question': 'Um experimento mostra que a taxa de reação dobra quando a temperatura aumenta de 25°C para 35°C. Qual é o fator de aumento?',
        'alternatives': ['A) 1.5', 'B) 2', 'C) 2.5', 'D) 3', 'E) 4'],
        'response': 'A taxa dobra, então o fator é 2. Resposta: B'
    }
]

def obter_fewshots_natureza(num_exemplos: int = 10) -> List[Dict]:
    """
    Retorna few-shots de Natureza
    
    Args:
        num_exemplos: Número de exemplos a retornar (default: 10)
        
    Returns:
        Lista de few-shots
    """
    return FEW_SHOTS_NATUREZA_EXPANDIDO[:num_exemplos]

if __name__ == "__main__":
    print("=" * 70)
    print("🔬 Few-Shots Expandidos para Natureza")
    print("=" * 70)
    print()
    print(f"✅ {len(FEW_SHOTS_NATUREZA_EXPANDIDO)} exemplos criados")
    print()
    print("📚 Categorias:")
    print("  - Física (Mecânica, Termodinâmica)")
    print("  - Química (Estequiometria, Soluções)")
    print("  - Biologia (Genética, Ecologia)")
    print("  - Gráficos e Tabelas")
    print("  - Unidades e Conversões")
    print("  - Relações Causa-Efeito")
    print("  - Análise de Dados Científicos")
    print()
    print("🎯 Objetivo: Aumentar acurácia de 84.09% para 93%+")

