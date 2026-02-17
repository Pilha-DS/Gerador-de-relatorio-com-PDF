from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QTabWidget,
    QLabel,
    QMenu,
    QMessageBox,
    QInputDialog,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QAbstractItemView,
    QApplication
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QEvent

import os
import csv
import json
import xml.etree.ElementTree as ET

from core.helper.helper import join_path
from core.functions.archive_manager import ArchiveManager


class SearchDialog(QDialog):
    def __init__(self, parent=None, column_name=""):
        super().__init__(parent)
        self.setWindowTitle(f"Pesquisar na coluna '{column_name}'")
        self.setModal(True)
        self.value = None

        layout = QFormLayout()
        self.input_field = QLineEdit()
        layout.addRow("Valor:", self.input_field)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def accept(self) -> None:
        self.value = self.input_field.text()
        super().accept()


class MainWindow(QWidget):

    def __init__(self, lang="en", language_screen=None):
        super().__init__()

        self.lang = lang
        self.language_screen = language_screen

        self.archive_manager = ArchiveManager()

        self.images_path = join_path(["default", "images"], True)
        self.icon_path = join_path([self.images_path, "icon.png"])

        self.resize(1000, 600)
        self.setWindowTitle("Análise de Dados")
        self.setWindowIcon(QIcon(self.icon_path))

        self.last_search = {}  # guarda última pesquisa
        self.last_selected_row = {}  # última linha selecionada para Shift+Click

        self.create_widgets()

    # =============================
    # UI
    # =============================

    def create_widgets(self):
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.open_tab_menu)

        self.btn_open_file = QPushButton("Abrir Arquivo")
        self.btn_open_file.clicked.connect(self.open_file)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_open_file)
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.load_saved_tabs()

    # =============================
    # FILE OPEN
    # =============================

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo",
            "",
            "Arquivos (*.csv *.json *.xml)"
        )

        if file_path:
            name, ok = QInputDialog.getText(
                self,
                "Nome da Aba",
                "Digite um nome para a aba:",
                text=os.path.basename(file_path)
            )
            custom_name = name.strip() if ok and name.strip() else os.path.basename(file_path)

            self.archive_manager.add_archive(file_path, custom_name=custom_name)
            self.add_tab(file_path, custom_name=custom_name)

    # =============================
    # TAB CONTROL
    # =============================

    def add_tab(self, file_path, custom_name=None):
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Erro", "Arquivo não encontrado.")
            return

        name = custom_name or os.path.basename(file_path)

        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if widget.property("file_path") == file_path:
                self.tabs.setCurrentIndex(i)
                self.tabs.setTabText(i, name)
                return

        data_table = self.load_file_data(file_path)

        if data_table:
            table = QTableWidget()
            table.setProperty("file_path", file_path)
            table.setRowCount(len(data_table) - 1)
            table.setColumnCount(len(data_table[0]))
            table.setHorizontalHeaderLabels(data_table[0])

            for row_idx, row_data in enumerate(data_table[1:]):
                for col_idx, cell in enumerate(row_data):
                    table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))

            # Seleção inteligente
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
            table.viewport().installEventFilter(self)

            # Clique no cabeçalho
            table.horizontalHeader().sectionClicked.connect(lambda index, t=table: self.next_result(t, index))
            table.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            table.horizontalHeader().customContextMenuRequested.connect(lambda pos, t=table: self.new_search_context(t, pos))

            # Clique direito no item
            table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            table.customContextMenuRequested.connect(lambda pos, t=table: self.row_context_menu(t, pos))

            self.tabs.addTab(table, name)
            self.tabs.setCurrentWidget(table)
        else:
            label = QLabel(f"Arquivo carregado:\n\n{file_path}")
            label.setAlignment(Qt.AlignmentFlag.AlignTop)
            label.setProperty("file_path", file_path)
            self.tabs.addTab(label, name)
            self.tabs.setCurrentWidget(label)

    # =============================
    # CARREGAR DADOS
    # =============================

    def load_file_data(self, file_path):
        data_table = None

        if file_path.lower().endswith(".csv"):
            try:
                with open(file_path, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    data_table = list(reader)
            except Exception as e:
                data_table = [["Erro ao ler CSV:", str(e)]]

        elif file_path.lower().endswith(".json"):
            try:
                with open(file_path, encoding="utf-8") as f:
                    json_data = json.load(f)
                    if isinstance(json_data, list) and all(isinstance(d, dict) for d in json_data):
                        headers = list(json_data[0].keys()) if json_data else []
                        data_table = [headers] + [[str(d.get(h, "")) for h in headers] for d in json_data]
                    else:
                        data_table = [[str(json_data)]]
            except Exception as e:
                data_table = [["Erro ao ler JSON:", str(e)]]

        elif file_path.lower().endswith(".xml"):
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                rows = []
                headers = []
                for i, child in enumerate(root):
                    if i == 0:
                        headers = list(child.attrib.keys()) + [c.tag for c in child]
                        rows.append(headers)
                    row = [child.attrib.get(h, "") for h in headers[:len(child.attrib)]] + [c.text for c in child]
                    rows.append(row)
                data_table = rows if rows else [["Sem dados"]]
            except Exception as e:
                data_table = [["Erro ao ler XML:", str(e)]]

        return data_table

    # =============================
    # SELEÇÃO INTELIGENTE
    # =============================

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseButtonPress and isinstance(source.parent(), QTableWidget):
            table = source.parent()
            index = table.indexAt(event.pos())
            row = index.row()
            if row < 0:
                return super().eventFilter(source, event)

            modifiers = QApplication.keyboardModifiers()
            last_row = self.last_selected_row.get(table)

            if modifiers == Qt.KeyboardModifier.ShiftModifier and last_row is not None:
                # Shift → seleciona de last_row até row, inclusive
                start = min(last_row, row)
                end = max(last_row, row)
                for r in range(start, end + 1):
                    table.selectRow(r)
            elif modifiers == Qt.KeyboardModifier.ControlModifier:
                # Ctrl → adiciona ou remove do conjunto
                if table.selectionModel().isRowSelected(row, table.rootIndex()):
                    # desmarca
                    table.selectionModel().select(
                        table.model().index(row, 0),
                        table.selectionModel().SelectionFlag.Deselect | table.selectionModel().SelectionFlag.Rows
                    )
                else:
                    table.selectRow(row)
            else:
                # Clique normal → desmarca tudo e seleciona apenas
                table.clearSelection()
                table.selectRow(row)

            self.last_selected_row[table] = row
            return True

        return super().eventFilter(source, event)

    # =============================
    # MENU CONTEXTO LINHAS
    # =============================

    def row_context_menu(self, table, pos):
        selected_rows = sorted(set(i.row() for i in table.selectionModel().selectedRows()), reverse=True)
        index = table.indexAt(pos)
        if index.isValid() and index.row() not in selected_rows:
            # Não remove seleções existentes, só inclui temporariamente a clicada
            selected_rows.append(index.row())
            selected_rows.sort(reverse=True)

        menu = QMenu()
        delete_action = menu.addAction("Excluir linhas selecionadas")
        action = menu.exec(table.viewport().mapToGlobal(pos))

        if action == delete_action:
            for row in selected_rows:
                table.removeRow(row)


    # =============================
    # Keyboard support
    # =============================

    def keyPressEvent(self, event):
        """Permite excluir linhas selecionadas pressionando Delete"""
        if event.key() == Qt.Key.Key_Delete:
            current_widget = self.tabs.currentWidget()
            if isinstance(current_widget, QTableWidget):
                table = current_widget
                selected_rows = sorted(set(i.row() for i in table.selectionModel().selectedRows()), reverse=True)
                for row in selected_rows:
                    table.removeRow(row)


    # =============================
    # PESQUISA
    # =============================

    def next_result(self, table, column_index):
        if (self.last_search.get('table') == table and
            self.last_search.get('column') == column_index):
            rows = self.last_search['rows']
            if not rows:
                return
            self.last_search['current_index'] = (self.last_search['current_index'] + 1) % len(rows)
            row = rows[self.last_search['current_index']]
            table.clearSelection()
            table.selectRow(row)
            table.scrollToItem(table.item(row, column_index), QAbstractItemView.ScrollHint.PositionAtCenter)
        else:
            self.new_search(table, column_index)

    def new_search_context(self, table, pos):
        column_index = table.horizontalHeader().logicalIndexAt(pos)
        self.new_search(table, column_index)

    def new_search(self, table, column_index):
        column_name = table.horizontalHeaderItem(column_index).text()
        dialog = SearchDialog(self, column_name)
        if dialog.exec() and dialog.value:
            value_to_search = dialog.value.strip()
        else:
            return

        table.clearSelection()
        matching_rows = []
        for row in range(table.rowCount()):
            item = table.item(row, column_index)
            if item and value_to_search.lower() in item.text().lower():
                table.selectRow(row)
                matching_rows.append(row)

        if matching_rows:
            self.last_search = {
                'table': table,
                'column': column_index,
                'value': value_to_search,
                'rows': matching_rows,
                'current_index': 0
            }
            table.scrollToItem(table.item(matching_rows[0], column_index), QAbstractItemView.ScrollHint.PositionAtCenter)
        else:
            QMessageBox.information(self, "Pesquisa", f"Nenhum valor '{value_to_search}' encontrado na coluna.")

    # =============================
    # FECHAR ABA
    # =============================

    def close_tab(self, index):
        widget = self.tabs.widget(index)
        if not widget:
            return

        file_path = widget.property("file_path")

        if file_path:
            data = self.archive_manager.load_archives()
            for archive in data["loaded_archives"]:
                if archive["path"] == file_path:
                    if archive.get("pinned", False):
                        QMessageBox.warning(
                            self,
                            "Atenção",
                            f"O arquivo '{os.path.basename(file_path)}' está fixado e não pode ser fechado."
                        )
                        return
                    else:
                        self.archive_manager.remove_archive(file_path)
                        break

        self.tabs.removeTab(index)

    # =============================
    # LOAD SAVED TABS
    # =============================

    def load_saved_tabs(self):
        data = self.archive_manager.load_archives()
        archives = data["loaded_archives"]

        archives.sort(key=lambda x: not x.get("pinned", False))

        for archive in archives:
            if os.path.exists(archive["path"]):
                self.add_tab(archive["path"], custom_name=archive.get("custom_name"))

                index = self.tabs.count() - 1
                color = Qt.GlobalColor.yellow if archive.get("pinned", False) else Qt.GlobalColor.white
                self.tabs.tabBar().setTabTextColor(index, color)

    # =============================
    # CONTEXT MENU (FIXAR/RENOMEAR ABA)
    # =============================

    def open_tab_menu(self, position):
        index = self.tabs.tabBar().tabAt(position)
        if index < 0:
            return

        menu = QMenu()
        pin_action = menu.addAction("Fixar / Desfixar")
        rename_action = menu.addAction("Renomear Aba")

        action = menu.exec(self.tabs.mapToGlobal(position))

        widget = self.tabs.widget(index)
        file_path = widget.property("file_path")
        data = self.archive_manager.load_archives()

        archive = next((a for a in data["loaded_archives"] if a["path"] == file_path), None)
        if not archive:
            return

        if action == pin_action:
            archive["pinned"] = not archive.get("pinned", False)
            self.archive_manager.save_archives(data)

            tab_name = archive.get("custom_name") or os.path.basename(file_path)
            self.tabs.setTabText(index, tab_name)
            color = Qt.GlobalColor.yellow if archive["pinned"] else Qt.GlobalColor.white
            self.tabs.tabBar().setTabTextColor(index, color)

        elif action == rename_action:
            current_name = self.tabs.tabText(index)
            new_name, ok = QInputDialog.getText(
                self,
                "Renomear Aba",
                "Digite o novo nome da aba:",
                text=current_name
            )

            if ok and new_name.strip():
                new_name = new_name.strip()
                self.tabs.setTabText(index, new_name)
                archive["custom_name"] = new_name
                self.archive_manager.save_archives(data)
