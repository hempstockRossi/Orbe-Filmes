from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
)

from ui.tela_base import TelaBase


class Home(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Filmes", largura=600, altura=500)
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QLabel("ORBE-FILMES")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        efeito_logo = QGraphicsDropShadowEffect()
        efeito_logo.setBlurRadius(30)
        efeito_logo.setColor(QColor(63, 114, 175, 200))
        efeito_logo.setOffset(0, 0)
        logo.setGraphicsEffect(efeito_logo)

        self._botao = QPushButton("Entrar")
        self._botao.setObjectName("botao")
        self._botao.setFixedSize(180, 50)
        self._botao.installEventFilter(self)
        self._botao.clicked.connect(self._abrir_dashboard)

        layout.addWidget(logo)
        layout.addSpacing(30)
        layout.addWidget(self._botao, alignment=Qt.AlignmentFlag.AlignCenter)

        self._carregar_estilo("home.qss")

    def _abrir_dashboard(self):
        from ui.dashboard import Dashboard
        self._proxima_tela = Dashboard()
        self._proxima_tela.show()
        self.close()

    def eventFilter(self, obj, evento):
        if obj is self._botao:
            if evento.type() == QEvent.Type.Enter:
                brilho = QGraphicsDropShadowEffect()
                brilho.setBlurRadius(25)
                brilho.setColor(QColor(63, 114, 175, 200))
                brilho.setOffset(0, 0)
                self._botao.setGraphicsEffect(brilho)
            elif evento.type() == QEvent.Type.Leave:
                self._botao.setGraphicsEffect(None)
        return super().eventFilter(obj, evento)
