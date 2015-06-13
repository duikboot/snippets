

class Adam(object):
    def get_age(self):
        return 99


class Eve(object):
    def get_age(self):
        return 99


class August(Adam, Eve):
    def get_age(self):
        return super().get_age()


class Klara(Adam, Eve):
    def get_age(self):
        return super().get_age()


class Ingrid(August, Klara):
    def get_age(self):
        return super().get_age()


class Gudrun(August, Klara):
    def get_age(self):
        return super().get_age()


class Udo(August, Klara):
    def get_age(self):
        return super().get_age()


class Pake(Adam, Eve):
    def get_age(self):
        return super().get_age()


class Beppe(Adam, Eve):
    def get_age(self):
        return super().get_age()


class Klaas(Pake, Beppe):
    def get_age(self):
        return super().get_age()


class Arjen(Klaas, Gudrun):
    def get_age(self):
        return super().get_age()


class Margo(Klaas, Gudrun):
    def get_age(self):
        return super().get_age()


class Karin(Adam, Eve):
    def get_age(self):
        return super().get_age()


class Kid(Arjen, Karin):
    def get_age(self):
        return super().get_age()
