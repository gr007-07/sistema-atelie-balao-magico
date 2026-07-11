from pedido_models import Cliente, Pedido


print("\n--- Bem Vindo à Criativa ---")


def main():
    lista_clientes = []
    lista_pedidos = []

    while True:
        print("\n--- Menu da Criativa ---")
        print("1 - Cadastrar Dados Pessoais do Cliente")
        print("2 - Iniciar Novo Pedido (Festa e Entrega)")
        print("3 - Personalizar Pedido (Tema, Cores, etc)")
        print("4 - Consultar Histórico")
        print("5 - Sair")

        escolha = input("Escolha uma Opção: ")

        if escolha == "1":
            print("\n--- 1. Cadastro de Cliente ---")
            nome = input("Digite o Nome do cliente: ").strip()
            telefone = input("Insira o Telefone (WhatsApp): ").strip()
            email = input("Insira o Email: ").strip()

            novo_cliente = Cliente(nome, telefone, email)
            lista_clientes.append(novo_cliente)
            print(f"-> Cliente {nome} cadastrado com sucesso!")

            avancar_pedido = input(f"\nDeseja já iniciar o pedido para {nome}? (S/N): ").strip().upper()
            if avancar_pedido == "S":
                print("\n--- 2. Dados do Pedido ---")
                data_festa = input("Qual a data da festa? ").strip()
                data_entrega = input("Qual a data de entrega na Criativa? ").strip()

                novo_pedido = Pedido(novo_cliente, data_festa, data_entrega)
                lista_pedidos.append(novo_pedido)
                print("-> Pedido iniciado com sucesso! Status: Orçamento.")

                avancar_personalizacao = input("\nDeseja preencher os detalhes do pedido agora? (S/N): ").strip().upper()
                if avancar_personalizacao == "S":
                    print("\n--- 3. Personalização ---")
                    tema = input("Tema da festa: ").strip()
                    cores = input("Cores principais: ").strip()
                    nome_aniv = input("Nome do aniversariante: ").strip()
                    idade = int(input("Idade: ").strip())
                    tamanho = input("Tamanho/Aro do bolo: ").strip()
                    novo_pedido.definir_personalizacao(tema, cores, nome_aniv, idade, tamanho)

                    fotos = input("Deseja anexar fotos como exemplo? Digite os caminhos separados por vírgula: ").strip()
                    if fotos:
                        for caminho in fotos.split(","):
                            novo_pedido.anexar_foto_exemplo(caminho)

                    print("\n-> Tudo pronto! Aqui está o resumo final do seu novo pedido:")
                    novo_pedido.exibir_info()
                else:
                    print("-> Sem problemas, você pode personalizar esse pedido depois.")
            else:
                print("-> Ok, cliente cadastrado sem pedido por enquanto.")

        elif escolha == "4":
            print("\n--- Histórico de Pedidos ---")
            if not lista_pedidos:
                print("Nenhum pedido foi cadastrado ainda na Criativa.")
            else:
                for indice, pedido in enumerate(lista_pedidos, start=1):
                    print(f"\n[ Pedido #{indice} ]")
                    pedido.exibir_info()

        elif escolha == "5":
            sair = input("\nDeseja realmente sair do sistema? (S/N): ").strip().upper()
            if sair == "S":
                break

        else:
            print("-> Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()