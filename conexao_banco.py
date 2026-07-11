import os

import mysql.connector
from mysql.connector import Error


def conectar_banco():
    """Conecta ao MySQL quando as variáveis DB_* estão configuradas."""
    host = os.getenv("DB_HOST")
    if not host:
        return None

    try:
        conexao = mysql.connector.connect(
            host=host,
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME", "ATELIE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        if conexao.is_connected():
            return conexao
    except Error as erro:
        print(f"-> Erro ao conectar ao MySQL: {erro}")
        return None

    return None
