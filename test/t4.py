import sys

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListView, QMainWindow, QVBoxLayout, QTableView, QLabel
from PyQt5.QtCore import QStringListModel,QPropertyAnimation,QPropertyAnimation, QSequentialAnimationGroup, QRect, QAbstractAnimation, QPoint
from PyQt5.QtGui import QStandardItemModel,QStandardItem,QPixmap

class Page(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        car=QLabel(self)
        # self.car_label=[]
        # self.car_label.append(car)
        img=QPixmap('../images/car-blue.png')
        car.setPixmap(img)
        car.setGeometry(100,100,64,63)
        # self.car_label[0].setPixmap(img)
        # self.car_label[0].setGeometry(100,100,64,63)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Event sender')
        self.show()
        self.move(car,1,1)

        # print("hello")
    def move(self,car,px,py):
        animation = QPropertyAnimation(self, b'pos')
        animation.setParent(self)
        animation.setDuration(2000)
        animation.setTargetObject(car)
        animation.setStartValue(QPoint(100,100))
        animation.setEndValue(QPoint(100, 400))
        animation.setLoopCount(1)
        # self.animation.finished.connect(self.animationFinished)
        animation.start()

if __name__ == '__main__':
    # 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。

    p=Page()
    p.show()


    # 系统exit()方法确保应用程序干净的退出
    # 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())