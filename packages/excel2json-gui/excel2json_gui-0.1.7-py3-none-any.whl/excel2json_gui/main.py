from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from excel2json_gui.gui import ExcelConverterGui
import sys

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Excel 2 JSON")

    
    window = ExcelConverterGui()
    # app.exec_()
    # window = ExcelConverterGui()
    # window.show()
    sys.exit(app.exec_())