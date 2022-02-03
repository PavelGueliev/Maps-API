import sys
from io import BytesIO

import requests
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
SCREEN_SIZE = [600, 450]
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.ll = float(input()), float(input())
        self.spn = float(input())
        self.getImage()
        self.initUI()

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

        self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        # Изображение
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap.fromImage(self.img))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_PageUp:
            self.spn += 0.01
        if event.key() == Qt.Key_PageDown:
            self.spn -= 0.01




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
