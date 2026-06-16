from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QFrame,
)

from ui.tela_base import TelaBase
from ui.botao import BotaoOrbe
import db


class _CardFavorito(QFrame):
    def __init__(self, filme, ao_remover):
        super().__init__()
        self._filme = filme
        self._ao_remover = ao_remover
        self._montar()

    def _montar(self):
        self.setObjectName("cardFilme")
        self.setFixedHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 16, 0)
        layout.setSpacing(10)

        col_info = QVBoxLayout()
        col_info.setSpacing(4)

        lbl_titulo = QLabel(self._filme["titulo"])
        lbl_titulo.setObjectName("cardFilmeTitulo")

        lbl_detalhe = QLabel(
            f"{self._filme['diretor']}  ·  {self._filme['ano_lancamento']}  ·  {self._filme['genero']}"
        )
        lbl_detalhe.setObjectName("cardFilmeDetalhe")

        col_info.addWidget(lbl_titulo)
        col_info.addWidget(lbl_detalhe)

        btn_remover = BotaoOrbe("♥")
        btn_remover.setObjectName("botaoCoracao")
        btn_remover.setFixedSize(40, 40)
        btn_remover.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_remover.setToolTip("Remover dos favoritos")
        btn_remover.setStyleSheet(
            "QPushButton { color: #E74C3C; font-size: 22px; background: transparent; border: none; }"
            "QPushButton:hover { color: rgba(231,76,60,160); }"
        )
        btn_remover.clicked.connect(self._remover)

        layout.addLayout(col_info)
        layout.addStretch()
        layout.addWidget(btn_remover)

    def _remover(self):
        db.remover_favorito(self._filme["id"])
        self._ao_remover()


class Favoritos(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Favoritos")
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(14)

        cabecalho = QHBoxLayout()
        btn_voltar = BotaoOrbe("← Voltar")
        btn_voltar.setObjectName("botaoVoltar")
        btn_voltar.clicked.connect(self._voltar)

        titulo = QLabel("FAVORITOS")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cabecalho.addWidget(btn_voltar)
        cabecalho.addStretch()
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setObjectName("scrollArea")
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._container = QWidget()
        self._container.setObjectName("scrollContainer")
        self._lista_layout = QVBoxLayout(self._container)
        self._lista_layout.setSpacing(10)
        self._lista_layout.setContentsMargins(2, 2, 10, 2)
        self._lista_layout.addStretch()

        self._scroll.setWidget(self._container)

        layout.addLayout(cabecalho)
        layout.addWidget(self._scroll)

        self._carregar_estilo("favoritos.qss")
        self._carregar_favoritos()

    def _carregar_favoritos(self):
        while self._lista_layout.count() > 1:
            item = self._lista_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        favoritos = db.listar_favoritos()

        if not favoritos:
            lbl = QLabel("Nenhum favorito ainda.\nFavorite filmes com o ♥ na tela de Filmes.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: rgba(255,255,255,45); font-size: 14px; padding: 20px;")
            self._lista_layout.insertWidget(0, lbl)
        else:
            for filme in favoritos:
                card = _CardFavorito(filme, self._carregar_favoritos)
                self._lista_layout.insertWidget(self._lista_layout.count() - 1, card)

    def _voltar(self):
        from ui.dashboard import Dashboard
        self._proxima_tela = Dashboard()
        self._proxima_tela.show()
        self.close()
