import sys
from PyQt6.QtWidgets import QApplication
from ui_main import JanelaPrincipal

app = QApplication(sys.argv)
janela = JanelaPrincipal()
janela.show()
sys.exit(app.exec())
