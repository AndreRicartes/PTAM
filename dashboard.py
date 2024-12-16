import streamlit as st
import pandas as pd

# Funções auxiliares
def calcular_depreciacao(idade, vida_util):
    """Calcula a depreciação do imóvel."""
    if vida_util <= 0:
        return 0.0  # Previne divisão por zero
    return min((idade / vida_util) * 100, 100)  # Limita a depreciação a 100%

# Tabela de coeficientes 'K' de depreciação de edificações
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


# Dicionário de estado de conservação
classificacao_imoveis = {
    "Novo": "A",
    "Entre novo e regular": "B",
    "Regular": "C",
    "Entre regular e reparos simples": "D",
    "Reparos simples": "E",
    "Entre reparos simples e importantes": "F",
    "Reparos importantes": "G",
    "Entre reparos importantes e sem valor": "H"
} 

descricao_imoveis = {
    "Novo": "Com até seis meses de uso e sem danos. Não sofreu nem necessita de reparos. Edificação nova ou com reforma geral e substancial, com menos de 02 anos, que apresente apenas sinais de desgaste natural da pintura externa",
    "Entre novo e regular": "Apesar de já submetido ao uso, apresenta-se nas condições de novo ou bem próximo disso. Não recebeu e nem necessita de reparos. Edificação nova ou com reforma geral e substancial, com menos de 02 anos, que apresente necessidade apenas de uma demão leve de pintura para recompor a sua aparência",
    "Regular": "Requer ou recebeu reparos pequenos. Quando o objeto de serviço de recuperação ou de restauração recente deixou em condições próximas ao de novo.  Quando da existência de atividade de manutenção permanente e eficiente que mantém a aparência e/ou uso em condições de novo; Requer apenas limpeza sem utilização de mão de obra especializada para manter em boas condições de uso/aparência. Edificação semi-nova ou com reforma geral e substancial entre 02 e 05 anos, cujo estado geral possa ser recuperado apenas com reparos de eventuais fissuras superficiais localizadas e/ou pintura externa e interna.",
    "Entre regular e reparos simples": "Atividade de manutenção eventual ou periódica que mantém uma boa aparência e condições normais de uso, mas sem o aspecto de novo ou recuperação recente. Requer intervenções superficiais em pontos localizados para recuperação de desgastes naturais.  Pode requerer mão de obra especializada com uso de instrumentos especiais. Edificação semi-nova ou com reforma geral e substancial entre 02 e 05 anos, cujo estado geral possa ser recuperado com reparo de fissuras localizadas e superficiais e pintura externa e interna.",
    "Reparos simples": "Requer reparações simples. Requer intervenções em pontos localizados ou em partes/componentes definidos para restauração de aspectos e/ou funcionalidades originais. Necessitam de serviços generalizados de manutenção e limpeza. Implicam a realização de serviços superficiais ou reparos de partes ou componentes definidos/localizados com mão de obra especializada. Não comprometem a operação e a funcionalidade. Edificação cujo estado geral possa ser recuperado com pintura interna e externa, após reparos de fissuras superficiais generalizadas, sem recuperação do sistema estrutural. Eventualmente, revisão do sistema hidráulico e elétrico.",
    "Entre reparos simples e importantes": "Requer intervenções generalizadas na maior parte ou com profundidades em peças ou componentes específicos sob pena de comprometimento iminente de operação e segurança. Implica restauração ou recuperação com remoção/ substituição/ adição de elementos ou peças com mão de obra especializada. Edificação cujo estado geral possa ser recuperado com pintura interna e externa, após reparos de fissuras, e com estabilização e/ou recuperação localizada do sistema estrutural. As instalações hidráulicas e elétricas possam ser restauradas mediante a revisão e com substituição eventual de algumas peças desgastadas naturalmente. Eventualmente possa ser necessária a substituição dos revestimentos de pisos e paredes, de um, ou de outro compartimento. Revisão da impermeabilização ou substituição de telhas da cobertura.",
    "Reparos importantes": "Requer reparações importantes. Requer intervenções generalizadas e com profundidade em partes ou peças críticas sob o aspecto de estética, salubridade, segurança e funcionalidade. Implica restauração ou recuperação com remoção/ substituição/ adição de elementos ou peças com mão de obra especializada. Edificação cujo estado geral possa ser recuperado com pintura interna e externa, com substituição de panos de regularização da alvenaria, reparos de fissuras, com estabilização e/ou recuperação de grande parte do sistema estrutura. As instalações hidráulicas e elétricas possam ser restauradas mediante a substituição das peças aparentes. A substituição dos revestimentos de pisos e paredes, da maioria dos compartimentos. Substituição ou reparações importantes na impermeabilização ou no telhado.",
    "Entre reparos importantes e sem valor": "Restauração total de elementos ou peças importantes. Degradação generalizada e com alto grau de exposição. Alto nível de comprometimento da funcionalidade, segurança e operação. Edificação cujo estado geral possa ser recuperado com estabilização e/ou recuperação do sistema estrutural, substituição da regularização da alvenaria, reparos de fissuras. Substituição das instalações hidráulicas e elétricas. Substituição dos revestimentos de pisos e paredes. Substituição da impermeabilização ou do telhado."
}


# Dicionário de vida útil dos imóveis estabelecido pelo Bureau of Internal Revenue Service (IRS)
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

# Dicionário de siglas
siglas = {
    'R-1': 'Residência Unifamiliar',
    'RP1Q': 'Residência Popular',
    'PP-4': 'Prédio Popular',
    'CAL-8': 'Comercial Andares Livres',
    'R-8': 'Residência Multifamiliar',
    'CSL-8': 'Comercial Salas e Lojas',
    'R-16': 'Residência Multifamiliar',
    'CSL-16': 'Comercial Salas e Lojas',
    'PIS': 'Projeto de Interesse Social',
    'GI': 'Galpão Industrial'
}

# Dicionário de referência
referencia = {
    'Projetos Residenciais': {
        'Padrão Baixo': ['R-1', 'PP-4', 'R-8', 'PIS'],
        'Padrão Normal': ['R-1', 'PP-4', 'R-8', 'R-16'],
        'Padrão Alto': ['R-1', 'R-8', 'R-16']
    },
    'Projetos Comerciais (CAL-Comercial Andares Livres e CSL-Comercial Salas e Lojas)': {
        'Padrão Normal': ['CAL-8', 'CSL-8', 'CSL-16'],
        'Padrão Alto': ['CAL-8', 'CSL-8', 'CSL-16']
    },
    'Projetos Galpão Industrial (GI) e Residência Popular (RP1Q)': ['RP1Q', 'GI']
}

# Interface do Streamlit
st.title('Parecer Técnico de Avaliação Mercadológica, PTAM')
st.write('Este aplicativo auxilia na avaliação de imóveis pelo método evolutivo.')

# Configurações no menu lateral
# Dados gerais
st.sidebar.title('Dados Gerais')
solicitante = st.sidebar.text_input('Solicitante', placeholder='Digite o nome do solicitante (obrigatório)', help='Este campo é obrigatório.')
proprietario = st.sidebar.text_input('Proprietário', placeholder='Informe o nome do proprietário')
matricula = st.sidebar.text_input('Matrícula', placeholder='Informe o número da matrícula')
endereco = st.sidebar.text_input('Endereço', placeholder='Digite o endereço completo')

# Características do imóvel
st.sidebar.title('Características do imóvel')
perimetro = st.sidebar.number_input('Perímetro Total (m)', value=0.0, step=0.01)
area_total = st.sidebar.number_input('Área Total (m²)', value=0.0, step=0.01)
area_construida_total = st.sidebar.number_input('Área Construída Total(m²)', value=0.0, step=0.01)

# Valor Imóvel Novo
st.sidebar.title('Valor do Imóvel Novo')
area_construída = st.sidebar.number_input('Área Construída (m²)', value=0.0, step=0.01)
area_equivalente = st.sidebar.number_input('Área Equivalente (%)', value=0.0, step=0.01)
custo_unitario = st.sidebar.number_input('Custo Unitário (R$/m²)', value=0.0, step=0.01)
bdi = st.sidebar.number_input('BDI (%)', value=10, step=1)
outros_custos = st.sidebar.number_input('Outros Custos (%)', value=5, step=1)
if area_equivalente > 0 and custo_unitario > 0:
    custo_bdi_outros = ((custo_unitario * (bdi + outros_custos) / 100) + custo_unitario)
    valor_novo = (custo_bdi_outros * ((area_construída * area_equivalente)/100))
    st.sidebar.write(f'Custos + BDI (R$): {custo_bdi_outros:.2f}')
    st.sidebar.write(f'Valor Novo (R$): {valor_novo:.2f}')
else:
    st.sidebar.write('Custo Equivalente (R$): -')
    st.sidebar.write('Valor Novo (R$): -')

# Projeto
st.sidebar.title('Referência')
categoria = st.sidebar.selectbox('Selecione uma categoria', referencia.keys())

# Verifica se a categoria tem subcategorias
if isinstance(referencia[categoria], dict):
    padrao = st.sidebar.selectbox('Selecione o Padrão do Projeto', list(referencia[categoria].keys()))
    valores = referencia[categoria][padrao]
    valor_selecionado = st.sidebar.selectbox('Selecione um valor do projeto', valores)
    st.sidebar.write('Você selecionou:', valor_selecionado)
else:
    valores = referencia[categoria]
    valor_selecionado = st.sidebar.selectbox('Selecione um valor do projeto', valores)
    st.sidebar.write('Você selecionou:', valor_selecionado)

# Função para obter a descrição da sigla
def obter_sigla_descricao(sigla, siglas_dict):
    return siglas_dict.get(sigla, 'Descrição não encontrada')

# Exibir sigla e descrição
if valor_selecionado:
    descricao = obter_sigla_descricao(valor_selecionado, siglas)
    st.sidebar.write(f'Descrição: {descricao}')

# Depreciação por Ross-Heidecke
st.sidebar.title('Depreciação por Ross-Heidecke')
idade = st.sidebar.number_input('Idade do Imóvel (anos)', value=0, step=1)
st.sidebar.title('Vida Útil dos Imóveis')
st.sidebar.write('por Bureau of Internal Revenue Service (IRS)')

tipo_imovel = st.sidebar.selectbox('Tipo de Imóvel', list(vida_util_imoveis.keys()))
subtipo_imovel = st.sidebar.selectbox('Subtipo de Imóvel', list(vida_util_imoveis[tipo_imovel].keys()))

if isinstance(vida_util_imoveis[tipo_imovel][subtipo_imovel], dict):
    subsubtipo_imovel = st.sidebar.selectbox('Subsubtipo de Imóvel', list(vida_util_imoveis[tipo_imovel][subtipo_imovel].keys()))
    vida_util = vida_util_imoveis[tipo_imovel][subtipo_imovel][subsubtipo_imovel]
else:
    vida_util = vida_util_imoveis[tipo_imovel][subtipo_imovel]

depreciacao = calcular_depreciacao(idade, vida_util)
st.sidebar.write(f'Vida Útil: {vida_util} anos')
st.sidebar.write(f'Tempo de Vida: {depreciacao:.0f}%')

st.sidebar.title('Estado de Conservação')
estado_conservacao = st.sidebar.selectbox('Selecione o Estado de Conservação', list(classificacao_imoveis.keys()))
st.sidebar.write(f'Classificação: {classificacao_imoveis[estado_conservacao]}')

# Coeficiente K
st.sidebar.title('Coeficiente k')

# Verificação e acesso ao valor
# Arredondar a depreciação para o valor mais próximo que existe no dicionário ir_vu
depreciacao_arredondada = round(depreciacao / 2) * 2

if depreciacao_arredondada in ir_vu:
    if classificacao_imoveis[estado_conservacao] in ir_vu[depreciacao_arredondada]:
        valor_k = ir_vu[depreciacao_arredondada][classificacao_imoveis[estado_conservacao]]
        st.sidebar.write(f"O valor para tempo de vida {depreciacao_arredondada} e classificação {estado_conservacao} é {valor_k:.2f}")
    else:
        st.sidebar.write(f"Classificação '{estado_conservacao}' não encontrada para o tempo de vida {depreciacao_arredondada}%.")
else:
    st.sidebar.write(f"Tempo de vida '{depreciacao_arredondada}' não encontrado no dicionário.")

# Depreciação Final e Valor Depreciado
st.sidebar.title('Depreciação %')
if 'valor_k' in locals():
    depreciacao_final = 100 - valor_k
    imovel_depreciado = valor_novo * (depreciacao_final / 100)
    st.sidebar.write(f'Depreciação Final: {depreciacao_final:.2f}%')
    st.sidebar.write(f'Valor do Imóvel Depreciado (R$): {imovel_depreciado:.2f}')
else:
    st.sidebar.write('Informações insuficientes para calcular a depreciação final.')




# Exibição do Parecer Técnico
st.title('Depreciação das construções')
st.write('Calculando a depreciação das amostras pelo Método de Ross-Heidecke, de acordo com a idade, vida útil e estado de conservação:')

# Botão extrair os dados das variáveis e criar as tabelas tabela_imovel_novo e tabela_depreciacao
if st.sidebar.button('Extrair Dados'):
    # Tabela imovel_novo com: Benfeitorias, Referência, Área, Custo Unitário, Custos + BDI, Valor Novo
    tabela_imovel_novo = pd.DataFrame({
        'Benfeitorias': [area_construída],
        'Referência': [valor_selecionado],
        'Área': [area_construída],
        'Custo Unitário': [custo_unitario],
        'Custos + BDI': [custo_bdi_outros],
        'Valor Novo': [valor_novo]
    })

    # Tabela depreciação com: Idade, Vida Útil, Estado de Conservação, Coeficiente K, Depreciação Final, Valor Depreciado
    tabela_depreciacao = pd.DataFrame({
        'Idade': [idade],
        'Vida Útil': [vida_util],
        'Vida Útil %': [depreciacao],
        'Estado de Conservação': [estado_conservacao],
        'Coeficiente K': [valor_k],
        'Depreciação Final': [depreciacao_final],
        'Valor Depreciado': [imovel_depreciado]
    })

    # Definindo o número de casas decimais
    casas_decimais = 2

    # Formatando as tabelas
    tabela_imovel_novo = tabela_imovel_novo.round(casas_decimais)
    tabela_depreciacao = tabela_depreciacao.round(casas_decimais)

    # Aplicando formatação brasileira
    def formatar_valor(x):
        if isinstance(x, (int, float)):
            return f'{x:,.{casas_decimais}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        return x

    # Formatando as tabelas
    tabela_imovel_novo = tabela_imovel_novo.map(formatar_valor)
    tabela_depreciacao = tabela_depreciacao.map(formatar_valor)

    # Exibindo as tabelas
    st.write('Tabela Imóvel Novo:')
    st.table(tabela_imovel_novo)

    st.write('Tabela Depreciação:')
    st.table(tabela_depreciacao)
    
    st.write(f'Classificação: {classificacao_imoveis[estado_conservacao]}')
    st.write(f'Descrição da classificação: {descricao_imoveis[estado_conservacao]}')
