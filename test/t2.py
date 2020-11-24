import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QDialog


class First(QMainWindow):

    def __init__(self,app):
        super().__init__()
        self.app=app

        self.initUI()

    def initUI(self):
        self.btn = QPushButton("Button", self)
        self.btn.move(30, 50)
        self.btn.clicked.connect(self.bt_click)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Event sender')
        self.show()

    def bt_click(self):
        app=self.app
        b=Second()
        b.show()
        pass

        # print("hello")



class Second(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Get sender')

# def bt_click():
#     print("aaa")
#     b.show()
#     a.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = First(app)
    # b = Second()
    a.show()
    # a.btn.clicked.connect(b.show)
    # a.btn.clicked.connect(bt_click)
    sys.exit(app.exec_())