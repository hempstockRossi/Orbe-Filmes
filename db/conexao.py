import mysql.connector
from mysql.connector import Error

_conexao = None

HOST = "127.0.0.1"
PORT = 3306
DATABASE = "orbefilmes"
USER = "root"
PASSWORD = "3570"


def get_conexao():
    global _conexao
    try:
        if _conexao is None or not _conexao.is_connected():
            _conexao = mysql.connector.connect(
                host=HOST,
                port=PORT,
                database=DATABASE,
                user=USER,
                password=PASSWORD,
            )
    except Error as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")
    return _conexao


def fechar_conexao():
    global _conexao
    if _conexao and _conexao.is_connected():
        _conexao.close()
        _conexao = None
