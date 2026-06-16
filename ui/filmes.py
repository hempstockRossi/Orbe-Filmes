from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QScrollArea, QWidget, QFrame,
    QDialog, QFormLayout, QSpinBox, QMessageBox,
)

from ui.tela_base import TelaBase
from ui.botao import BotaoOrbe
import db

_DIALOG_STYLE = """
QDialog {
    background-color: #070D1F;
}
QLabel {
    color: #DBE2EF;
    font-size: 13px;
}
QLineEdit, QSpinBox {
    background: rgba(63, 114, 175, 40);
    border: 1px solid rgba(63, 114, 175, 120);
    border-radius: 8px;
    color: white;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 34px;
}
QLineEdit:focus, QSpinBox:focus {
    border-color: #3F72AF;
    background: rgba(63, 114, 175, 65);
}
QSpinBox::up-button, QSpinBox::down-button {
    background: rgba(63,114,175,80);
    border: none;
    width: 20px;
}
#botaoSalvar {
    background: #3F72AF;
    color: white;
    border-radius: 8px;
    padding: 9px 22px;
    font-size: 13px;
    border: none;
}
#botaoSalvar:hover { background: #5589C4; }
#botaoCancelar {
    background: rgba(255,255,255,15);
    color: rgba(219,226,239,180);
    border-radius: 8px;
    padding: 9px 22px;
    font-size: 13px;
    border: 1px solid rgba(255,255,255,30);
}
#botaoCancelar:hover { background: rgba(255,255,255,30); }
"""


class _DialogAdicionarFilme(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Filme")
        self.setFixedSize(420, 295)
        self.setStyleSheet(_DIALOG_STYLE)
        self._montar()

    def _montar(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(30, 28, 30, 22)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._titulo = QLineEdit()
        self._titulo.setPlaceholderText("Ex: Interestelar")
        self._diretor = QLineEdit()
        self._diretor.setPlaceholderText("Ex: Christopher Nolan")
        self._ano = QSpinBox()
        self._ano.setRange(1888, 2100)
        self._ano.setValue(2024)
        self._genero = QLineEdit()
        self._genero.setPlaceholderText("Ex: Ficção Científica")

        layout.addRow("Título:", self._titulo)
        layout.addRow("Diretor:", self._diretor)
        layout.addRow("Ano:", self._ano)
        layout.addRow("Gênero:", self._genero)

        rodape = QHBoxLayout()
        btn_cancelar = BotaoOrbe("Cancelar")
        btn_cancelar.setObjectName("botaoCancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_salvar = BotaoOrbe("Salvar")
        btn_salvar.setObjectName("botaoSalvar")
        btn_salvar.clicked.connect(self._salvar)
        rodape.addStretch()
        rodape.addWidget(btn_cancelar)
        rodape.addWidget(btn_salvar)
        layout.addRow(rodape)

    def _salvar(self):
        titulo = self._titulo.text().strip()
        diretor = self._diretor.text().strip()
        genero = self._genero.text().strip()
        if not titulo or not diretor or not genero:
            QMessageBox.warning(self, "Atenção", "Preencha todos os campos.")
            return
        db.inserir_filme(titulo, diretor, self._ano.value(), genero)
        self.accept()


class _CardFilme(QFrame):
    def __init__(self, filme):
        super().__init__()
        self._filme = filme
        self._favorito = db.is_favorito(filme["id"])
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

        self._btn_coracao = BotaoOrbe()
        self._btn_coracao.setObjectName("botaoCoracao")
        self._btn_coracao.setFixedSize(40, 40)
        self._btn_coracao.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_coracao.clicked.connect(self._toggle_favorito)
        self._atualizar_coracao()

        layout.addLayout(col_info)
        layout.addStretch()
        layout.addWidget(self._btn_coracao)

    def _atualizar_coracao(self):
        if self._favorito:
            cor = "#E74C3C"
            cor_hover = "#FF6B6B"
            texto = "♥"
        else:
            cor = "rgba(255,255,255,55)"
            cor_hover = "rgba(255,255,255,150)"
            texto = "♡"
        self._btn_coracao.setText(texto)
        self._btn_coracao.setStyleSheet(
            f"QPushButton {{ color: {cor}; font-size: 22px; background: transparent; border: none; }}"
            f"QPushButton:hover {{ color: {cor_hover}; }}"
        )

    def _toggle_favorito(self):
        if self._favorito:
            db.remover_favorito(self._filme["id"])
        else:
            db.adicionar_favorito(self._filme["id"])
        self._favorito = not self._favorito
        self._atualizar_coracao()


class Filmes(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Filmes")
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(14)

        cabecalho = QHBoxLayout()
        btn_voltar = BotaoOrbe("← Voltar")
        btn_voltar.setObjectName("botaoVoltar")
        btn_voltar.clicked.connect(self._voltar)

        titulo = QLabel("FILMES")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_adicionar = BotaoOrbe("+ Adicionar")
        btn_adicionar.setObjectName("botaoAdicionar")
        btn_adicionar.clicked.connect(self._abrir_dialog)

        cabecalho.addWidget(btn_voltar)
        cabecalho.addStretch()
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(btn_adicionar)

        self._campo_busca = QLineEdit()
        self._campo_busca.setObjectName("campoBusca")
        self._campo_busca.setPlaceholderText("🔍  Buscar filmes...")
        self._campo_busca.textChanged.connect(self._filtrar)

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
        layout.addWidget(self._campo_busca)
        layout.addWidget(self._scroll)

        self._carregar_estilo("filmes.qss")
        self._carregar_filmes()

    def _carregar_filmes(self, filtro=""):
        while self._lista_layout.count() > 1:
            item = self._lista_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        filmes = db.listar_filmes()
        if filtro:
            filtro_lower = filtro.lower()
            filmes = [f for f in filmes if filtro_lower in f["titulo"].lower()]

        if not filmes:
            lbl = QLabel("Nenhum filme encontrado." if filtro else "Nenhum filme cadastrado ainda.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: rgba(255,255,255,45); font-size: 14px; padding: 20px;")
            self._lista_layout.insertWidget(0, lbl)
        else:
            for filme in filmes:
                card = _CardFilme(filme)
                self._lista_layout.insertWidget(self._lista_layout.count() - 1, card)

    def _filtrar(self, texto):
        self._carregar_filmes(texto)

    def _abrir_dialog(self):
        dialog = _DialogAdicionarFilme(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._carregar_filmes(self._campo_busca.text())

    def _voltar(self):
        from ui.dashboard import Dashboard
        self._proxima_tela = Dashboard()
        self._proxima_tela.show()
        self.close()
