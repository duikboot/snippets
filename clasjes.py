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

    # def __new__(cls, c):
    #     self = object.__new__(cls)
    #     self.celsius = c
    #     return self

    def __init__(self, c):
        self._celsius = c

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


class TestClassVariables(object):
    """docstring for TestClassVariables"""
    def __init__(self, a, b):
        self.a, self.b = a, b
        


if __name__ == "__main__":
    c = Circle(10)
    print c

    d = Donut(100, 80)
    print d

    temperature = Temperature.from_celsius(10)
    print temperature

    kelvin = Temperature.from_kelvin(100)
    print kelvin

    fahrenheit = Temperature.from_fahrenheit(100)
    print fahrenheit

    stock = Stock("ACME")
    print stock.name
