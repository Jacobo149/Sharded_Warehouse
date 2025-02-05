# Class to hold non-processed transactions.
class TransactionPool:
    def __init__(self):
        self.pool = []

    def add_transaction(self, transaction):
        self.pool.append(transaction)

    def get_transactions(self):
        return self.pool
    
    def remove_transaction(self, transaction):
        self.pool.remove(transaction)
    
    def __str__(self):
        return '\n'.join([str(transaction) for transaction in self.pool])