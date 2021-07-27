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
    input = ""
    output = ""
    current_folder = ""

    def __init__(self):
        super(DataAnalyzer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.ui.pushButton.clicked.connect(self.start)
        self.ui.listWidget.clicked.connect(self.lv_date_action)
        self.ui.listWidget_2.clicked.connect(self.lv_pic_action)

    def start(self):
        self. input = self.ui.textEdit.toPlainText()
        self.output = self.ui.textEdit_2.toPlainText()
        items = process(self.input, self.output)
        self.ui.listWidget.addItems(
        items)

    def lv_pic_action(self):
        item = self.ui.listWidget_2.currentItem()
        pic_path = self.output + "/"+self.current_folder+"/"+item.text()
        print(pic_path)
        self.view_pic(pic_path)

    def lv_date_action(self):
        self.current_folder = self.ui.listWidget.currentItem().text()
        items = get_paths(self.ui.textEdit_2.toPlainText() +
                          "/"+self.current_folder, ".png")
        for item in items:
            self.ui.listWidget_2.addItem(Path(item).stem)

    def view_pic(self, path):
        pixmap = QPixmap(path)
        self.ui.label_3.setPixmap(pixmap)


app = QtWidgets.QApplication([])
application = DataAnalyzer()
application.show()

sys.exit(app.exec())
