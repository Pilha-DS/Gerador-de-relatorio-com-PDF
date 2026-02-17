from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from core.helper.helper import get_languages, join_path


class LanguageScreen(QWidget):

    language_selected = pyqtSignal(str)
    credits_requested = pyqtSignal()   # novo signal

    def __init__(self):
        super().__init__()

        self.images_path = join_path(["default", "images"], True)
        self.icon_path = join_path([self.images_path, "laguageIcon.png"])

        self.setWindowTitle("Select Language")
        self.setWindowIcon(QIcon(self.icon_path))
        self.resize(300, 200)

        self.create_ui()

    def create_ui(self):

        # Layout principal vertical
        main_layout = QVBoxLayout()

        # ---------------------------
        # Área central (idiomas)
        # ---------------------------
        main_layout.addStretch()

        languages = get_languages("language_screen")

        for lang_code, lang_name in languages:
            btn = QPushButton(lang_name)

            btn.clicked.connect(
                lambda checked, l=lang_code: self.select_language(l)
            )

            main_layout.addWidget(
                btn,
                alignment=Qt.AlignmentFlag.AlignCenter
            )

        main_layout.addStretch()

        # ---------------------------
        # Área inferior (botão créditos)
        # ---------------------------
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()  # empurra para direita

        self.btn_credits = QPushButton("Credits")
        self.btn_credits.clicked.connect(self.open_credits)

        bottom_layout.addWidget(self.btn_credits)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def select_language(self, lang):
        self.language_selected.emit(lang)
        self.close()

    def open_credits(self):
        self.credits_requested.emit()
