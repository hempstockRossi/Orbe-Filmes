from db.conexao import get_conexao


def listar_filmes():
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM filmes ORDER BY titulo")
    return cursor.fetchall()


def buscar_filme(id):
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM filmes WHERE id = %s", (id,))
    return cursor.fetchone()


def inserir_filme(titulo, diretor, ano_lancamento, genero):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO filmes (titulo, diretor, ano_lancamento, genero) VALUES (%s, %s, %s, %s)",
        (titulo, diretor, ano_lancamento, genero),
    )
    conn.commit()
    return cursor.lastrowid


def atualizar_filme(id, titulo, diretor, ano_lancamento, genero):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE filmes SET titulo=%s, diretor=%s, ano_lancamento=%s, genero=%s WHERE id=%s",
        (titulo, diretor, ano_lancamento, genero, id),
    )
    conn.commit()


def deletar_filme(id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM filmes WHERE id = %s", (id,))
    conn.commit()
