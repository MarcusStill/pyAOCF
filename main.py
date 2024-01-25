import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

from mainform import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.calculate)
        self.ui.pushButton_2.clicked.connect(self.clear)
        self.ui.pushButton_3.clicked.connect(self.close)
        self.ui.checkBox.stateChanged.connect(self.onStateChanged)
        self.ui.checkBox_2.stateChanged.connect(self.onStateChanged)
        self.ui.checkBox_3.stateChanged.connect(self.onStateChanged_2)
        self.ui.checkBox_4.stateChanged.connect(self.onStateChanged_2)

    def clear(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_16.clear()
        self.ui.lineEdit_17.clear()
        self.ui.lineEdit_5.setText('Введите данные для оценки риска ПОКД')
        self.ui.lineEdit_5.setStyleSheet('background-color: white;')
        self.ui.checkBox.setCheckState(Qt.Unchecked)
        self.ui.checkBox_2.setCheckState(Qt.Unchecked)
        self.ui.checkBox_3.setCheckState(Qt.Unchecked)
        self.ui.checkBox_4.setCheckState(Qt.Unchecked)

    def onStateChanged(self):
        if self.ui.checkBox.isChecked():
            self.ui.checkBox_2.setEnabled(False)
        else:
            self.ui.checkBox_2.setEnabled(True)
        if self.ui.checkBox_2.isChecked():
            self.ui.checkBox.setEnabled(False)
        else:
            self.ui.checkBox.setEnabled(True)

    def onStateChanged_2(self):
        if self.ui.checkBox_3.isChecked():
            self.ui.checkBox_4.setEnabled(False)
        else:
            self.ui.checkBox_4.setEnabled(True)
        if self.ui.checkBox_4.isChecked():
            self.ui.checkBox_3.setEnabled(False)
        else:
            self.ui.checkBox_3.setEnabled(True)

    def error_input(self):
        self.ui.lineEdit_5.setText('Недостаточно исходных данных!')
        self.ui.lineEdit_5.setStyleSheet('background-color: yellow;')

    def calculate(self):
        """ Функция производит определение принадлежности пожилых пациентов к группе
        высокого или низкого риска ухудшения когнитивной функции """
        result_1 = 'Высокий риск ПОКД'
        result_2 = 'Низкий риск ПОКД'
        constant = (0.822, 0.059, 0.186, 0.548, 0.004, 0.081, -0.869)
        try:
            # Продолжительность ИК (мин)
            pik = self.ui.lineEdit.text()
            if pik:
                pik: int = int(pik)
            else:
                self.error_input()
            # Дыхательная недостаточность
            if self.ui.checkBox.isChecked():
                dn: int = 1
            elif self.ui.checkBox_2.isChecked():
                dn: int = 0
            else:
                self.error_input()
            # Фибрилляция предсердия
            if self.ui.checkBox_3.isChecked():
                fp: int = 1
            elif self.ui.checkBox_4.isChecked():
                fp: int = 0
            else:
                self.error_input()
            # ФВлж
            fv = self.ui.lineEdit_16.text()
            if fv:
                fv: int = int(fv)
            else:
                self.error_input()
            # Hb - гемоглобин (г/л)
            hb = self.ui.lineEdit_17.text()
            if hb:
                hb: int = int(hb)
            else:
                self.error_input()
            score = (
                    constant[0] + (constant[1] * pik) + (constant[2] * dn) +
                    (constant[3] * fp) - (constant[4] * fv) - (constant[5] * hb)
            )

            if score > constant[6]:
                self.ui.lineEdit_5.setText(result_1)
                self.ui.lineEdit_5.setStyleSheet('background-color: red;')

            else:
                self.ui.lineEdit_5.setText(result_2)
                self.ui.lineEdit_5.setStyleSheet('background-color: green;')
        except Exception as e:
            self.error_input()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
