import base64
import os
from cryptography.fernet import Fernet
from PIL import Image
from stegano import lsb

#Funções da criptografia
def gerar_chave():

    chave = Fernet.generate_key()
    with open("chave.key", "wb") as arquivo_chave:
        arquivo_chave.write(chave)
def carregar_chave():
    return open("chave.key", "rb").read()


if __name__ == '__main__':
    gerar_chave()
    chave = carregar_chave()

    #Codifica a mensagem usando o codec UTF-8
    mensagem = "esteganografia".encode()

    #Cria o objeto Fernet que permite criptografar e descriptografar
    fernet = Fernet(chave)

    #Criptografa a mensagem em bytes
    mensagem_criptografada = fernet.encrypt(mensagem)
    print(mensagem_criptografada)

    #Converte criptografia para string
    mensagem_criptografada_str = base64.urlsafe_b64encode(mensagem_criptografada).decode('utf-8')

    imagem = Image.open("abacaxi.png")
    print("Tamanho da imagem original: ", os.path.getsize("abacaxi.png"))
    imagem.show()

    #coloca a mensagem dentro da imagem
    estaganografia = lsb.hide("./abacaxi.png", mensagem_criptografada_str)
    estaganografia.save("./nova_imagem.png", optimize=False, compress_level=0)

    imagem_nova = Image.open("nova_imagem.png")
    print("Tamanho da imagem com a mensagem: ", os.path.getsize("nova_imagem.png"))
    imagem_nova.show()

    #Pega a mensagem dentro da imagem
    revelar_mensagem = lsb.reveal("./nova_imagem.png")

    #Converte de volta para bytes
    mensagem_criptografada_bytes = base64.urlsafe_b64decode(mensagem_criptografada_str.encode('utf-8'))

    #Descriptografa mensagem
    descriptografia = fernet.decrypt(mensagem_criptografada_bytes)
    print("Mensagem: ", descriptografia)