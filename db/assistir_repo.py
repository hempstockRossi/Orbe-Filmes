from db.conexao import get_conexao


def listar_assistir():
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT a.id, f.id AS filme_id,
               f.titulo, f.diretor, f.ano_lancamento, f.genero
        FROM assistir a
        JOIN filmes f ON f.id = a.filme_id
        ORDER BY a.data_assistido ASC
        """
    )
    return cursor.fetchall()


def inserir_assistir(filme_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO assistir (filme_id, data_assistido) VALUES (%s, NOW())",
        (filme_id,),
    )
    conn.commit()
    return cursor.lastrowid


def marcar_assistido(assistir_id, filme_id):
    from db.assistidos_repo import inserir_assistido
    inserir_assistido(filme_id)
    deletar_assistir(assistir_id)


def deletar_assistir(id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assistir WHERE id = %s", (id,))
    conn.commit()


def is_na_lista(filme_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM assistir WHERE filme_id = %s", (filme_id,))
    return cursor.fetchone() is not None
