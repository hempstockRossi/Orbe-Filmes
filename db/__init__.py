from db.conexao import get_conexao, fechar_conexao
from db.filmes_repo import (
    listar_filmes,
    buscar_filme,
    inserir_filme,
    atualizar_filme,
    deletar_filme,
)
from db.favoritos_repo import (
    listar_favoritos,
    adicionar_favorito,
    remover_favorito,
    is_favorito,
)
from db.comentarios_repo import (
    listar_comentarios,
    buscar_comentarios_do_filme,
    inserir_comentario,
    deletar_comentario,
)
from db.assistir_repo import (
    listar_assistir,
    inserir_assistir,
    marcar_assistido,
    deletar_assistir,
    is_na_lista,
)
from db.assistidos_repo import (
    listar_assistidos,
    inserir_assistido,
    deletar_assistido,
)
