
import sys

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QLabel

from Park import Park

if __name__ == '__main__':
    app = QApplication(sys.argv)

    park=Park()

    park.show()


    sys.exit(app.exec_())