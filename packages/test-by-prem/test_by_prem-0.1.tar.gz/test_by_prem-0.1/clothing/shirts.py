from .Generalclothing import Clothing

class Shirt(Clothing):

    def __init__(self, price, size, material, color, type):
        Clothing.__init__(self, size, material, color, price)
        self.type = type

    def __repr__(self):
        return "Shirt{\n"\
                       "Price : " + str(self.price) +\
                        "\nType : " + self.type + \
                        "\nMaterial : " + self.material +\
                        "\nColor : " + self.color +\
                        "\nSize : " + self.size+\
                        "\n}"

    def increase_price(self, amount):
        self.price += amount
                    