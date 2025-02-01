# Class used to represent a transaction to be sent to shards.
class Transaction:
    def __init__(self, ID, item, number, price, warehouse):
        self.ID = ID
        self.item = item
        self.number = number
        self.price = price
        self.warehouse = warehouse

    def __str__(self):
        return f'{self.ID} {self.item} {self.number} {self.price} {self.warehouse}'