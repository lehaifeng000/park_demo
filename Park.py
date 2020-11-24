from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QTextEdit, QDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QSequentialAnimationGroup
import time

from entity.MyList import MyList
from entity.MyQueue import MyQueue
from entity.Car import Car

# 停车起始位置
POS_X = 300
POS_Y = 10
# 临时停车起始位置
POS_TMP_X = 200
POS_TMP_Y = 10
# 排队起始位置
POS_Q_X = 100
POS_Q_Y = 200
# 横向移动y
MOVE_Y = 300
# 出口x
OUT_X = 600
# 车距
DISTANCE = 10
# 车大小
SHAPE = 30

# 车库大小
N = 4


class Park(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        self.cars = MyList(N)
        self.wait_cars = MyQueue(N)
        self.tmp_cars = MyList(N)

        self.la = self.layout()
        bbb = 1

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        # self.setGeometry(shape)
        self.setWindowTitle('停车场模拟程序')

        # 进车按钮
        self.bt1 = QPushButton("进车", self)
        self.bt1.setGeometry(20, 60, 80, 30)
        self.bt1.clicked.connect(self.click_in)

        # 输入框
        self.ed1 = QTextEdit(parent=self)
        self.ed1.setPlaceholderText("汽车下标")
        self.ed1.setGeometry(20, 160, 80, 30)

        # 出车按钮
        self.bt2 = QPushButton("出库", self)
        self.bt2.setGeometry(20, 200, 80, 30)
        self.bt2.clicked.connect(self.click_out)

        # 阴影
        self.lb1= QLabel(text="等待区",parent=self)
        self.lb1.setGeometry(POS_Q_X,0,100,30)
        self.lb2 = QLabel(text="临时停车区", parent=self)
        self.lb2.setGeometry(POS_TMP_X, 0, 100, 30)
        self.lb3 = QLabel(text="停车场", parent=self)
        self.lb3.setGeometry(POS_X, 0, 100, 30)
        self.lb4 = QLabel(text="入口", parent=self)
        self.lb4.setGeometry(POS_X, MOVE_Y+10, 100, 30)

        self.lb5=QLabel(text="停车费", parent=self)
        self.lb5.setGeometry(400, 100, 100, 30)
        self.lb_fare=QLabel(text="0 元", parent=self)
        self.lb_fare.setGeometry(400, 150, 100, 30)



        #
        # self.lb1 = Car(self, POS_Q_X, 0)
        # self.lb1.init()
        # self.lb1.setPixmap(QPixmap('images/car-blue.png'))
        # self.lb1.setText("hello")

    def car_in(self):
        # car = Car(self, POS_Q_X, 0)
        # self.la.addWidget(car)

        # ret = self.cars.push(car)
        # 直接进入停车场
        # print(ret)

        if not self.cars.is_full():
            car = Car(self, POS_Q_X, 0)
            self.la.addWidget(car)
            self.cars.push(car)
            a1 = self.move_animation(car, POS_Q_X, 0, POS_Q_X, MOVE_Y)
            # a1.start()
            a2 = self.move_animation(car, POS_Q_X, MOVE_Y, POS_X, MOVE_Y)
            # 计算队伍位置
            y = POS_Y + (self.cars.now_size - 1) * (DISTANCE + SHAPE)
            a3 = self.move_animation(car, POS_X, MOVE_Y, POS_X, y)
            car.px = POS_X
            car.py = y
            aq = QSequentialAnimationGroup(parent=self)
            aq.addAnimation(a1)
            aq.addAnimation(a2)
            aq.addAnimation(a3)
            aq.start()
            # print("动画")
        elif not self.wait_cars.is_full():
            car = Car(self, POS_Q_X, 0)
            self.la.addWidget(car)
            self.wait_cars.push(car)
            # 进入排队
            y = POS_Q_Y - (self.wait_cars.now_size - 1) * (DISTANCE + SHAPE)
            a1 = self.move_animation(car, POS_Q_X, 0, POS_Q_X, y)
            car.px = POS_Q_X
            car.py = y
            aq = QSequentialAnimationGroup(parent=self)
            aq.addAnimation(a1)
            aq.start()

    def car_out(self, index):
        if index < self.cars.now_size:
            aq = QSequentialAnimationGroup(parent=self)
            for i in range(index + 1, self.cars.now_size):
                car = self.cars.pop()
                self.tmp_cars.push(car)
                a1 = self.move_animation(car, POS_X, car.py, POS_X, MOVE_Y)
                a2 = self.move_animation(car, POS_X, MOVE_Y, POS_TMP_X, MOVE_Y, 0.4)
                y = POS_TMP_Y + (self.tmp_cars.now_size - 1) * (DISTANCE + SHAPE)
                a3 = self.move_animation(car, POS_TMP_X, MOVE_Y, POS_TMP_X, y)
                car.px = POS_TMP_X
                car.py = y
                # aq = QSequentialAnimationGroup(parent=self)
                aq.addAnimation(a1)
                aq.addAnimation(a2)
                aq.addAnimation(a3)
            car = self.cars.pop()
            # 计算车费
            self.lb_fare.setText(str(round(car.cost(),2))+" 元")
            a1 = self.move_animation(car, POS_X, car.py, POS_X, MOVE_Y)
            a2 = self.move_animation(car, POS_X, MOVE_Y, OUT_X, MOVE_Y)
            aq.addAnimation(a1)
            aq.addAnimation(a2)
            # 返回
            for i in range(self.tmp_cars.now_size):
                car = self.tmp_cars.pop()
                self.cars.push(car)
                a1 = self.move_animation(car, POS_TMP_X, car.py, POS_TMP_X, MOVE_Y)
                a2 = self.move_animation(car, POS_TMP_X, MOVE_Y, POS_X, MOVE_Y, 0.4)
                y = POS_Y + (self.cars.now_size - 1) * (DISTANCE + SHAPE)
                a3 = self.move_animation(car, POS_X, MOVE_Y, POS_X, y)
                car.px = POS_X
                car.py = y
                aq.addAnimation(a1)
                aq.addAnimation(a2)
                aq.addAnimation(a3)
            if not self.wait_cars.is_empty():
                car = self.wait_cars.pop()
                self.cars.push(car)
                car.clear_cost()
                a1 = self.move_animation(car, POS_Q_X, car.py, POS_Q_X, MOVE_Y, 0.4)
                a2 = self.move_animation(car, POS_Q_X, MOVE_Y, POS_X, MOVE_Y)
                y = POS_Y + (self.cars.now_size - 1) * (DISTANCE + SHAPE)
                a3 = self.move_animation(car, POS_X, MOVE_Y, POS_X, y)
                car.px = POS_X
                car.py = y
                aq.addAnimation(a1)
                aq.addAnimation(a2)
                aq.addAnimation(a3)
                for i in range(self.wait_cars.now_size):
                    # print(self.wait_cars.now_size,len(self.wait_cars))
                    car = self.wait_cars.get(i)
                    y = car.py + (DISTANCE + SHAPE)
                    a1 = self.move_animation(car, POS_Q_X, car.py, POS_Q_X, y,0.5)
                    car.py = y
                    aq.addAnimation(a1)

            aq.start()

    def move_in(self, car):
        pass
        # self.aq = QSequentialAnimationGroup(self)
        # a1 = self.move_animation(car, 100, 400, 1)
        # a2 = self.move_animation(car, 400, 400, 1)
        # self.aq.addAnimation(a1)
        # self.aq.addAnimation(a2)
        # self.aq.start()

    def move_animation(self, car, x1, y1, x2, y2, cost=1):
        animation = QPropertyAnimation(self, propertyName=b'pos')
        animation.setParent(self)
        animation.setTargetObject(car)
        animation.setDuration(cost * 1000)
        animation.setStartValue(QPoint(x1, y1))
        animation.setEndValue(QPoint(x2, y2))
        # animation.start()
        return animation

    def move_to_park(self):
        pass

    def move_out(self, car):
        pass

    def click_in(self):
        # self.lb1.move(self.lb1.x()+10,self.lb1.y()+10)
        # self.move_in(self.lb1)
        self.car_in()

    def click_out(self):
        str1 = self.ed1.toPlainText()
        if str1 is not None:
            try:
                t = int(str1)
                if t>=self.cars.now_size:
                    return
                self.car_out(t)
            except Exception:
                pass
