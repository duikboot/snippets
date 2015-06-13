

class DoughFactory(object):
    """docstring for DoughFactory"""

    def get_dough(self):
        return 'insecticide treated wheat dough'


class Pizza(DoughFactory):

    """Docstring for Pizza. """


    def order_pizza(self, *toppings):
        print('getting dough')
        dough = super().get_dough()
        print('Making pie with %s' % dough)
        for topping in toppings:
            print('Adding: %s' % topping)


if __name__ == '__main__':
    Pizza().order_pizza('Pepperoni', 'Bell')
