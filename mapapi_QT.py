import os
import sys
import requests
from PyQt5.QtCore import Qt
from geocoder import get_coordinates, geocode, get_nearest_object, postal_code
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from main_qt import Ui_MainWindow
from PIL import Image, ImageQt
from io import BytesIO
from PyQt5.QtGui import QPixmap

SCREEN_SIZE = [600, 450]
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ll = [float(input()), float(input())]
        self.spn = float(input())
        self.l = self.comboBox.currentText()
        self.comboBox.currentTextChanged.connect(
                    lambda: self.getImage(self.ll[0], self.ll[1], self.spn, self.comboBox.currentText())
                )
        self.pushButton.clicked.connect(self.add_point)
        self.pushButton_2.clicked.connect(self.del_point)
        self.pt = None
        self.getImage(self.ll[0], self.ll[1], self.spn, self.l)
        self.setWindowTitle('Отображение карты')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.spn += 0.1
        if event.key() == Qt.Key_PageUp:
            if self.spn - 0.1 > 0:
                self.spn -= 0.1
        if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            if self.ll[0] - self.spn * 4 > -180:
                self.ll[0] -= self.spn * 4
            else:
                self.ll[0] -= self.spn * 4
                self.ll[0] %= 180
        if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            if self.ll[0] + self.spn * 4 < 180:
                self.ll[0] += self.spn * 4
            else:
                self.ll[0] += self.spn * 4
                self.ll[0] %= 180
        if event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
            if self.ll[1] + self.spn * 1.5 < 80.0:
                self.ll[1] += self.spn * 1.5
            else:
                self.ll[1] += self.spn * 1.5
                self.ll[1] %= 80
        if event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
            if self.ll[1] - self.spn * 1.5 > -80:
                self.ll[1] -= self.spn * 1.5
            else:
                self.ll[1] -= self.spn * 1.5
                self.ll[1] %= 80
        self.getImage(self.ll[0], self.ll[1], self.spn, self.comboBox.currentText())

    def add_point(self):
        try:
            self.pt = get_coordinates(self.lineEdit.text())
            self.ll = self.pt[::]
            if self.checkBox.isChecked():
                adress = postal_code(self.pt)
            else:
                adress = ''
            self.getImage(self.ll[0], self.ll[1], self.spn, self.comboBox.currentText())
            self.statusbar.showMessage(geocode(self.lineEdit.text())['metaDataProperty']['GeocoderMetaData']['text']
                                       + ' ' + adress)
        except Exception:
            self.pt = None
            self.lineEdit.clear()

    def del_point(self):
        self.pt = None
        self.lineEdit.clear()
        self.getImage(self.ll[0], self.ll[1], self.spn, self.comboBox.currentText())

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
        if not self.pt:
            map_params = {
                "apikey": API_KEY,
                "ll": f'{ll_1},{ll_2}',
                "spn": f'{spn},{spn}',
                "l": l
            }
        else:
            map_params = {
                "apikey": API_KEY,
                "ll": f'{ll_1},{ll_2}',
                "spn": f'{spn},{spn}',
                "l": l,
                'pt': f'{self.pt[0]},{self.pt[1]},flag'
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
        self.label.setStyleSheet(f"border-image:url(map.png)")

        #self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))
        #self.label.setPixmap(QPixmap.fromImage(self.img))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = Example()
    ex.show()
    try:
        os.remove('map.png')
    except Exception:
        pass
    sys.exit(app.exec())

