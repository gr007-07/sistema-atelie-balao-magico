import os
import mysql.connector
from mysql.connector import Error


def conectar_banco():
    """Tenta estabelecer a conexão com o MySQL e retorna o objeto de conexão."""
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "ATELIE"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "12345678"),
            port=int(os.getenv("DB_PORT", "3306")),
        )

        if conexao.is_connected():
            return conexao
    except Error as erro:
        print(f"-> Erro ao conectar ao MySQL: {erro}")
        return None

    return None