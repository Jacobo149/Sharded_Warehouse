from transaction_pool import transaction_pool
from warehouse import warehouse
from transaction import transaction

class main:
    def __init__(self):
        self.transaction_pool = transaction_pool()
        self.warehouses = {}

    def create_warehouse(self, ID):
        self.warehouses[ID] = warehouse(ID)

    def create_transaction_pool(self):
        self.transaction_pool = transaction_pool()

    def create_transaction(self, ID, item, number, price, warehouse):
        self.transaction_pool.add_transaction(transaction(ID, item, number, price, warehouse))
        
    def process_transactions(self):
        for transaction in self.transaction_pool.get_transactions():
            self.warehouses[transaction.warehouse].add_transaction(transaction)
            self.transaction_pool.remove_transaction(transaction)


main = main()
main.create_warehouse(1)
main.create_warehouse(2)
main.create_transaction_pool()
main.create_transaction(1, 'apple', 10, 1, 1)
main.create_transaction(2, 'orange', 20, 2, 1)
main.create_transaction(3, 'apple', 5, 1, 1)
main.process_transactions()
print(main.warehouses[1])