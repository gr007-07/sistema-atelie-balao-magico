import mysql.connector
from mysql.connector import Error


def conectar_banco():
    """Tenta estabelecer a conexão com o MySQL e retorna o objeto de conexão."""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            database="ATELIE",
            user="root",
            password="12345678",
        )

        if conexao.is_connected():
            return conexao
    except Error as erro:
        print(f"-> Erro ao conectar ao MySQL: {erro}")
        return None

    return None