# Coding: utf-8
# Argumentos: SCRIPT-GEOCODE-HERE
# Autor: Rosner Henrique Alves Rodrigues
# Versão: script
# Criado usando PayCharm (Python 3.10)
#
# ----------------------------------------------------------------------------------------------------------------------
# ROTEIRO
# ----------------------------------------------------------------------------------------------------------------------
#
# 01 - Cadastrar na plataforma HERE (https://www.here.com/);
# 02 - Encontrar a API Key na plataforma HERE (https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/quick-start.html);
#       Acess Manege>APP>Regitre new APP> API KEI
# 03 - Pychram (https://www.jetbrains.com/pt-br/pycharm/download/#section=mac)
# 04 - Desenvolver o código de geocodificação;
# 05 - Rodar o código de geocodificação;
# 06 - Carregar os dados geocodificados em um softwares de Geoprocessamento;
#
# ----------------------------------------------------------------------------------------------------------------------
# BIBLIOTECAS
# ----------------------------------------------------------------------------------------------------------------------
#
import requests  # Usado para enviar uma solicitação GET para a API de geocodificação da Here.
import pandas as pd  # Usada para ler, manipular e salvar um arquivo CSV
from tkinter import Tk  # Usada para criar uma janela de diálogo para selecionar um arquivo.
from tkinter.filedialog import askopenfilename
from tqdm import tqdm  # Usada para fornece uma barra de progresso rápida e extensível para Python.
#
# ----------------------------------------------------------------------------------------------------------------------
# INPUTS DO HEREGEOCODE
# ----------------------------------------------------------------------------------------------------------------------
#
# Chave de API que você precisa para acessar a API de geocodificação da Here.
HERE_API_KEY = 'COLE SUA APY AQUI'
# Localização de partida que você deseja usar para a geocodificação.
START_LOCATION = '-8.060319,-34.902362'
#
# ----------------------------------------------------------------------------------------------------------------------
# FUNÇÕES
# ----------------------------------------------------------------------------------------------------------------------
#
# Essa função pega um endereço como entrada e retorna a localização (latitude e longitude).
def geocode(address):
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&at={START_LOCATION}&apiKey={HERE_API_KEY}"
    response = requests.get(url)  # Envia uma solicitação GET para a API e recebe a resposta.
    data = response.json()  # Resposta convertida de JSON para um dicionário Python.

    # Extrai o endereço e a localização do dicionário e retorna esses dados.
    items = data.get('items', [{}])
    if items:
        add = items[0]
    else:
        add = {}  # Ou qualquer outro valor padrão que faça sentido no seu caso.

    return {
        'address': add.get('address', ''),
        'location': add.get('position', {'lat': None, 'lng': None})
    }

# Essa função lê e processa um arquivo CSV.
def process_csv(file_name):
    try:
        df = pd.read_csv(file_name, sep=';', on_bad_lines='warn')

        # Cria as colunas de Latitude e Longitude se elas não existirem.
        if 'Latitude' not in df.columns:
            df['Latitude'] = None
        if 'Longitude' not in df.columns:
            df['Longitude'] = None

        # Exibe todas as colunas do DataFrame e permite que você escolha qual coluna deseja geocodificar.
        print('Colunas:')
        for i, column in enumerate(df.columns):
            print(f'{i + 1}. {column}')
        column_num = int(input('Digite o número da coluna que deseja geocodificar: ')) - 1
        column_name = df.columns[column_num]
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    # Passa por cada linha do DataFrame e preenche as colunas 'Latitude' e 'Longitude' se necessário.
    chunks = df[column_name]

    for idx in tqdm(chunks.index):  # Cria uma barra de carregamento do processo.
        address = chunks.loc[idx]
        if pd.isnull(df.at[idx, 'Latitude']) and pd.isnull(df.at[idx, 'Longitude']):
            result = geocode(address)

            df.at[idx, 'Latitude'] = result['location']['lat']
            df.at[idx, 'Longitude'] = result['location']['lng']

    # Altera o separador decimal para uma vírgula para as colunas 'Latitude' e 'Longitude'
    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].applymap(lambda x: str(x).replace('.', ','))

    # Salva o DataFrame atualizado de volta no CSV
    df.to_csv(file_name, index=False, sep=';')

#
# ----------------------------------------------------------------------------------------------------------------------
# PROCESSO
# ----------------------------------------------------------------------------------------------------------------------
#
# Abre uma janela de diálogo para escolher o arquivo a ser carregado
Tk().withdraw()  # Evita que a janela do tkinter seja mostrada;
filename = askopenfilename()  # Mostra uma janela de diálogo para abrir o arquivo;
process_csv(filename)  # Inicia a função process_csv no arquivo escolhido;


