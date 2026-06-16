import random
import math
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QBrush, QFontDatabase
from PySide6.QtWidgets import QWidget

_RAIZ = Path(__file__).parent.parent
_STYLES = _RAIZ / "assets" / "styles"
_FONTS = _RAIZ / "assets" / "fonts"


class TelaBase(QWidget):
    """Fundo animado com estrelas e gradiente — herdado por todas as telas."""

    def __init__(self, titulo_janela, largura=900, altura=600):
        super().__init__()
        self.setWindowTitle(titulo_janela)
        self.resize(largura, altura)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

        self._carregar_fontes()

        self._tempo = 0.0
        self._estrelas = self._criar_estrelas()

        self._temporizador = QTimer(self)
        self._temporizador.timeout.connect(self._pulso)
        self._temporizador.start(30)

    def _carregar_fontes(self):
        for fonte in ["Orbitron.ttf", "Outfit.ttf"]:
            caminho = _FONTS / fonte
            if caminho.exists():
                QFontDatabase.addApplicationFont(str(caminho))

    def _carregar_estilo(self, arquivo_qss):
        estilo = ""
        for nome in ["base.qss", arquivo_qss]:
            caminho = _STYLES / nome
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    estilo += f.read() + "\n"
            except FileNotFoundError:
                pass
        self.setStyleSheet(estilo)

    def _criar_estrelas(self, quantidade=120):
        largura = self.width() or 900
        altura = self.height() or 600
        return [
            {
                "x":          random.randint(0, largura),
                "y":          random.randint(0, altura),
                "tamanho":    random.uniform(0.8, 2.5),
                "fase":       random.uniform(0, math.pi * 2),
                "velocidade": random.uniform(0.8, 2.5),
            }
            for _ in range(quantidade)
        ]

    def _pulso(self):
        self._tempo += 0.05
        self.update()

    def resizeEvent(self, evento):
        self._estrelas = self._criar_estrelas()
        super().resizeEvent(evento)

    def paintEvent(self, _evento):
        pintor = QPainter(self)
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        largura, altura = self.width(), self.height()

        pintor.fillRect(self.rect(), QColor(2, 3, 10))

        gradiente = QRadialGradient(largura / 2, 0, altura)
        gradiente.setColorAt(0.00, QColor(17, 45, 78))
        gradiente.setColorAt(0.45, QColor(5,  8,  22))
        gradiente.setColorAt(1.00, QColor(2,  3,  10))
        pintor.fillRect(self.rect(), gradiente)

        brilho_topo = QRadialGradient(largura / 2, 0, min(largura, altura) * 0.55)
        brilho_topo.setColorAt(0.0, QColor(63, 114, 175, 36))
        brilho_topo.setColorAt(1.0, QColor(63, 114, 175,  0))
        pintor.fillRect(self.rect(), brilho_topo)

        pintor.setPen(Qt.PenStyle.NoPen)
        for estrela in self._estrelas:
            opacidade = 0.2 + 0.6 * (0.5 + 0.5 * math.sin(
                self._tempo * estrela["velocidade"] + estrela["fase"]
            ))
            pintor.setBrush(QBrush(QColor(255, 255, 255, int(opacidade * 255))))
            tam = estrela["tamanho"]
            pintor.drawEllipse(QRectF(
                estrela["x"] - tam / 2,
                estrela["y"] - tam / 2,
                tam, tam
            ))

        pintor.end()
