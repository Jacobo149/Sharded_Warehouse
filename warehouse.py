# Class to represent a warehouse.
class warehouse:
    def __init__(self, ID):
        self.ID = ID
        self.stock = {}

    def add_transaction(self, transaction):
        if transaction.item not in self.stock:
            self.stock[transaction.item] = [transaction.number, transaction.price]
        else:
            self.stock[transaction.item][0] += transaction.number


    def __str__(self):
        for item in self.stock:
            return f'{self.ID} {item} {self.stock[item][0]} {self.stock[item][1]}'