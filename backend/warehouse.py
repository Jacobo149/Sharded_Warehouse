class Warehouse:
    def __init__(self, ID, shared_inventories, lock):
        self.ID = ID
        self.shared_inventory = shared_inventories  # Shared inventory from Manager
        self.lock = lock  # Lock for this warehouse's inventory

    def add_transaction(self, transaction):
        """Updates warehouse stock based on a new transaction."""
        with self.lock:  # Acquire lock before modifying the shared inventory
            if transaction.item not in self.shared_inventory:
                self.shared_inventory[transaction.item] = [transaction.number, transaction.price]
            else:
                self.shared_inventory[transaction.item][0] += transaction.number  # Increase quantity
    
    def process_transactions(self, queue):
        """Continuously processes transactions from the queue."""
        while True:
            transaction = queue.get()  # Wait for a transaction
            
            if transaction is None:
                break  # Exit loop if shutdown signal received

            print(f"Processing transaction {transaction.ID} in warehouse {self.ID}")
            self.add_transaction(transaction)  # Process the transaction
            print(f"Updated warehouse {self.ID} stock: {self.shared_inventory}")  # Debug log

    def __str__(self):
        """Returns a string representation of the warehouse inventory."""
        return f"Warehouse {self.ID} Inventory:\n" + "\n".join(
            f"{item}: {data[0]} units @ ${data[1]} each" for item, data in self.shared_inventory.items()
        )
