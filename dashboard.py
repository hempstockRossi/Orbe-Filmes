import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect
)

from tela_base import TelaBase


class CartaoClicavel(QFrame):
    """QFrame que emite sinal ao ser clicado."""
    clicado = Signal()

    def mousePressEvent(self, evento):
        self.clicado.emit()
        super().mousePressEvent(evento)

    def enterEvent(self, evento):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(evento)

    def leaveEvent(self, evento):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(evento)


class Dashboard(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Dashboard", largura=900, altura=600)
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titulo = QLabel("ORBE-FILMES")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        efeito_titulo = QGraphicsDropShadowEffect()
        efeito_titulo.setBlurRadius(30)
        efeito_titulo.setColor(QColor(63, 114, 175, 200))
        efeito_titulo.setOffset(0, 0)
        titulo.setGraphicsEffect(efeito_titulo)

        layout.addWidget(titulo)
        layout.addSpacing(40)

        area_cards = QHBoxLayout()
        area_cards.setSpacing(25)

        dados = [
            ("FILMES",       "Catálogo de filmes"),
            ("FAVORITOS",    "Sua lista salva"),
            ("COMENTÁRIOS",  "Suas avaliações"),
        ]

        for nome, descricao in dados:
            card = CartaoClicavel()
            card.setObjectName("card")
            card.setFixedSize(200, 130)

            card_layout = QVBoxLayout(card)

            card_titulo = QLabel(nome)
            card_titulo.setObjectName("cardTitulo")

            card_texto = QLabel(descricao)
            card_texto.setObjectName("cardTexto")

            card_layout.addWidget(card_titulo)
            card_layout.addWidget(card_texto)

            card.clicado.connect(lambda tela=nome: self._abrir_tela(tela))
            area_cards.addWidget(card)

        layout.addLayout(area_cards)

        self._carregar_estilo("dashboard.qss")

    def _abrir_tela(self, nome):
        if nome == "FILMES":
            from filmes import Filmes
            self._proxima_tela = Filmes()
        elif nome == "FAVORITOS":
            from favoritos import Favoritos
            self._proxima_tela = Favoritos()
        elif nome == "COMENTÁRIOS":
            from comentarios import Comentarios
            self._proxima_tela = Comentarios()
        self._proxima_tela.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Dashboard()
    janela.show()
    sys.exit(app.exec())
