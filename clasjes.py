import math


class Circle(object):

    __slots__ = ['diameter']

    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self.diameter / 2.0

    @radius.setter
    def radius(self, radius):
        self.diameter = radius * 2.0

    def area(self):
        return self.radius ** 2 * math.pi

    def __repr__(self):

        return "%s has area %s" % (
            self.__class__.__name__, self.area()
        )


class Donut(Circle):
    """Yummie"""
    def __init__(self, outer, inner):
        super(Donut, self).__init__(outer)
        self.inner = inner

    def area(self):
        outer, inner = self.radius, self.inner
        return Circle(outer).area() - Circle(inner).area()


class Temperature(object):

    __slots__ = []

    def __new__(cls, c):
        cls.celsius = c
        self = object.__new__(cls)
        return self

    @classmethod
    def from_celsius(cls, c):
        return cls(c)

    @classmethod
    def from_kelvin(cls, kelvin):
        celsius = -273.15 + kelvin
        return cls(celsius)

    @classmethod
    def from_fahrenheit(cls, f):
        celsius = (f - 32) * 5/9.0
        return cls(celsius)

    def _to_kelvin(self):
        return self.celsius + 273.15

    def _to_fahrenheit(self):
        return self.celsius * 9/5.0 + 32

    def __repr__(self):
        return "celsius: {0:.2f}\nkelvin: {1:.2f}\nfahrenheit: {2:.2f}".format(
            self.celsius,
            self.kelvin,
            self.fahrenheit
        )

    @property
    def celsius(self):
        return self._celsius

    @property
    def fahrenheit(self):
        return self._to_fahrenheit()

    @property
    def kelvin(self):
        return self._to_kelvin()


class Structure(object):
    _fields = []

    def __init__(self, *args):
        # for name, val in zip(self._fields, args):
        for name, val in zip(self.__class__._fields, args):
            setattr(self, name, val)


class Stock(Structure):
    _fields = ['name', 'shares', 'price']


class Point(Structure):
    _fields = ['x', 'y']


class Address(Structure):
    _fields = ['hostname', 'port']


class MyDict(object):
    """docstring for MyDict"""
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)
        self._update = 1

    def update(self, iterable):
        print(self.__class__.__name__ + " update")
        for item in iterable:
            self.items_list.append(item)

    __update = update


class MyDict2(MyDict):

    def update(self, iterable):
        print(self.__class__.__name__ + " update")

        for item in iterable:
            self.items_list.insert(0, item)


if __name__ == "__main__":
    circle = Circle(10)
    print(circle)

    d = Donut(100, 80)

    temperature = Temperature.from_celsius(10)
    print(temperature)

    kelvin = Temperature.from_kelvin(100)
    print(kelvin)

    fahrenheit = Temperature.from_fahrenheit(100)
    print(fahrenheit)

    stock = Stock("ACME")
    print(stock.name)
