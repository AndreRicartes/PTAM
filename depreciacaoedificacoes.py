#Avaliacao pelo metodo evolutivo
''' 
Vi = (Vt + Cb) x Fc
Vi = valor inicial
Vt = valor total
Cb = custo de benfeitorias
Fc = fator de comercialização
Cálculo de depreciação de edificações
'''
# Vida útil dos imóveis estabelecido pelo Bureu of Internal Revenue Service (IRS)

vida_util_imoveis = {
    "Residenciais": {
        "Apartamentos": {
            "econômico, simples ou médio": 60,
            "fino ou luxo": 50
        },
        "Casas": {
            "alvenaria": 65,
            "madeira": 45
        }
    },
    "Comerciais": {
        "Bancos": 70,
        "Escritórios": {
            "econômico ou simples": 70,
            "médio": 60,
            "fino ou luxo": 50
        },
        "Lojas": 70
    },
    "Industriais": {
        "Armazéns": 75,
        "Galpões": {
            "rústico ou simples": 60,
            "médio ou superior": 80
        },
        "Fábricas": 50
    },
    "Outros Tipos de Construções": {
        "Hotéis": 50,
        "Teatros": 50,
        "Construções rurais (gerais)": 60,
        "Silos": 75
    }
}


classificacao_imoveis = {
    "A": "Novo",
    "B": "Entre novo e regular",
    "C": "Regular",
    "D": "Entre regular e reparos simples",
    "E": "Reparos simples",
    "F": "Entre reparos simples e importantes",
    "G": "Reparos importantes",
    "H": "Entre reparos importantes e sem valor"
} 


# Tabela de coeficientes de depreciação de edificações
ir_vu = {
    2.00: {"A": 1.02, "B": 1.05, "C": 3.51, "D": 9.03, "E": 18.90, "F": 39.30, "G": 53.10, "H": 75.40},
    4.00: {"A": 2.08, "B": 2.11, "C": 4.55, "D": 10.00, "E": 19.80, "F": 34.60, "G": 53.60, "H": 75.70},
    6.00: {"A": 3.18, "B": 3.21, "C": 5.62, "D": 11.00, "E": 20.70, "F": 35.30, "G": 54.10, "H": 76.00},
    8.00: {"A": 4.32, "B": 4.35, "C": 6.73, "D": 12.10, "E": 21.60, "F": 36.10, "G": 54.60, "H": 76.30},
    10.00: {"A": 5.50, "B": 5.53, "C": 7.88, "D": 13.20, "E": 22.60, "F": 36.90, "G": 55.20, "H": 76.60},
    12.00: {"A": 6.72, "B": 6.75, "C": 9.07, "D": 14.30, "E": 23.60, "F": 37.70, "G": 55.80, "H": 76.90},
    14.00: {"A": 7.98, "B": 8.01, "C": 10.30, "D": 15.40, "E": 24.60, "F": 38.50, "G": 56.40, "H": 77.20},
    16.00: {"A": 9.28, "B": 9.31, "C": 11.60, "D": 16.60, "E": 25.70, "F": 39.40, "G": 57.00, "H": 77.50},
    18.00: {"A": 10.60, "B": 10.60, "C": 12.90, "D": 17.80, "E": 26.80, "F": 40.30, "G": 57.60, "H": 77.80},
    20.00: {"A": 12.00, "B": 12.00, "C": 14.20, "D": 19.10, "E": 27.90, "F": 41.80, "G": 58.30, "H": 78.20},
    22.00: {"A": 13.40, "B": 13.40, "C": 15.60, "D": 20.40, "E": 29.10, "F": 42.20, "G": 59.00, "H": 78.50},
    24.00: {"A": 14.90, "B": 14.90, "C": 17.00, "D": 21.80, "E": 30.30, "F": 43.10, "G": 59.60, "H": 78.90},
    26.00: {"A": 16.40, "B": 16.40, "C": 18.50, "D": 23.10, "E": 31.50, "F": 44.10, "G": 60.40, "H": 79.30},
    28.00: {"A": 17.90, "B": 17.90, "C": 20.00, "D": 24.60, "E": 32.80, "F": 45.20, "G": 61.10, "H": 79.60},
    30.00: {"A": 19.50, "B": 19.50, "C": 21.50, "D": 26.00, "E": 34.10, "F": 46.20, "G": 61.80, "H": 80.00},
    32.00: {"A": 21.10, "B": 21.10, "C": 23.10, "D": 27.50, "E": 35.40, "F": 47.30, "G": 62.60, "H": 80.40},
    34.00: {"A": 22.80, "B": 22.80, "C": 24.70, "D": 29.00, "E": 36.80, "F": 48.40, "G": 63.40, "H": 80.80},
    36.00: {"A": 24.50, "B": 24.50, "C": 26.40, "D": 30.50, "E": 38.10, "F": 49.50, "G": 64.20, "H": 81.30},
    38.00: {"A": 26.20, "B": 26.20, "C": 28.10, "D": 32.20, "E": 39.60, "F": 50.70, "G": 65.00, "H": 81.70},
    40.00: {"A": 28.80, "B": 28.80, "C": 29.90, "D": 33.80, "E": 41.00, "F": 51.90, "G": 65.90, "H": 82.10},
    42.00: {"A": 29.90, "B": 29.80, "C": 31.60, "D": 35.50, "E": 42.50, "F": 53.10, "G": 66.70, "H": 82.60},
    44.00: {"A": 31.70, "B": 31.70, "C": 33.40, "D": 37.20, "E": 44.00, "F": 54.40, "G": 67.60, "H": 83.10},
    46.00: {"A": 33.60, "B": 33.60, "C": 35.20, "D": 38.90, "E": 45.60, "F": 55.60, "G": 68.50, "H": 83.50},
    48.00: {"A": 35.60, "B": 35.50, "C": 37.10, "D": 40.70, "E": 47.20, "F": 56.90, "G": 69.40, "H": 84.00},
    50.00: {"A": 37.50, "B": 37.50, "C": 39.10, "D": 42.60, "E": 48.80, "F": 58.20, "G": 70.40, "H": 84.50},
    52.00: {"A": 39.50, "B": 39.50, "C": 41.90, "D": 44.00, "E": 50.50, "F": 59.60, "G": 71.30, "H": 85.00},
    54.00: {"A": 41.60, "B": 41.60, "C": 43.00, "D": 46.30, "E": 52.10, "F": 61.00, "G": 72.30, "H": 85.50},
    56.00: {"A": 43.70, "B": 43.70, "C": 45.10, "D": 48.20, "E": 53.90, "F": 62.40, "G": 73.30, "H": 86.00},
    58.00: {"A": 45.80, "B": 45.80, "C": 47.20, "D": 50.20, "E": 55.60, "F": 63.80, "G": 74.30, "H": 86.60},
    60.00: {"A": 48.80, "B": 48.80, "C": 49.30, "D": 52.20, "E": 57.40, "F": 65.30, "G": 75.30, "H": 87.10},
    62.00: {"A": 50.20, "B": 50.20, "C": 51.50, "D": 54.20, "E": 59.20, "F": 66.70, "G": 75.40, "H": 87.70},
    64.00: {"A": 52.50, "B": 52.50, "C": 53.70, "D": 56.30, "E": 61.10, "F": 68.30, "G": 77.50, "H": 88.20},
    66.00: {"A": 54.80, "B": 54.80, "C": 55.90, "D": 58.40, "E": 69.00, "F": 69.80, "G": 78.60, "H": 88.80},
    68.00: {"A": 57.10, "B": 57.10, "C": 58.20, "D": 60.60, "E": 64.90, "F": 71.40, "G": 79.70, "H": 89.40},
    70.00: {"A": 59.50, "B": 59.50, "C": 60.50, "D": 62.80, "E": 66.80, "F": 72.90, "G": 80.80, "H": 90.40},
    72.00: {"A": 62.20, "B": 62.20, "C": 62.90, "D": 65.00, "E": 68.80, "F": 74.60, "G": 81.90, "H": 90.90},
    74.00: {"A": 64.40, "B": 64.40, "C": 65.30, "D": 67.30, "E": 70.80, "F": 76.20, "G": 83.10, "H": 91.20},
    76.00: {"A": 66.90, "B": 66.90, "C": 67.70, "D": 69.60, "E": 72.90, "F": 77.90, "G": 84.30, "H": 91.80},
    78.00: {"A": 69.40, "B": 69.40, "C": 72.20, "D": 71.90, "E": 74.90, "F": 79.60, "G": 85.50, "H": 92.40},
    80.00: {"A": 72.00, "B": 72.00, "C": 72.70, "D": 74.30, "E": 77.10, "F": 81.30, "G": 86.70, "H": 93.10},
    82.00: {"A": 74.60, "B": 74.60, "C": 75.30, "D": 76.70, "E": 79.20, "F": 83.00, "G": 88.00, "H": 93.70},
    84.00: {"A": 77.30, "B": 77.30, "C": 77.80, "D": 79.10, "E": 81.40, "F": 84.50, "G": 89.20, "H": 94.40},
    86.00: {"A": 80.00, "B": 80.00, "C": 80.50, "D": 81.60, "E": 83.60, "F": 86.60, "G": 90.50, "H": 95.00},
    88.00: {"A": 82.70, "B": 82.70, "C": 83.20, "D": 84.10, "E": 85.80, "F": 88.50, "G": 91.80, "H": 95.70},
    90.00: {"A": 85.50, "B": 85.50, "C": 85.90, "D": 86.70, "E": 88.10, "F": 90.30, "G": 93.10, "H": 96.40},
    92.00: {"A": 88.30, "B": 88.30, "C": 88.60, "D": 89.30, "E": 90.40, "F": 92.20, "G": 94.50, "H": 97.10},
    94.00: {"A": 91.20, "B": 91.20, "C": 91.40, "D": 91.90, "E": 92.80, "F": 94.10, "G": 95.80, "H": 97.80},
    96.00: {"A": 94.10, "B": 94.10, "C": 94.20, "D": 94.60, "E": 95.10, "F": 96.00, "G": 97.20, "H": 98.50},
    98.00: {"A": 97.00, "B": 97.00, "C": 97.10, "D": 97.30, "E": 97.60, "F": 98.00, "G": 98.00, "H": 99.80},
    100.00: {"A": 100.00, "B": 100.00, "C": 100.00, "D": 100.00, "E": 100.00, "F": 100.00, "G": 100.00, "H": 100.00},
}

# Obter o valor de IR para 4% de vida útil e estado de conservação 'c'
ir_valor = ir_vu[4]["C"]
print(ir_valor)  # Saída: 4.55