import json
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *

from excel2json_gui.excel_converter import ExcelConverter


class ExcelConverterGui(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ExcelConverterGui, self).__init__(*args, **kwargs)
        self.script_dir = os.path.dirname(__file__)
        self.width = 450
        self.height = 300

        # self.setWindowIcon(QIcon(os.path.join('excel2json_gui/images', 'icon.png')))
        # self.setWindowIconText("Excel 2 JSON")
        # self.setWindowTitle("Excel 2 JSON")
        self.setWindowTitle(QCoreApplication.applicationName())
        self.converter = None
        self.excel_loaded = False
        
        self.layout = QVBoxLayout()
        self.excel_pages = {}

        self.tabs = QTabWidget()
        self.page_tabs = QTabWidget()
        self.excel_tab = QWidget()
        self.json_tab = QWidget()
        self.tabs.resize(300, 200)


        self.tabs.addTab(self.excel_tab, "Excel Viewer")
        self.tabs.addTab(self.json_tab, "JSON Viewer")

        self.create_table()
        self.excel_tab.layout = QVBoxLayout()
        self.excel_tab.layout.addWidget(self.page_tabs)

        self.excel_tab.setLayout(self.excel_tab.layout)

        self.json_tab.layout = QVBoxLayout()

        self.create_tree_view()
        self.json_tab.layout.addWidget(self.tree_widget)
        self.json_tab.setLayout(self.json_tab.layout)

        self.layout.addWidget(self.tabs)

        self.path = None

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        menu_bar = self.menuBar()
        # menu_bar.text("Excel 2 JSON")
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(file_toolbar)
        file_menu = menu_bar.addMenu("&File")

        open_file_action = QAction(
            QIcon(self.script_dir.split('/')[-1] + '/images/folder-open-big.png'), "Open file...", self)
            # QIcon(os.path.join('excel2json_gui/images', 'folder-open-big.png')), "Open file...", self)
            # QIcon(os.path.join(self.script_dir, '../images/folder-open-big.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        # convert_action = QAction(QIcon(os.path.join('excel2json_gui/images', 'convert-big.png')), "Convert Excel to JSON", self)
        convert_action = QAction(QIcon(self.script_dir.split('/')[-1] + '/images/convert-big.png'), "Convert Excel to JSON", self)
        # convert_action = QAction(QIcon(os.path.join(self.script_dir, '../images/convert-big.png')), "Convert Excel to JSON", self)
        convert_action.setStatusTip("Convert the Excel file")
        convert_action.triggered.connect(self.convert_file)
        file_menu.addAction(convert_action)
        file_toolbar.addAction(convert_action)

        # save_file_action = QAction(QIcon(os.path.join('excel2json_gui/images', 'save-big.png')), "Save", self)
        save_file_action = QAction(QIcon(self.script_dir.split('/')[-1] + '/images/save-big.png'), "Save", self)
        # save_file_action = QAction(QIcon(os.path.join(self.script_dir, '../images/save-big.png')), "Save", self)
        save_file_action.setStatusTip("Save JSON")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)
        print(self.script_dir)
        self.show()

    def get_image_path(self, var):
        relative_path = f"/images/{type(var).__name__}.png"
        # return os.path.join(self.script_dir, relative_path)
        return self.script_dir.split('/')[-1] + relative_path
        # return relative_path

    def dialog_critical(self, s):
        print("critical dialog")
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def create_table(self):
        if self.converter is not None:
            self.page_tabs.removeTab(0)
            for sheet in self.converter.workbook.worksheets:
                sheet_tab = QWidget()
                self.page_tabs.addTab(sheet_tab, sheet.title)
                sheet_tab.layout = QVBoxLayout()
                new_table = QTableWidget(sheet.max_row, sheet.max_column)
                for row in sheet.rows:
                    for cell in row:
                        row_val, col_val = cell.row - 1, cell.column - 1
                        cell_val = str(cell.value) if cell.value is not None else cell.value
                        new_table.setItem(row_val, col_val, QTableWidgetItem(cell_val))
                sheet_tab.layout.addWidget(new_table)
                sheet_tab.setLayout(sheet_tab.layout)
        else:
            blank_tab = QWidget()
            self.page_tabs.addTab(blank_tab, 'Empty')
            blank_tab.layout = QVBoxLayout()
            empty_table = QTableWidget(3, 5)
            for r in range(1, 4):
                for c in range(1, 5):
                    empty_table.setItem(r, c, QTableWidgetItem(None))
            blank_tab.layout.addWidget(empty_table)
            blank_tab.setLayout(blank_tab.layout)


    def create_tree_view(self):
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["JSON Viewer"])

    def fill_tree(self, item, value):
        item.setExpanded(False)
        if isinstance(value, dict):
            for key, val in value.items():
                child = QTreeWidgetItem()
                # icon = QIcon(os.path.join('excel2json_gui/images', f"{type(val).__name__}.png"))
                icon = QIcon(self.get_image_path(val))
                child.setIcon(0, icon)
                if any(map(lambda x: isinstance(val, x), (str, bool, int))):
                    child.setText(0, f'{key}: "{val}"' if isinstance(val, str) else f'{key}: {val}')
                    item.addChild(child)
                else:
                    child.setText(0, f"{key}")
                    item.addChild(child)
                    self.fill_tree(child, val)
        elif isinstance(value, list):
            for idx, val in enumerate(value):
                child = QTreeWidgetItem()
                item.addChild(child)
                # icon = QIcon(os.path.join('excel2json_gui/images', f"{type(val).__name__}.png"))
                icon = QIcon(self.get_image_path(val))
                child.setIcon(0, icon)
                if isinstance(val, dict):
                    child.setText(0, f'{idx}')
                    self.fill_tree(child, val)
                elif isinstance(val, list):
                    child.setText(0, '[list]')
                    self.fill_tree(child, val)
                else:
                    child.setText(0, f"{val}")
        else:
            child = QTreeWidgetItem()
            child.setText(0, f"{value}")
            # icon = QIcon(os.path.join('excel2json_gui/images', f"{type(value).__name__}.png"))
            icon = QIcon(self.get_image_path(value))
            child.setIcon(0, icon)
            item.addChild(child)


    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                self.converter = ExcelConverter(file_name=path)
                self.excel_loaded = True
                self.create_table()
            except Exception as e:
                self.dialog_critical(str(e))

    def file_save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        save_dialog, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getSaveFileName()",
            "",
            "JSON (*.json)",
            options=options
        )
        with open(save_dialog, 'w') as f:
            json.dump(self.converter.excel_json, f, indent=4)

    def convert_file(self):
        if self.converter is not None:
            self.converter.convert()
            self.out_json = json.dumps(self.converter.excel_json, indent=4)
            self.fill_tree(self.tree_widget.invisibleRootItem(), self.converter.excel_json)