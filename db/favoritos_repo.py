from db.conexao import get_conexao


def listar_favoritos():
    conn = get_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT f.id, f.titulo, f.diretor, f.ano_lancamento, f.genero, fav.data_favorito
        FROM favoritos fav
        JOIN filmes f ON f.id = fav.filme_id
        ORDER BY fav.data_favorito DESC
        """
    )
    return cursor.fetchall()


def adicionar_favorito(filme_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT IGNORE INTO favoritos (filme_id) VALUES (%s)",
        (filme_id,),
    )
    conn.commit()


def remover_favorito(filme_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favoritos WHERE filme_id = %s", (filme_id,))
    conn.commit()


def is_favorito(filme_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favoritos WHERE filme_id = %s", (filme_id,))
    return cursor.fetchone() is not None
