import base64
import os
from cryptography.fernet import Fernet
from PIL import Image
from stegano import lsb
from scipy.stats import chi2
import numpy as np

# Função para teste do Qui-Quadrado: detectar esteganografia LSB em imagem.
def chi_square_test(caminho_imagem, num_canais=3, grupos=1000):
    # Pra maioria das imagens grupo com valor entre 1000 e 5000 é adequado
    try:
        img = Image.open(caminho_imagem).convert("RGB")
    except FileNotFoundError:
        print(f"Erro: Imagem não encontrada em {caminho_imagem}")
        return 1.0  # Retorna valor seguro

    # Converter a imagem para um array numpy para manipulação de pixels
    pixels = np.array(img)
    # nivela o array para ter uma lista simples de valores de pixel e selecionar só os canais que serão analisados
    if num_canais == 3:  # Analisa os 3 canais (R, G, B)
        pixel_data = pixels.flatten()
    elif num_canais == 1:  # Analisa apenas o primeiro canal (Grayscale/Vermelho)
        pixel_data = pixels[:, :, 0].flatten()
    else:
        print("Erro: num_canais deve ser 1 ou 3.")
        return 1.0

    N = len(pixel_data)
    if N == 0:
        return 1.0

    tamanho_grupo = N // grupos  # Determinar o tamanho de cada intervalo (grupo)
    if tamanho_grupo < 2:
        print("A imagem é muito pequena para a análise com tantos grupos.")
        return 1.0

    chi_square_sum = 0  # Variáveis para armazenar o valor total do qui-quadrado
    graus_liberdade = grupos  # Cada grupo (intervalo) é um grau de liberdade

    for i in range(grupos):  # 1º Iterar sobre os grupos de pixels
        start = i * tamanho_grupo
        end = start + tamanho_grupo
        grupo = pixel_data[start:end]

        C0 = np.sum(
            grupo % 2 == 0)  # 2º Contar as frequências de pixels Pares (C0) e Ímpares (C1) o valor do LSB é 0 se o valor do pixel for par (pixel % 2 == 0)
        C1 = np.sum(grupo % 2 != 0)

        # 3º Calcular o valor Qui-Quadrado para o grupo. A frequência esperada (E) de pares/ímpares em uma imagem esteganografada (onde a mensagem é ~50% 0s e 50% 1s) é (C0 + C1) / 2
        E = (C0 + C1) / 2.0

        # O Teste do Qui-Quadrado usa a fórmula: (Observado - Esperado) ao quadrado / Esperado
        if E > 0:
            chi_square_sum += ((C0 - E) ** 2 / E) + ((C1 - E) ** 2 / E)

    # 4. Calcular o P-value
    # O P-value é a probabilidade de obter um valor chi-quadrado
    # igual ou mais extremo, assumindo que a hipótese nula (sem esteganografia) é verdadeira.
    # O p-value baixo indica que a distribuição observada é muito improvável de ocorrer por acaso.
    p_value = chi2.sf(chi_square_sum, graus_liberdade)

    return p_value

#Funções da criptografia
def gerar_chave():

    chave = Fernet.generate_key()
    with open("chave.key", "wb") as arquivo_chave:
        arquivo_chave.write(chave)
def carregar_chave():
    return open("chave.key", "rb").read()


