import mysql.connector
from mysql.connector import Error

def conectar_banco():
    """Tenta estabelecer a conexão com o MySQL e retorna o objeto de conexão."""
    try:
        conexao = mysql.connector.connect(
            host='localhost',          # Onde o banco está rodando (geralmente localhost)
            database='ATELIE',         # O nome exato do banco que você criou
            user='root',               # Seu usuário do MySQL (padrão é root)
            password='12345678'  # Substitua pela sua senha do MySQL
        )
        
        if conexao.is_connected():
            print("-> Conexão ao MySQL estabelecida com sucesso!")
            return conexao

    except Error as erro:
        print(f"-> Erro ao conectar ao MySQL: {erro}")
        return None

# --- Testando a Conexão e Inserindo um Dado ---
# 1. Abre a conexão
minha_conexao = conectar_banco()

if minha_conexao:
    # O cursor é o "mensageiro" que leva o SQL do Python para o Banco
    cursor = minha_conexao.cursor()
    
    # 2. Comando SQL de Inserção (CRUD - Create)
    sql_inserir = "INSERT INTO CLIENTES (NOME, EMAIL) VALUES (%s, %s)"
    dados_cliente = ("João Silva", "joao.silva@email.com")
    
    try:
        # Executa a inserção e confirma (commit) a gravação no banco
        cursor.execute(sql_inserir, dados_cliente)
        minha_conexao.commit()
        print(f"-> Cliente inserido com sucesso! ID gerado: {cursor.lastrowid}")
        
        # 3. Comando SQL de Busca (CRUD - Read)
        cursor.execute("SELECT * FROM CLIENTES")
        clientes_cadastrados = cursor.fetchall()
        
        print("\n--- Lista de Clientes no Banco ---")
        for cliente in clientes_cadastrados:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]} | E-mail: {cliente[2]}")
            
    except Error as erro:
        print(f"-> Erro ao executar comando no banco: {erro}")
        
    finally:
        # 4. É boa prática sempre fechar o cursor e a conexão no final
        if minha_conexao.is_connected():
            cursor.close()
            minha_conexao.close()
            print("\n-> Conexão com o MySQL encerrada.")