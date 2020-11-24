import time
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint


class Car(QLabel):

    def __init__(self, parent, px, py):
        super().__init__(parent=parent)
        # self.setParent(parent)
        self.setPixmap(QPixmap('images/car-blue.png'))
        self.in_time = time.time()
        self.setGeometry(px, py, 64, 64)
        self.px = px
        self.py = py
        # self.is_move=False

    def cost(self):
        out_time = time.time()
        return out_time - self.in_time
    def clear_cost(self):
        self.in_time=time.time()

