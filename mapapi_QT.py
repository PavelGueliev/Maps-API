import os
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from main_qt import Ui_MainWindow

SCREEN_SIZE = [600, 450]
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ll = [float(input()), float(input())]
        self.spn = float(input())
        self.l = self.buttonGroup.checkedButton().text()
        self.radioButton.clicked.connect(
                    lambda: self.getImage(self.ll[0], self.ll[1], self.spn, self.buttonGroup.checkedButton().text())
                )
        self.radioButton_2.clicked.connect(
                    lambda: self.getImage(self.ll[0], self.ll[1], self.spn, self.buttonGroup.checkedButton().text())
                )
        self.radioButton_3.clicked.connect(
                    lambda: self.getImage(self.ll[0], self.ll[1], self.spn, self.buttonGroup.checkedButton().text())
                )

        self.getImage(self.ll[0], self.ll[1], self.spn, self.l)
        self.setWindowTitle('Отображение карты')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn += 1
        elif event.key() == Qt.Key_PageDown:
            if self.spn - 1 > 0:
                self.spn -= 0.01
        elif event.key() == Qt.Key_A:
            self.ll[0] -= 0.01
        elif event.key() == Qt.Key_D:
            self.ll[0] += 0.01
        elif event.key() == Qt.Key_W:
            self.ll[1] += 0.01
        elif event.key() == Qt.Key_S:
            self.ll[1] -= 0.01
        self.getImage(self.ll[0], self.ll[1], self.spn, self.buttonGroup.checkedButton().text())

    def getImage(self, ll_1, ll_2, spn, l):
        try:
            os.remove('map.png')
        except Exception:
            pass
        if l == 'схема':
            l = 'map'
        elif l == 'спутник':
            l = 'sat'
        elif l == 'гибрид':
            l = 'sat,skl'
        map_request = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "apikey": API_KEY,
            "ll": f'{ll_1},{ll_2}',
            "spn": f'{spn},{spn}',
            "l": l
        }
        response = requests.get(map_request, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        print(self.spn)
        self.label.setStyleSheet(f"border-image:url(map.png)")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Example()
    ex.show()
    os.remove('map.png')
    sys.exit(app.exec())

