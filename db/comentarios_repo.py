from db.conexao import get_conexao


def listar_comentarios():
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.id, f.titulo, c.texto_comentario, c.data_assistido,
               c.data_comentario, c.hora_comentario, c.nota
        FROM comentarios c
        JOIN filmes f ON f.id = c.filme_id
        ORDER BY c.data_comentario DESC
        """
    )
    return cursor.fetchall()


def buscar_comentarios_do_filme(filme_id):
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM comentarios WHERE filme_id = %s ORDER BY data_comentario DESC",
        (filme_id,),
    )
    return cursor.fetchall()


def inserir_comentario(filme_id, texto_comentario, data_assistido, nota, hora_comentario=None):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO comentarios (filme_id, texto_comentario, data_assistido, nota, hora_comentario)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (filme_id, texto_comentario, data_assistido, nota, hora_comentario),
    )
    conn.commit()
    return cursor.lastrowid


def deletar_comentario(id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comentarios WHERE id = %s", (id,))
    conn.commit()
