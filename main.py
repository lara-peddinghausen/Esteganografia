from esteganografia import *

if __name__ == "__main__":
    chave = None
    fernet = None
    mensagem_criptografada_str = None

    while True:
        print("\n MENU ")
        print("1. Gerar e carregar chave e Criptografar mensagem e esconder na imagem")
        print("2. Revelar e descriptografar mensagem")
        print("3. Executar teste Qui-Quadrado")
        print("4. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        # OPÇÃO 1: Gerar e carregar chave Criptografar mensagem e esconder

        if opcao == "1":
            gerar_chave()
            chave = carregar_chave()
            if chave:
                fernet = Fernet(chave)
                print("Chave carregada e pronta para uso.")

            # caminho da imagem
            caminho_imagem = input("Caminho da imagem (ex: abacaxi.png): ").strip()
            if not os.path.exists(caminho_imagem):
                print("Imagem não encontrada.")

            # Gerar mensagem caso não seja preenchida completar
            mensagem = input("Mensagem a ser escondida (padrão: esteganografia): ").strip()
            if not mensagem:
                mensagem = "esteganografia"

            # Codificar e criptografar
            mensagem_bytes = mensagem.encode()
            mensagem_criptografada = fernet.encrypt(mensagem_bytes)
            print("Mensagem criptografada (bytes):", mensagem_criptografada)

            # Converter para string Base64
            mensagem_criptografada_str = base64.urlsafe_b64encode(mensagem_criptografada).decode("utf-8")

            # Exibir info da imagem original
            imagem = Image.open(caminho_imagem)
            print("Tamanho da imagem original:", os.path.getsize(caminho_imagem), "bytes")
            imagem.show()

            # Esconder a mensagem
            imagem_saida = "nova_imagem.png"
            esteganografia = lsb.hide(caminho_imagem, mensagem_criptografada_str)
            esteganografia.save(imagem_saida, optimize=False, compress_level=0)

            imagem_nova = Image.open(imagem_saida)
            print("Tamanho da imagem com mensagem:", os.path.getsize(imagem_saida), "bytes")
            imagem_nova.show()

            print("Mensagem escondida com sucesso em 'nova_imagem.png'.")


        # OPÇÃO 2: Revelar e descriptografar mensagem

        elif opcao == "2":
            if not fernet:
                print("Gere e carregue uma chave primeiro.")
                continue

            imagem_estego = input("Caminho da imagem esteganografada (ex: nova_imagem.png): ").strip()
            if not os.path.exists(imagem_estego):
                print("Imagem não encontrada.")
                continue

            revelar_mensagem_str = lsb.reveal(imagem_estego)
            if not revelar_mensagem_str:
                print("Nenhuma mensagem encontrada.")
                continue

            # Converter string Base64 para bytes
            mensagem_criptografada_bytes = base64.urlsafe_b64decode(revelar_mensagem_str.encode("utf-8"))

            # Descriptografar
            descriptografia = fernet.decrypt(mensagem_criptografada_bytes)
            print("Mensagem revelada:", descriptografia.decode("utf-8"))


        # OPÇÃO 3: Executar teste do Qui-Quadrado

        elif opcao == "3":
            img_original = input("Caminho da imagem original (ex: abacaxi.png): ").strip()
            img_estego = input("Caminho da imagem com mensagem (ex: nova_imagem.png): ").strip()

            if not os.path.exists(img_original) or not os.path.exists(img_estego):
                print("Caminhos inválidos.")
                continue

            print("\n ANÁLISE DO QUI-QUADRADO")
            p_original = chi_square_test(img_original, grupos=2500)
            p_estego = chi_square_test(img_estego, grupos=2500)

            print(f"P-valor (Original): {p_original:.4f}")
            print(f"P-valor (Esteganograma): {p_estego:.4f}")

            if p_estego < 0.05:
                print("\n Esteganografia DETECTADA (P < 0.05)")
            else:
                print("\n Nenhuma esteganografia detectada.")

            print("\n--- NOTA ---")
            print("P-value alto (~1): imagem limpa.")
            print("P-value baixo (~0): provável esteganografia.")


        # OPÇÃO 4: Sair

        elif opcao == "4":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")