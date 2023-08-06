from .Generalclothing import Clothing

class Pant(Clothing):

    def __init__(self, size, material, color, price, length):
        Clothing.__init__(self, size, material, color, price)
        self.length = length

    def __repr__(self):
        return "Shirt{\n"\
                       "Price : " + str(self.price) +\
                        "\nMaterial : " + self.material +\
                        "\nColor : " + self.color +\
                        "\nSize : " + self.size+\
                        "\nLength : " + self.length+\
                        "\n}"    

    def double_price(self):
        self.price *= 2