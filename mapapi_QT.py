import os
import sys
from io import BytesIO
import requests
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from main_qt import Ui_MainWindow

SCREEN_SIZE = [600, 450]
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ll = float(input()), float(input())
        self.spn = float(input())
        self.getImage()

        self.label.setStyleSheet(f"border-image:url(map.png)")
        self.setWindowTitle('Отображение карты')


    def getImage(self):

        map_request = "http://static-maps.yandex.ru/1.x/"
        map_params = {
            "apikey": API_KEY,
            "ll": f'{self.ll[0]},{self.ll[1]}',
            "spn": f'{self.spn},{self.spn}',
            "l": 'map'
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    os.remove('map.png')
    sys.exit(app.exec())

