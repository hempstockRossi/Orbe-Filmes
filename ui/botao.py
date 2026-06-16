import math
import random

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QPushButton


class BotaoOrbe(QPushButton):
    """QPushButton com partículas sutis animadas ao hover."""

    def __init__(self, texto="", parent=None):
        super().__init__(texto, parent)
        self._hover = False
        self._opacidade = 0.0
        self._particulas = self._gerar_particulas()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    # ------------------------------------------------------------------
    def _gerar_particulas(self, n=22):
        return [
            {
                "bx":    random.uniform(0.05, 0.95),
                "by":    random.uniform(0.05, 0.95),
                "fase":  random.uniform(0, math.tau),
                "vel":   random.uniform(0.5, 1.4),
                "ax":    random.uniform(0.04, 0.12),
                "ay":    random.uniform(0.04, 0.12),
                "raio":  random.uniform(1.1, 2.0),
                "brilho": random.uniform(0.35, 0.85),
            }
            for _ in range(n)
        ]

    def _tick(self):
        alvo = 1.0 if self._hover else 0.0
        self._opacidade += (alvo - self._opacidade) * 0.12

        if self._opacidade > 0.008:
            for p in self._particulas:
                p["fase"] += 0.045 * p["vel"]
            self.update()
        elif alvo == 0.0:
            self._opacidade = 0.0

    # ------------------------------------------------------------------
    def enterEvent(self, event):
        self._hover = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        super().leaveEvent(event)

    # ------------------------------------------------------------------
    def paintEvent(self, event):
        super().paintEvent(event)          # renderiza QSS normalmente

        if self._opacidade < 0.008:
            return

        w, h = self.width(), self.height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        for p in self._particulas:
            t = p["fase"]
            px = (p["bx"] + math.sin(t) * p["ax"]) * w
            py = (p["by"] + math.cos(t * 0.73) * p["ay"]) * h

            pulso = 0.5 + 0.5 * math.sin(t * 1.2)
            alpha = int(self._opacidade * p["brilho"] * pulso * 65)  # max ≈65/255

            painter.setBrush(QBrush(QColor(255, 255, 255, max(0, alpha))))
            r = p["raio"] * (0.7 + 0.3 * pulso)
            painter.drawEllipse(QPointF(px, py), r, r)

        painter.end()
