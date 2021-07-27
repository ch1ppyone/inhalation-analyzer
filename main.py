import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
from ui import Ui_MainWindow
import sys
from analyse import process, get_paths
from pathlib import Path


class DataAnalyzer(QtWidgets.QMainWindow):
    current_date = ""
    input = ""
    output = ""

    def __init__(self):
        super(DataAnalyzer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.ui.pushButton.clicked.connect(lambda: self.start())
        self.ui.comboBox.activated.connect(self.cmb_action)
        self.ui.listWidget.clicked.connect(self.lv_action)

    def start(self):
        self. input = self.ui.textEdit.toPlainText()
        self.output = self.ui.textEdit_2.toPlainText()
        self.ui.comboBox.addItems(
            get_paths(self.ui.textEdit.toPlainText(),  ".LOG"))

    def lv_action(self):
        item = self.ui.listWidget.currentItem()
        pic_path = self.output + "/"+self.current_date+"/"+item.text()
        self.view_pic(pic_path)

    def cmb_action(self):
        current_file = str(self.ui.comboBox.currentText())
        self.current_date = process(self.input+"/" +
                                    current_file, self.output)
        items = get_paths(self.ui.textEdit_2.toPlainText() +
                          "/"+self.current_date, ".png")
        for item in items:
            self.ui.listWidget.addItem(Path(item).stem)

    def view_pic(self, path):
        pixmap = QPixmap(path)
        self.ui.label_3.setPixmap(pixmap)


app = QtWidgets.QApplication([])
application = DataAnalyzer()
application.show()

sys.exit(app.exec())
