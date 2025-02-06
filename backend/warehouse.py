class Warehouse:
    def __init__(self, ID, shared_inventories, lock, processed_transactions):
        self.ID = ID
        self.shared_inventory = shared_inventories  # Shared inventory from Manager
        self.lock = lock  # Lock for this warehouse's inventory
        self.processed_transactions = processed_transactions  # Store processed transactions

    def add_transaction(self, transaction):
        # Updates warehouse stock based on a new transaction.
        with self.lock:  # Acquire lock before modifying the shared inventory
            if transaction.item not in self.shared_inventory:
                self.shared_inventory[transaction.item] = [transaction.number, transaction.price]
            else:
                # Create a new list and reassign it to avoid issues with Manager().dict()
                current_quantity, price = self.shared_inventory[transaction.item]
                self.shared_inventory[transaction.item] = [current_quantity + transaction.number, price]

        
    def process_transactions(self, queue):
        while True:
            transaction = queue.get()
            if transaction is None:
                break  # Shutdown signal

            print(f"Processing transaction {transaction.ID} in warehouse {self.ID}")
            self.add_transaction(transaction)

            # Append to the shared list to track processing order
            self.processed_transactions.append(transaction)

            print(f"Updated warehouse {self.ID} stock: {self.shared_inventory}")

    def __str__(self):
        """Returns a string representation of the warehouse inventory."""
        return f"Warehouse {self.ID} Inventory:\n" + "\n".join(
            f"{item}: {data[0]} units @ ${data[1]} each" for item, data in self.shared_inventory.items()
        )
