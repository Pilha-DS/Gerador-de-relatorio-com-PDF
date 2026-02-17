from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from core.helper.helper import join_path


class CreditsScreen(QWidget):

    def __init__(self, language_screen=None):
        super().__init__()

        self.language_screen = language_screen

        self.images_path = join_path(["default", "images"], True)
        self.icon_path = join_path([self.images_path, "laguageIcon.png"])

        self.setWindowTitle("Credits")
        self.setWindowIcon(QIcon(self.icon_path))
        self.resize(350, 250)

        self.create_ui()

    def create_ui(self):

        main_layout = QVBoxLayout()

        # Texto central
        self.label = QLabel(
            "Developed by:\n\n"
            "Jonathan S. Cardoso\n\n"
            "2026"
        )

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch()
        main_layout.addWidget(self.label)
        main_layout.addStretch()

        # Botão voltar (canto inferior direito)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.btn_back = QPushButton("Back")
        self.btn_back.clicked.connect(self.go_back)

        bottom_layout.addWidget(self.btn_back)

        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def go_back(self):
        self.close()
        if self.language_screen:
            self.language_screen.show()
