from multiprocessing import Process, Queue, Manager, Lock
from transaction_pool import transaction_pool
from warehouse import Warehouse
from transaction import Transaction
import time

class ShardedWarehouseManager:
    def __init__(self):
        self.transaction_pool = transaction_pool()
        self.warehouses = {}

        # Use multiprocessing Manager to store shared warehouse inventories
        self.manager = Manager()
        self.shared_inventories = self.manager.dict()  # This is shared across processes

    def create_warehouse(self, ID):
        """Creates a warehouse with a shared inventory dictionary and its own process."""
        queue = Queue()
        self.shared_inventories[ID] = self.manager.dict()  # Initialize shared inventory for warehouse
        lock = Lock()  # Create a lock for this warehouse's inventory
        warehouse = Warehouse(ID, self.shared_inventories[ID], lock)  # Pass the shared inventory
        process = Process(target=warehouse.process_transactions, args=(queue,))
        process.start()
        self.warehouses[ID] = (process, queue)

    def create_transaction(self, ID, item, number, price, warehouse_id):
        """Adds a transaction to the transaction pool."""
        self.transaction_pool.add_transaction(Transaction(ID, item, number, price, warehouse_id))

    def distribute_transactions(self):
        """Distributes transactions from the pool to the appropriate warehouse queues."""
        for transaction in self.transaction_pool.get_transactions()[:]:  # Copy to avoid mutation
            if transaction.warehouse in self.warehouses:
                print(f"Distributing transaction {transaction.ID} to warehouse {transaction.warehouse}")
                _, queue = self.warehouses[transaction.warehouse]
                queue.put(transaction)  # Send transaction to warehouse
                self.transaction_pool.remove_transaction(transaction)

    def shutdown(self):
        """Gracefully shuts down all warehouse processes."""
        for _, queue in self.warehouses.values():
            queue.put(None)  # Send shutdown signal
        for process, _ in self.warehouses.values():
            process.join()  # Wait for processes to exit

    def print_warehouses(self):
        """Prints the inventory of all warehouses."""
        for ID, inventory in self.shared_inventories.items():
            print(f"Warehouse {ID} Inventory:")
            if inventory:  # Check if the inventory is not empty
                for item, data in inventory.items():
                    print(f" - {item}: {data[0]} units @ ${data[1]} each")
            else:
                print(" - No inventory data found!")
            print()

# Example Execution
if __name__ == "__main__":
    manager = ShardedWarehouseManager()
    
    # Create warehouses (shards)
    manager.create_warehouse(1)
    manager.create_warehouse(2)

    # Add transactions to the transaction pool
    manager.create_transaction(1, 'apple', 10, 1, 1)
    manager.create_transaction(2, 'orange', 20, 2, 1)
    manager.create_transaction(3, 'apple', 5, 1, 1)
    manager.create_transaction(4, 'banana', 15, 1, 2)

    # Distribute transactions multiple times (simulating a periodic batch processing)
    for _ in range(3):
        manager.distribute_transactions()
        time.sleep(1)  # Simulate time delay for warehouse processing

    manager.shutdown()  # Shut down warehouse processes

    # Print warehouse inventory
    manager.print_warehouses()
