import sys
from PyQt6.QtWidgets import QApplication
from interface.core.language_screen import LanguageScreen
from interface.core.main_screen import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    language_screen = LanguageScreen()

    def open_main(lang):
        main_window = MainWindow(lang, language_screen)
        main_window.show()

        # quando voltar para tela de idioma
        language_screen.language_selected.connect(
            lambda new_lang: main_window.set_lang(new_lang)
        )

    language_screen.language_selected.connect(open_main)

    language_screen.show()

    sys.exit(app.exec())
