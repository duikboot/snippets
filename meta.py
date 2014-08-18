

class Meta(type):

    def __init__(self, name, base, atts):
        super(Meta, self).__init__(name, base, atts)
        print(name)


class Child(object):
    __metaclass__ = Meta

    def __init__(self):
        print ("me")


class newtype(type):

    def __new__(cls, name, bases, atts):
        clsobj = super(newtype, cls).__new__(cls, name, bases, atts)
        print clsobj.__name__
        print bases
        return clsobj


class Child2(object):
    __metaclass__ = newtype

    def __init__(self):
        print ("me")


def debugattr(cls):
    orig_getattribute = cls.__getattribute__

    def __getattribute__(self, name):
        print "Get: ", name
        return orig_getattribute(self, name)
    cls.__getattribute__ = __getattribute__

    return cls


@debugattr
class NewDict(dict):

    def __getattribute__(self, name):
        return dict.__getitem__(self, name)


@debugattr
class TryAttr(object):

    def __init__(self):
        self.value = {}

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __setitem__(self, name, value):
        self.value[name] = value


if __name__ == "__main__":

    print "instantiate child"
    a = Child()

    print "instantiate child2"
    a = Child2()
    d = NewDict(a=1)
    print d.a

    d = TryAttr()
    d["a"] = 3
