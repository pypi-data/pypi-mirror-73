class Clothing:

    def __init__(self, size, material, color, price):
        self.price = price
        self.color = color
        self.material = material
        self.size = size

    def change_price(self, amount):
        self.price = amount

    def discounted_price(self, discount):
        return self.price(1- discount/100)