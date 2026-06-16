from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QFrame, QTextEdit,
    QComboBox, QDoubleSpinBox, QDateEdit, QMessageBox,
)

from ui.tela_base import TelaBase
import db


class _CardComentario(QFrame):
    def __init__(self, comentario, ao_deletar):
        super().__init__()
        self._comentario = comentario
        self._ao_deletar = ao_deletar
        self._montar()

    def _montar(self):
        self.setObjectName("cardComentario")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(6)

        topo = QHBoxLayout()

        lbl_filme = QLabel(self._comentario["titulo"])
        lbl_filme.setObjectName("cardFilmeTitulo")

        lbl_nota = QLabel(f"★ {self._comentario['nota']:.1f}")
        lbl_nota.setObjectName("cardNota")

        btn_del = QPushButton("✕")
        btn_del.setObjectName("botaoDeletar")
        btn_del.setFixedSize(26, 26)
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(self._deletar)

        topo.addWidget(lbl_filme)
        topo.addStretch()
        topo.addWidget(lbl_nota)
        topo.addSpacing(6)
        topo.addWidget(btn_del)

        lbl_texto = QLabel(self._comentario["texto_comentario"])
        lbl_texto.setObjectName("cardFilmeDetalhe")
        lbl_texto.setWordWrap(True)

        data_assistido = self._comentario.get("data_assistido")
        data_str = (
            f"Assistido em: {data_assistido.strftime('%d/%m/%Y')}"
            if data_assistido else ""
        )
        lbl_data = QLabel(data_str)
        lbl_data.setObjectName("cardComentarioData")

        layout.addLayout(topo)
        layout.addWidget(lbl_texto)
        if data_str:
            layout.addWidget(lbl_data)

    def _deletar(self):
        db.deletar_comentario(self._comentario["id"])
        self._ao_deletar()


class Comentarios(TelaBase):

    def __init__(self):
        super().__init__("ORBE - Comentários")
        self._montar_interface()

    def _montar_interface(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(14)

        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton("← Voltar")
        btn_voltar.setObjectName("botaoVoltar")
        btn_voltar.clicked.connect(self._voltar)

        titulo = QLabel("COMENTÁRIOS")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cabecalho.addWidget(btn_voltar)
        cabecalho.addStretch()
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()

        layout.addLayout(cabecalho)

        # Formulário de novo comentário
        form = QFrame()
        form.setObjectName("formComentario")
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(20, 16, 20, 16)
        form_layout.setSpacing(10)

        lbl_form = QLabel("NOVO COMENTÁRIO")
        lbl_form.setObjectName("formTitulo")

        self._combo_filmes = QComboBox()
        self._combo_filmes.setObjectName("comboFilmes")
        self._combo_filmes.setPlaceholderText("Selecione um filme...")
        self._carregar_combo()

        self._texto = QTextEdit()
        self._texto.setObjectName("textoComentario")
        self._texto.setPlaceholderText("Escreva seu comentário sobre o filme...")
        self._texto.setFixedHeight(76)

        linha = QHBoxLayout()
        linha.setSpacing(10)

        lbl_data = QLabel("Assistido em:")
        lbl_data.setObjectName("formLabel")

        self._data_edit = QDateEdit()
        self._data_edit.setObjectName("dataEdit")
        self._data_edit.setDate(QDate.currentDate())
        self._data_edit.setCalendarPopup(True)
        self._data_edit.setDisplayFormat("dd/MM/yyyy")
        self._data_edit.setFixedWidth(130)

        self._nota = QDoubleSpinBox()
        self._nota.setObjectName("notaSpinBox")
        self._nota.setRange(1.0, 10.0)
        self._nota.setSingleStep(0.5)
        self._nota.setValue(7.0)
        self._nota.setPrefix("★  ")
        self._nota.setFixedWidth(100)

        btn_salvar = QPushButton("Salvar comentário")
        btn_salvar.setObjectName("botaoSalvar")
        btn_salvar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_salvar.clicked.connect(self._salvar_comentario)

        linha.addWidget(lbl_data)
        linha.addWidget(self._data_edit)
        linha.addSpacing(10)
        linha.addWidget(self._nota)
        linha.addStretch()
        linha.addWidget(btn_salvar)

        form_layout.addWidget(lbl_form)
        form_layout.addWidget(self._combo_filmes)
        form_layout.addWidget(self._texto)
        form_layout.addLayout(linha)

        layout.addWidget(form)

        # Lista de comentários
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
        layout.addWidget(self._scroll)

        self._carregar_estilo("comentarios.qss")
        self._carregar_comentarios()

    def _carregar_combo(self):
        self._combo_filmes.clear()
        for filme in db.listar_filmes():
            self._combo_filmes.addItem(filme["titulo"], filme["id"])

    def _salvar_comentario(self):
        if self._combo_filmes.currentIndex() < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um filme.")
            return
        texto = self._texto.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Atenção", "Escreva um comentário.")
            return

        db.inserir_comentario(
            filme_id=self._combo_filmes.currentData(),
            texto_comentario=texto,
            data_assistido=self._data_edit.date().toPython(),
            nota=self._nota.value(),
        )
        self._texto.clear()
        self._carregar_comentarios()

    def _carregar_comentarios(self):
        while self._lista_layout.count() > 1:
            item = self._lista_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        comentarios = db.listar_comentarios()

        if not comentarios:
            lbl = QLabel("Nenhum comentário ainda.\nAdicione um comentário acima.")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: rgba(255,255,255,45); font-size: 14px; padding: 20px;")
            self._lista_layout.insertWidget(0, lbl)
        else:
            for c in comentarios:
                card = _CardComentario(c, self._carregar_comentarios)
                self._lista_layout.insertWidget(self._lista_layout.count() - 1, card)

    def _voltar(self):
        from ui.dashboard import Dashboard
        self._proxima_tela = Dashboard()
        self._proxima_tela.show()
        self.close()
