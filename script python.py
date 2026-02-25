print("\n--- Bem Vindo ao Ateliê Balão Mágico ---")
class Cliente:
    def __init__(self, nome, telefone,email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.historico_de_compras = [] 
        self.datas_de_aniversarios = []

class Pedido:
    def __init__(self, cliente, data_festa, data_entrega):
        self.cliente = cliente
        self.data_festa = data_festa
        self.data_entrega = data_entrega
        self.status = "Orçamento" 
        
        self.tema = ""
        self.cores = ""
        self.nome_do_aniversariante = ""
        self.idade = None
        self.tamanho_do_bolo = ""

    def definir_personalizacao(self, tema, cores, nome, idade, tamanho):
        """Preenche os dados de personalização da festa"""
        self.tema = tema
        self.cores = cores
        self.nome_do_aniversariante = nome
        self.idade = idade
        self.tamanho_do_bolo = tamanho

    def exibir_info(self):
        print(f"\n--- Resumo do Pedido ---")
        print(f"Cliente: {self.cliente.nome} | telefone: {self.cliente.telefone} | email: {self.email}")
        print(f"Tema: {self.tema}")
        print(f"Cores: {self.cores}")
        print(f"Nome do Aniversariante: {self.nome_do_aniversariante}")
        print(f"Idade: {self.idade}")
        print(f"Tamanho do bolo: {self.tamanho_do_bolo}")
        print(f"Status atual: {self.status}")
        print("------------------------\n")



lista_clientes = []
lista_pedidos = []
lista_histórico = []

while True:
    print("\n--- Menu do Ateliê ---")
    print("1 - Cadastrar Dados Pessoais do Cliente")
    print("2 - Iniciar Novo Pedido (Festa e Entrega)")
    print("3 - Personalizar Pedido (Tema, Cores, etc)")
    print("4 - Consultar Histórico")
    print("5 - Sair")

    escolha = input("Escolha uma Opção: ")

    if escolha == "1":
        print("\n--- 1. Cadastro de Cliente ---")
        nome = input("Digite o Nome do cliente: ")
        telefone = input("Insira o Telefone (WhatsApp): ")
        email = input("Insira o Email: ")
        
        novo_cliente = Cliente(nome, telefone)
        lista_clientes.append(novo_cliente)
        print(f"-> Cliente {nome} cadastrado com sucesso!")

       
        avancar_pedido = input(f"\nDeseja já iniciar o pedido para {nome}? (S/N): ").strip().upper()

            
        
        if avancar_pedido == "S":
            print("\n--- 2. Dados do Pedido ---")
            data_festa = input("Qual a data da festa? ")
            data_entrega = input("Qual a data de entrega no ateliê? ")
            
            novo_pedido = Pedido(novo_cliente, data_festa, data_entrega)
            lista_pedidos.append(novo_pedido)
            print("-> Pedido iniciado com sucesso! Status: Orçamento.")

            
            avancar_personalizacao = input("\nDeseja preencher os detalhes do topo/artigo agora? (S/N): ").strip().upper()
            
            if avancar_personalizacao == "S":
                print("\n--- 3. Personalização ---")
                tema = input("Tema da festa: ")
                cores = input("Cores principais: ")
                nome_aniv = input("Nome do aniversariante: ")
                idade = input("Idade: ")
                tamanho = input("Tamanho/Aro do bolo: ")
                
                novo_pedido.definir_personalizacao(tema, cores, nome_aniv, idade, tamanho)
                print("\n-> Tudo pronto! Aqui está o resumo final do seu novo pedido:")
                novo_pedido.exibir_info()
            else:
                print("-> Sem problemas, você pode personalizar esse pedido depois.")
        else:
            print("-> Ok, cliente cadastrado sem pedido por enquanto.")

    elif escolha == "4":
        print("\n--- Histórico de Pedidos ---")
        if not lista_pedidos:
            print("Nenhum pedido foi cadastrado ainda no ateliê.")
        else:
            for indice, pedido in enumerate(lista_pedidos, start=1):
                print(f"\n[ Pedido #{indice} ]")
                pedido.exibir_info()
                
    elif escolha == "5":
        sair = input("\nDeseja realmente sair do sistema? (S/N): ").strip().upper
        break
        
    else:
        print("-> Opção inválida. Tente novamente.")