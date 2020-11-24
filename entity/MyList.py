from entity.Car import Car


class MyList(list):
    def __init__(self, N):
        list.__init__([])
        self.max_size = N
        self.now_size = 0
        self.cars = []

    def push(self, car: Car):
        if self.now_size >= self.max_size:
            return False
        # self.cars[self.now_size] = car
        self.cars.append(car)
        self.now_size += 1
        # 进停车场

        return True

    def pop(self) -> Car:
        if self.now_size <= 0:
            return None
        self.now_size -= 1
        car = self.cars[self.now_size]
        self.cars.pop()  # 去除最后一个
        return car

    def is_full(self):
        if self.now_size >= self.max_size:
            return True
        return False

    def is_empty(self):
        if self.now_size == 0:
            return True
        return False

    def get(self, index):
        return self.cars[index]
