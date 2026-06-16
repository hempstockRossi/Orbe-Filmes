from db.conexao import get_conexao


def listar_assistidos():
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT a.id, a.data_assistido, f.id AS filme_id,
               f.titulo, f.diretor, f.ano_lancamento, f.genero
        FROM assistidos a
        JOIN filmes f ON f.id = a.filme_id
        ORDER BY a.data_assistido DESC
        """
    )
    return cursor.fetchall()


def inserir_assistido(filme_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO assistidos (filme_id) VALUES (%s)",
        (filme_id,),
    )
    conn.commit()
    return cursor.lastrowid


def deletar_assistido(id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assistidos WHERE id = %s", (id,))
    conn.commit()
