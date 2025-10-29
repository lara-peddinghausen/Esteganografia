from esteganografia import *

if __name__ == "__main__":
    chave = None
    fernet = None

    # TENTATIVA DE CARREGAMENTO AUTOMÁTICO DA CHAVE AO INICIAR (Para o RECEPTOR)
    if os.path.exists("chave.key"):
        try:
            chave = carregar_chave()
            fernet = Fernet(chave)
            print("\n [INFO] Chave 'chave.key' carregada automaticamente.")
        except Exception:
            print("\n [ERRO] Chave existente não pôde ser carregada ou é inválida.")
    else:
        print("\n [INFO] Nenhuma chave 'chave.key' encontrada. Use a Opção 4 para gerar uma.")

    while True:
        print("\n==============================================")
        print("          MENU ESTEGANOGRAFIA LSB           ")
        print("==============================================")
        print("1. Ocultar Mensagem e Criptografar (Emissor)")
        print("2. Revelar e Descriptografar Mensagem (Receptor)")
        print("3. Executar Teste Qui-Quadrado (Esteganálise)")
        print("4. Gerar NOVA Chave (Cria/Substitui chave.key)")
        print("5. Sair")
        print("==============================================")

        opcao = input("\nEscolha uma opção: ").strip()

        # OPÇÃO 1: Ocultar Mensagem e Criptografar (Emissor)
        if opcao == "1":
            # REQUISITO: A chave deve existir
            if not fernet:
                print("\n [AVISO] É preciso carregar uma chave Fernet primeiro (Opção 4).")
                continue

            # caminho da imagem
            caminho_imagem = input("Caminho da imagem original (ex: abacaxi.png): ").strip()
            if not os.path.exists(caminho_imagem):
                print(" [ERRO] Imagem não encontrada.")
                continue

            # Gerar mensagem caso não seja preenchida completar
            mensagem = input("Mensagem a ser escondida (padrão: esteganografia): ").strip()
            if not mensagem:
                mensagem = "esteganografia"

            # Codificar e criptografar (Desafio Adicional 3a)
            mensagem_bytes = mensagem.encode()
            mensagem_criptografada = fernet.encrypt(mensagem_bytes)
            print("Mensagem criptografada (bytes):", mensagem_criptografada)

            # Converter para string Base64 e esconder
            mensagem_criptografada_str = base64.urlsafe_b64encode(mensagem_criptografada).decode("utf-8")

            # Exibir info da imagem original
            imagem = Image.open(caminho_imagem)
            print("Tamanho da imagem original:", os.path.getsize(caminho_imagem), "bytes")
            # imagem.show() # Descomente se quiser ver a imagem automaticamente

            # Esconder a mensagem (Tarefa 1)
            imagem_saida = "nova_imagem.png"
            esteganografia = lsb.hide(caminho_imagem, mensagem_criptografada_str)
            esteganografia.save(imagem_saida, optimize=False, compress_level=0)

            imagem_nova = Image.open(imagem_saida)
            print("Tamanho da imagem com mensagem:", os.path.getsize(imagem_saida), "bytes")
            # imagem_nova.show() # Descomente se quiser ver a imagem automaticamente

            print("\n [SUCESSO] Mensagem escondida com sucesso em 'nova_imagem.png'.")
            print(" Lembre-se de enviar 'chave.key' e 'nova_imagem.png' para o receptor.")


        # OPÇÃO 2: Revelar e descriptografar mensagem (Receptor)
        elif opcao == "2":
            # REQUISITO: A chave deve existir
            if not fernet:
                print("\n [AVISO] É preciso carregar a chave Fernet (Opção 4) para descriptografar.")
                continue

            imagem_estego = input("Caminho da imagem esteganografada (ex: nova_imagem.png): ").strip()
            if not os.path.exists(imagem_estego):
                print(" [ERRO] Imagem não encontrada.")
                continue

            # Extrair mensagem (Tarefa 2)
            revelar_mensagem_str = lsb.reveal(imagem_estego)
            if not revelar_mensagem_str:
                print(" [AVISO] Nenhuma mensagem encontrada (string vazia).")
                continue

            try:
                # Converter string Base64 para bytes
                mensagem_criptografada_bytes = base64.urlsafe_b64decode(revelar_mensagem_str.encode("utf-8"))

                # Descriptografar
                descriptografia = fernet.decrypt(mensagem_criptografada_bytes)
                print("\n [SUCESSO] Mensagem revelada:", descriptografia.decode("utf-8"))

            except Exception as e:
                print(
                    f"\n [ERRO] Falha ao descriptografar. A CHAVE PODE ESTAR ERRADA ou a mensagem corrompida. Detalhe: {e}")


        # OPÇÃO 3: Executar teste do Qui-Quadrado (Desafio Adicional 3b)
        elif opcao == "3":
            img_original = input("Caminho da imagem original limpa (ex: abacaxi.png): ").strip()
            img_estego = input("Caminho da imagem com mensagem (ex: nova_imagem.png): ").strip()

            if not os.path.exists(img_original) or not os.path.exists(img_estego):
                print(" [ERRO] Caminhos de imagem inválidos.")
                continue

            print("\n--- ANÁLISE DO QUI-QUADRADO ---")
            p_original = chi_square_test(img_original, num_canais=3, grupos=300)
            p_estego = chi_square_test(img_estego, num_canais=3, grupos=300)

            print(f"P-valor (Original):    {p_original:.4f} (Esperado: Alto ~1.0)")
            print(f"P-valor (Esteganograma): {p_estego:.4f} (Esperado: Baixo ~0.0)")

            if p_estego < 0.05:
                print("\n [DETECÇÃO] Esteganografia LSB DETECTADA com 95% de confiança!")
            else:
                print("\n [DETECÇÃO] Nenhuma esteganografia LSB detectada com alta confiança.")

        # OPÇÃO 4: Gerar NOVA Chave
        elif opcao == "4":
            print("\n [AVISO] Gerando NOVA chave Fernet. Isso irá sobrescrever 'chave.key'.")
            gerar_chave()
            chave = carregar_chave()
            fernet = Fernet(chave)
            print(" [SUCESSO] Nova chave gerada e salva em 'chave.key'.")
            print(" ATENÇÃO: Envie este arquivo 'chave.key' para o Receptor.")


        # OPÇÃO 5: Sair
        elif opcao == "5":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")