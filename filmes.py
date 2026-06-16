import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout
)

from tela_base import TelaBase


class Filmes(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Filmes")
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)

        # Cabeçalho
        cabecalho = QHBoxLayout()

        botao_voltar = QPushButton("← Voltar")
        botao_voltar.setObjectName("botaoVoltar")
        botao_voltar.clicked.connect(self._voltar)

        titulo = QLabel("FILMES")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cabecalho.addWidget(botao_voltar)
        cabecalho.addStretch()
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()

        layout.addLayout(cabecalho)
        layout.addStretch()

        self._carregar_estilo("filmes.qss")

    def _voltar(self):
        from dashboard import Dashboard
        self._proxima_tela = Dashboard()
        self._proxima_tela.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Filmes()
    janela.show()
    sys.exit(app.exec())
