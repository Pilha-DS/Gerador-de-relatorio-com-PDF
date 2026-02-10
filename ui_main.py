from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox
)

from data_loader import carregar_dados
from analyzer import analisar_dados_completo
from pdf_report import gerar_pdf_completo

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Relatórios Completo")
        self.resize(500, 300)

        self.dados = []

        layout = QVBoxLayout()

        self.label = QLabel("Nenhum arquivo carregado")
        layout.addWidget(self.label)

        self.btn_arquivo = QPushButton("📂 Carregar Arquivo")
        self.btn_arquivo.clicked.connect(self.carregar_arquivo)
        layout.addWidget(self.btn_arquivo)

        self.btn_pdf = QPushButton("📄 Gerar PDF")
        self.btn_pdf.clicked.connect(self.gerar_relatorio)
        layout.addWidget(self.btn_pdf)

        self.setLayout(layout)

    def carregar_arquivo(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self, "Abrir arquivo", "", "CSV (*.csv);;JSON (*.json)"
        )

        if caminho:
            try:
                self.dados = carregar_dados(caminho)
                self.label.setText(f"Arquivo carregado: {caminho}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))

    def gerar_relatorio(self):
        if not self.dados:
            QMessageBox.warning(self, "Aviso", "Nenhum dado carregado!")
            return

        analise = analisar_dados_completo(self.dados)

        caminho, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", "", "PDF (*.pdf)"
        )

        if caminho:
            gerar_pdf_completo(caminho, self.dados, analise)
            QMessageBox.information(self, "Sucesso", "PDF gerado com sucesso!")
