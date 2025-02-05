from sharded_warehouse_manager import ShardedWarehouseManager
import time

# Class to generate transactions and process them via Sharded Warehouse Manager.
class Workload:
    def __init__(self, manager):
        self.manager = manager

    def generate_transactions(self):
        """Generates a series of transactions for testing."""
        self.manager.create_warehouse(1)
        self.manager.create_warehouse(2)
        self.manager.create_warehouse(3)

        self.manager.create_transaction(1, "apple", 5, 1.50, 1)
        self.manager.create_transaction(2, "banana", 10, 0.75, 2)
        self.manager.create_transaction(3, "orange", 15, 0.50, 3)
        self.manager.create_transaction(4, "apple", 2, 1.50, 2)
        self.manager.create_transaction(5, "banana", 4, 0.75, 3)
        self.manager.create_transaction(6, "orange", 6, 0.50, 1)

    def process_transactions(self):
        """Distributes transactions to warehouses and processes them."""
        for _ in range(6):
            self.manager.distribute_transactions()
            time.sleep(1)  # Simulate time delay for warehouse processing

    def kill_processes(self):
        """Shuts down all warehouse processes."""
        self.manager.shutdown()

    def print_inventory(self):
        """Prints the inventory of all warehouses."""
        self.manager.print_warehouses()

# Example Execution
if __name__ == "__main__":
    manager = ShardedWarehouseManager()
    workload = Workload(manager)

    workload.generate_transactions()
    workload.process_transactions()
    workload.kill_processes()
    workload.print_inventory()
