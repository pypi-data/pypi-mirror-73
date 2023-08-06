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

        open_base64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB90lEQVRo3u2WsWtTQRzHP79rFTEmtBS6iJpGhI7iJNSpVAQnJ3enYuof0K26dXGzxUxuLoKrYBscxHbSzcGgTZwEEZTEtKK++7m0WPMacmds7gXvM727d+/e98N9HzyIRCKRyP+MHDRZrDSnxcoyyiyQ99pQubO1kL8dTKBYaU5LIpvA2F9vOkAJk3q5leV+wgOosFRaaYUR2K1N3wxKIlWhqdWWHvZLHWkJVBVdrJcLb7otMj47Dpi8wjWQzbMr26eGUWCPcSvJ3WEWALjS7cZoryfr5bz0WhOSYTmBKJBZen4DnUyttmrAudDBLebq+3LuidcJlCo7p7MQHvh+QtvPwbNC+vPH5dDJd9l4vTD51VtAROZCJwdAWd+7dBdQFeXf/Oj1jbFr3gJn7m+fByZDZwe+1CcKL70FjCbZqA9UuS6JtwBko//K7/47CxQf6DHgUujwAKMjydr+sZOAabdngOOhw4M03s6PvfMWsEIm6gP6tHPGSUCwGRH4s/9OAifvNScQuRA6OWCPjOgzb4GjRmZd1h06qq9q84VP3gKQjf4rZv2g+aERMIqzQLNjXAodHtixudwLJwFRqqHTptFHjRvyzUkA1UXgc+jI+/igkix1u5kS2LpVqInViwqPSddpkHxUeGiTZKZxc7wRMEckEolEMswvAVaJ4cAPpCwAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMDctMDdUMTg6NDU6MjYrMDA6MDALUq1WAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTA3LTA3VDE4OjQ1OjI2KzAwOjAweg8V6gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="
        open_file_action = QAction(
            QIcon(self.create_image_from_base64(open_base64)), "Open file...", self)
            # QIcon(self.script_dir.split('/')[-1] + '/images/folder-open-big.png'), "Open file...", self)
            # QIcon(os.path.join('excel2json_gui/images', 'folder-open-big.png')), "Open file...", self)
            # QIcon(os.path.join(self.script_dir, '../images/folder-open-big.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        # convert_action = QAction(QIcon(os.path.join('excel2json_gui/images', 'convert-big.png')), "Convert Excel to JSON", self)
        convert_base64 = "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"
        convert_action = QAction(QIcon(self.create_image_from_base64(convert_base64)), "Convert Excel to JSON", self)
        # convert_action = QAction(QIcon(self.script_dir.split('/')[-1] + '/images/convert-big.png'), "Convert Excel to JSON", self)
        # convert_action = QAction(QIcon(os.path.join(self.script_dir, '../images/convert-big.png')), "Convert Excel to JSON", self)
        convert_action.setStatusTip("Convert the Excel file")
        convert_action.triggered.connect(self.convert_file)
        file_menu.addAction(convert_action)
        file_toolbar.addAction(convert_action)

        # save_file_action = QAction(QIcon(os.path.join('excel2json_gui/images', 'save-big.png')), "Save", self)
        save_base64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB/klEQVRo3u2ZsWsTURzHv9/fxcZCHZyLuwjFjF2tvUSoU0s62M6dujm0mzqpk6CTCm5FuHQM2LvUPyCbBRHcdSxiHULEu5+DUkr1ci/NS94F3mdL3pf3+37uHXeQAB6Px+MSDlrcr8fXMwaPCdwGcGW8TfRR8yB8aE3gbT2+VmFwBODqWIuPKCF5CwGDZxMtDwDKB607HTsCBOoTLX9BidxbqNU41LOfm/Eyi7cz5/z+/+FpM17eLdpHigIO2Wk1Dp9Ms4CRRNkFCiWmQQAAdqZdIBcv4JqKadDgue2EqT8BL+AaL+AaL+CacQj0oXhOlcWepnM9TeeosgjyBYC+7WHGLzIjFF8DyspqsnR0bqULoBuFyRtS2iDmbY20eQL9gLKyGv9T/pT1Tv2DanYXFk/CnoDi5aDyZyUIfV06ASX3TLMUGGcnJoC+fDKNpr3Kx/IJDMHP2Z61ufYEqtkN0+gsLhlnJyZAYtM0qxk2SicA1a0oTGpFsShMagpulU8AqJLSHiQRhUmNlDaAGVtD7b6JiXlSuvuNzisK9k6fNpfTBVG99/fKWytfJPADF/tPYEbBbc2wzWr65xsFFCP9tPo9byH3FlLgvc0rNRqMhxYAZRfAN9fVARyLyP2hBdYPlj7/0vQmgBaAEwfFTwBGIkFt7d2tLw7mezwejwG/AT3UjuaEFYGgAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIwLTA3LTA3VDE5OjQ0OjQ3KzAwOjAwWR4d3gAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMC0wNy0wN1QxOTo0NDo0NyswMDowMChDpWIAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC"
        save_file_action = QAction(QIcon(self.create_image_from_base64(save_base64)), "Save", self)
        # save_file_action = QAction(QIcon(self.script_dir.split('/')[-1] + '/images/save-big.png'), "Save", self)
        # save_file_action = QAction(QIcon(os.path.join(self.script_dir, '../images/save-big.png')), "Save", self)
        save_file_action.setStatusTip("Save JSON")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)
        self.icon_json_dict = self.create_image_from_base64("iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACQUlEQVRo3u2ZwU7UUBSG/9OZItJQHIk7WbOUvWwYzBh2GpVNYeUTGDY8ghvDE7gwUknwAQwmM7jQsIUla9yZAeyEAqbtcWFMOrfM2NM7tRjvt+v0ns7/397pPX8HMBgMhiqhIkWtrXAmTniDQS2AJ9PnOp4z9JpN/4wVCT2A25zE67ur7qFUi1VEfJTwPgNPVPHF4EkAj8iq7bW2wpnSDcQJbwC4rS88QyNK+FXpBn4tm9J4KC2oy79DtuZV1PHKb8KVqhHfgeuGMVA1xkDVGANVIzLwYPt4qmxB919/E7UnIgNxNC7eKaWM35xYLMXA4ptgmjjTq3zXl0y99BEzvZz3TxsjM7C02XUX3oXLXK/tA7jbd5J5R98At5XjWRv2QdMPny1tdv/YWgzsY7J9e4ZuwjT3aWXiq478hbfBLFm1PQBDZ31Qz1XkKRSAeXsU4gFgd9U9rFt0D8B7AIG0voABIhCNEUeOrvi+qwIWQOKEWMCAXoJS0U14Aw10PIc6nkOXF6FLhMcAqXm1UIJSuSrhMXDERE8vL0L3t45B9blv2bx/2rBhHxCQnvWg4zlam1vTD4P0zDNwNGZHczvLU8d56nMvoc/erRMCrSkfixNUFmXZEL3IK15kAABu8PkInvvD+XF+9lEyXmTgw8q0+DEn5cvzOz3J+P+rG72OGANVYwxUzT9voMC7Ueqld081N8j/H+hDnPCKdKNteU3eS8sTnvz1ehKvAzgpQX43gbUmLRIb0E1QVzDShGcwGAx/l59oc8zr2HyODwAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMC0wNy0wN1QyMjowNzo1MiswMDowMAfKYB4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjAtMDctMDdUMjI6MDc6NTIrMDA6MDB2l9iiAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==")
        self.icon_json_list = self.create_image_from_base64("iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAeElEQVRo3u3YsQ2AMAwAwYDo2Io1mC9rsBU1VJQocWFeEX81WHoSGpciSfqzqfXAVs+rZ9Cxr81ZGXPnzK/zBQNoS/SF6F2Pzun9Nx7Dn4ABNANoBtAMoBlAM4BmAM0AmgE0A2gG0MJ7obe9TdZutGX4EzBAkiTSDXCgFEREebHRAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIwLTA3LTA3VDIyOjA5OjMzKzAwOjAweRtSngAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMC0wNy0wN1QyMjowOTozMyswMDowMAhG6iIAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC")
        self.icon_json_str = self.create_image_from_base64("iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVRIx2NgGAWjgFLAiEtiaunZ/6QYlN1tjNUsJlr7YNSCUQtGLRgOFoyCUUA5AAAbpwQYNZm2LgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMC0wNy0wN1QyMjoxNjo1NSswMDowMOwh6m4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjAtMDctMDdUMjI6MTY6NTUrMDA6MDCdfFLSAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==")
        self.icon_json_int = self.create_image_from_base64("iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMUlEQVRIx2NgGAWjgFLAiEui+7DXf1IMKrXdhtUsJlr7YNSCUQtGLRgOFoyCUUA5AAAP1wQYeDbx4AAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMC0wNy0wN1QyMjoxNzo1MiswMDowMMZEv94AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjAtMDctMDdUMjI6MTc6NTIrMDA6MDC3GQdiAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAABJRU5ErkJggg==")
        self.icon_json_bool = self.create_image_from_base64("iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAMElEQVRIx2NgGAWjgFLAiEvi/8ey/yQZxN+F1SwmWvtg1IJRC0YtGA4WjIJRQDkAADZ3BBik8By9AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIwLTA3LTA3VDIyOjE3OjMyKzAwOjAwACu2WQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMC0wNy0wN1QyMjoxNzozMiswMDowMHF2DuUAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC")

        self.show()

    def create_image_from_base64(self, b64_str):
        pixmap = QPixmap()
        byte_arr = QByteArray.fromBase64(bytearray(b64_str.encode('utf-8')))
        pixmap.loadFromData(byte_arr, 'PNG')
        return pixmap


    def get_image_path(self, var):
        # relative_path = f"/images/{type(var).__name__}.png"
        image = f"{type(var).__name__}.png"
        return image
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
                icon = QIcon(getattr(self, f"icon_json_{type(val).__name__}"))
                # icon = QIcon(self.icon_json_object)
                # icon = QIcon(self.get_image_path(val))
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
                icon = QIcon(getattr(self, f"icon_json_{type(val).__name__}"))
                # icon = QIcon(self.get_image_path(val))
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
            icon = QIcon(getattr(self, f"icon_json_{type(value).__name__}"))
            # icon = QIcon(self.get_image_path(value))
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