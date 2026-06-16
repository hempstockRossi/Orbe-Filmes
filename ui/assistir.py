from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QFrame, QDialog,
    QFormLayout, QComboBox, QMessageBox,
    QStackedWidget, QLineEdit, QSpinBox,
)

from ui.tela_base import TelaBase
import db

_DIALOG_STYLE = """
QDialog { background-color: #070D1F; }
QLabel { color: #DBE2EF; font-size: 13px; }
QComboBox, QLineEdit, QSpinBox {
    background: rgba(63, 114, 175, 40);
    border: 1px solid rgba(63, 114, 175, 120);
    border-radius: 8px;
    color: white;
    padding: 8px 12px;
    font-size: 13px;
    min-height: 34px;
}
QComboBox:focus, QLineEdit:focus, QSpinBox:focus { border-color: #3F72AF; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background: #0D1B2A;
    border: 1px solid rgba(63,114,175,150);
    color: white;
    selection-background-color: #3F72AF;
    outline: none;
}
QSpinBox::up-button, QSpinBox::down-button {
    background: rgba(63,114,175,80);
    border: none;
    width: 18px;
}
#botaoSalvar {
    background: #3F72AF; color: white;
    border-radius: 8px; padding: 9px 22px;
    font-size: 13px; border: none;
}
#botaoSalvar:hover { background: #5589C4; }
#botaoCancelar {
    background: rgba(255,255,255,15);
    color: rgba(219,226,239,180);
    border-radius: 8px; padding: 9px 22px;
    font-size: 13px;
    border: 1px solid rgba(255,255,255,30);
}
#botaoCancelar:hover { background: rgba(255,255,255,30); }
#toggleAtivo {
    background: #3F72AF; color: white;
    border-radius: 8px; padding: 7px 0;
    font-size: 12px; border: none; font-weight: bold;
}
#toggleInativo {
    background: rgba(63,114,175,25);
    color: rgba(219,226,239,150);
    border-radius: 8px; padding: 7px 0;
    font-size: 12px;
    border: 1px solid rgba(63,114,175,60);
}
#toggleInativo:hover { background: rgba(63,114,175,50); color: white; }
"""


class _DialogAdicionar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar à Lista")
        self.setFixedSize(430, 340)
        self.setStyleSheet(_DIALOG_STYLE)
        self._modo_novo = False
        self._montar()

    def _montar(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 22)
        layout.setSpacing(12)

        toggle = QHBoxLayout()
        toggle.setSpacing(6)
        self._btn_existente = QPushButton("Filme existente")
        self._btn_existente.setObjectName("toggleAtivo")
        self._btn_existente.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_existente.clicked.connect(lambda: self._mudar_modo(False))
        self._btn_novo = QPushButton("Novo filme")
        self._btn_novo.setObjectName("toggleInativo")
        self._btn_novo.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_novo.clicked.connect(lambda: self._mudar_modo(True))
        toggle.addWidget(self._btn_existente)
        toggle.addWidget(self._btn_novo)
        layout.addLayout(toggle)

        self._stack = QStackedWidget()

        # Página 0 — selecionar existente
        pag_exist = QWidget()
        form_exist = QFormLayout(pag_exist)
        form_exist.setSpacing(10)
        form_exist.setContentsMargins(0, 6, 0, 0)
        form_exist.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self._combo = QComboBox()
        self._combo.setPlaceholderText("Selecione um filme...")
        for f in db.listar_filmes():
            self._combo.addItem(f["titulo"], f["id"])
        form_exist.addRow("Filme:", self._combo)
        self._stack.addWidget(pag_exist)

        # Página 1 — novo filme
        pag_novo = QWidget()
        form_novo = QFormLayout(pag_novo)
        form_novo.setSpacing(10)
        form_novo.setContentsMargins(0, 6, 0, 0)
        form_novo.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self._titulo = QLineEdit()
        self._titulo.setPlaceholderText("Ex: Interestelar")
        self._diretor = QLineEdit()
        self._diretor.setPlaceholderText("Ex: Christopher Nolan")
        self._ano = QSpinBox()
        self._ano.setRange(1888, 2100)
        self._ano.setValue(2024)
        self._genero = QLineEdit()
        self._genero.setPlaceholderText("Ex: Ficção Científica")
        form_novo.addRow("Título:", self._titulo)
        form_novo.addRow("Diretor:", self._diretor)
        form_novo.addRow("Ano:", self._ano)
        form_novo.addRow("Gênero:", self._genero)
        self._stack.addWidget(pag_novo)

        layout.addWidget(self._stack)
        layout.addStretch()

        rodape = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("botaoCancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_salvar = QPushButton("Adicionar")
        btn_salvar.setObjectName("botaoSalvar")
        btn_salvar.clicked.connect(self._salvar)
        rodape.addStretch()
        rodape.addWidget(btn_cancelar)
        rodape.addWidget(btn_salvar)
        layout.addLayout(rodape)

    def _mudar_modo(self, novo):
        self._modo_novo = novo
        self._stack.setCurrentIndex(1 if novo else 0)
        self._btn_novo.setObjectName("toggleAtivo" if novo else "toggleInativo")
        self._btn_existente.setObjectName("toggleInativo" if novo else "toggleAtivo")
        for btn in (self._btn_novo, self._btn_existente):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _salvar(self):
        if self._modo_novo:
            titulo = self._titulo.text().strip()
            diretor = self._diretor.text().strip()
            genero = self._genero.text().strip()
            if not titulo or not diretor or not genero:
                QMessageBox.warning(self, "Atenção", "Preencha todos os campos do filme.")
                return
            filme_id = db.inserir_filme(titulo, diretor, self._ano.value(), genero)
        else:
            if self._combo.currentIndex() < 0:
                QMessageBox.warning(self, "Atenção", "Selecione um filme.")
                return
            filme_id = self._combo.currentData()

        db.inserir_assistir(filme_id)
        self.accept()


class _CardPendente(QFrame):
    """Card da lista 'A Assistir' com botão de marcar como assistido."""

    def __init__(self, item, ao_atualizar):
        super().__init__()
        self._item = item
        self._ao_atualizar = ao_atualizar
        self._montar()

    def _montar(self):
        self.setObjectName("cardAssistir")
        self.setFixedHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 16, 0)
        layout.setSpacing(10)

        col_info = QVBoxLayout()
        col_info.setSpacing(4)
        lbl_titulo = QLabel(self._item["titulo"])
        lbl_titulo.setObjectName("cardFilmeTitulo")
        lbl_detalhe = QLabel(
            f"{self._item['diretor']}  ·  {self._item['ano_lancamento']}  ·  {self._item['genero']}"
        )
        lbl_detalhe.setObjectName("cardFilmeDetalhe")
        col_info.addWidget(lbl_titulo)
        col_info.addWidget(lbl_detalhe)

        btn_assistido = QPushButton("✓  Assistido")
        btn_assistido.setObjectName("botaoAssistido")
        btn_assistido.setFixedHeight(34)
        btn_assistido.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_assistido.setToolTip("Marcar como assistido")
        btn_assistido.clicked.connect(self._marcar)

        btn_excluir = QPushButton("✕")
        btn_excluir.setObjectName("botaoDeletar")
        btn_excluir.setFixedSize(34, 34)
        btn_excluir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_excluir.clicked.connect(self._excluir)

        layout.addLayout(col_info)
        layout.addStretch()
        layout.addWidget(btn_assistido)
        layout.addWidget(btn_excluir)

    def _marcar(self):
        db.marcar_assistido(self._item["id"], self._item["filme_id"])
        self._ao_atualizar()

    def _excluir(self):
        db.deletar_assistir(self._item["id"])
        self._ao_atualizar()


class _CardAssistido(QFrame):
    """Card da lista 'Assistidos' com data/hora salva automaticamente."""

    def __init__(self, item, ao_atualizar):
        super().__init__()
        self._item = item
        self._ao_atualizar = ao_atualizar
        self._montar()

    def _montar(self):
        self.setObjectName("cardAssistido")
        self.setFixedHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 16, 0)
        layout.setSpacing(10)

        col_info = QVBoxLayout()
        col_info.setSpacing(4)
        lbl_titulo = QLabel(self._item["titulo"])
        lbl_titulo.setObjectName("cardFilmeTitulo")
        lbl_detalhe = QLabel(
            f"{self._item['diretor']}  ·  {self._item['ano_lancamento']}  ·  {self._item['genero']}"
        )
        lbl_detalhe.setObjectName("cardFilmeDetalhe")
        col_info.addWidget(lbl_titulo)
        col_info.addWidget(lbl_detalhe)

        data = self._item["data_assistido"]
        if hasattr(data, "strftime"):
            data_str = data.strftime("%d/%m/%Y  %H:%M")
        else:
            data_str = str(data)
        lbl_data = QLabel(f"✓  {data_str}")
        lbl_data.setObjectName("cardAssistidoData")

        btn_excluir = QPushButton("✕")
        btn_excluir.setObjectName("botaoDeletar")
        btn_excluir.setFixedSize(34, 34)
        btn_excluir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_excluir.clicked.connect(self._excluir)

        layout.addLayout(col_info)
        layout.addStretch()
        layout.addWidget(lbl_data)
        layout.addSpacing(10)
        layout.addWidget(btn_excluir)

    def _excluir(self):
        db.deletar_assistido(self._item["id"])
        self._ao_atualizar()


class Assistir(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Assistir")
        self._aba_ativa = 0  # 0 = a assistir, 1 = assistidos
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(14)

        # Cabeçalho
        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton("← Voltar")
        btn_voltar.setObjectName("botaoVoltar")
        btn_voltar.clicked.connect(self._voltar)

        titulo = QLabel("ASSISTIR")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._btn_adicionar = QPushButton("+ Adicionar")
        self._btn_adicionar.setObjectName("botaoAdicionar")
        self._btn_adicionar.clicked.connect(self._abrir_dialog)

        cabecalho.addWidget(btn_voltar)
        cabecalho.addStretch()
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        cabecalho.addWidget(self._btn_adicionar)
        layout.addLayout(cabecalho)

        # Abas
        abas = QHBoxLayout()
        abas.setSpacing(6)
        self._btn_aba_pendente = QPushButton("A Assistir")
        self._btn_aba_pendente.setObjectName("abaAtiva")
        self._btn_aba_pendente.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_aba_pendente.clicked.connect(lambda: self._mudar_aba(0))

        self._btn_aba_assistidos = QPushButton("Assistidos")
        self._btn_aba_assistidos.setObjectName("abaInativa")
        self._btn_aba_assistidos.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_aba_assistidos.clicked.connect(lambda: self._mudar_aba(1))

        abas.addWidget(self._btn_aba_pendente)
        abas.addWidget(self._btn_aba_assistidos)
        abas.addStretch()
        layout.addLayout(abas)

        # Stack das listas
        self._stack = QStackedWidget()

        # Página 0 — A Assistir
        pag_pendente = QWidget()
        pag_layout_0 = QVBoxLayout(pag_pendente)
        pag_layout_0.setContentsMargins(0, 0, 0, 0)
        self._scroll_pendente = self._criar_scroll()
        pag_layout_0.addWidget(self._scroll_pendente)
        self._stack.addWidget(pag_pendente)

        # Página 1 — Assistidos
        pag_assistidos = QWidget()
        pag_layout_1 = QVBoxLayout(pag_assistidos)
        pag_layout_1.setContentsMargins(0, 0, 0, 0)
        self._scroll_assistidos = self._criar_scroll()
        pag_layout_1.addWidget(self._scroll_assistidos)
        self._stack.addWidget(pag_assistidos)

        layout.addWidget(self._stack)

        self._carregar_estilo("assistir.qss")
        self._carregar_pendentes()
        self._carregar_assistidos()

    def _criar_scroll(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        container = QWidget()
        container.setObjectName("scrollContainer")
        lista = QVBoxLayout(container)
        lista.setSpacing(10)
        lista.setContentsMargins(2, 2, 10, 2)
        lista.addStretch()
        scroll.setWidget(container)
        scroll._lista_layout = lista
        return scroll

    def _mudar_aba(self, indice):
        self._aba_ativa = indice
        self._stack.setCurrentIndex(indice)
        self._btn_aba_pendente.setObjectName("abaAtiva" if indice == 0 else "abaInativa")
        self._btn_aba_assistidos.setObjectName("abaAtiva" if indice == 1 else "abaInativa")
        self._btn_adicionar.setVisible(indice == 0)
        for btn in (self._btn_aba_pendente, self._btn_aba_assistidos):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _limpar_scroll(self, scroll):
        lista = scroll._lista_layout
        while lista.count() > 1:
            item = lista.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _vazio(self, texto):
        lbl = QLabel(texto)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: rgba(255,255,255,45); font-size: 14px; padding: 20px;")
        return lbl

    def _carregar_pendentes(self):
        self._limpar_scroll(self._scroll_pendente)
        lista = db.listar_assistir()
        if not lista:
            self._scroll_pendente._lista_layout.insertWidget(
                0, self._vazio("Nenhum filme na lista.\nClique em + Adicionar para começar.")
            )
        else:
            for item in lista:
                card = _CardPendente(item, self._recarregar_tudo)
                self._scroll_pendente._lista_layout.insertWidget(
                    self._scroll_pendente._lista_layout.count() - 1, card
                )

    def _carregar_assistidos(self):
        self._limpar_scroll(self._scroll_assistidos)
        lista = db.listar_assistidos()
        if not lista:
            self._scroll_assistidos._lista_layout.insertWidget(
                0, self._vazio("Nenhum filme assistido ainda.\nMarque filmes com ✓ Assistido.")
            )
        else:
            for item in lista:
                card = _CardAssistido(item, self._recarregar_tudo)
                self._scroll_assistidos._lista_layout.insertWidget(
                    self._scroll_assistidos._lista_layout.count() - 1, card
                )

    def _recarregar_tudo(self):
        self._carregar_pendentes()
        self._carregar_assistidos()

    def _abrir_dialog(self):
        dialog = _DialogAdicionar(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._carregar_pendentes()

    def _voltar(self):
        from ui.dashboard import Dashboard
        self._proxima_tela = Dashboard()
        self._proxima_tela.show()
        self.close()
