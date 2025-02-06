from sharded_warehouse_manager import ShardedWarehouseManager
import time
import random

# Class to generate transactions and process them via Sharded Warehouse Manager.
class Workload:
    def __init__(self, manager):
        self.manager = manager

    def generate_warehouses(self, num_warehouses):
        """Generates a series of warehouses for testing."""
        for i in range(num_warehouses):
            self.manager.create_warehouse(i)

    def generate_transactions(self, num_transactions=6, num_warehouses=3):
        item_price_map = {'apple': 1.50, 'banana': 0.75, 'orange': 0.50}

        """Generates a series of transactions for testing."""
        # List of item names for easy selection
        items = list(item_price_map.keys())
        
        for i in range(num_transactions):
            # Randomly select an item from the list of keys
            item_select = random.choice(items)  # Choose a random item name
            self.manager.create_transaction(i, item_select, i + 1, item_price_map[item_select], i % num_warehouses)
            print(f"Created transaction {i} for {i + 1} {item_select} at warehouse {i % num_warehouses}")

    def process_transactions(self, num_iterations=6):
        """Distributes transactions to warehouses and processes them."""
        for _ in range(num_iterations):
            self.manager.distribute_transactions()
            time.sleep(1)  # Simulate time delay for warehouse processing
            print("Processed transactions:{}\n".format(self.manager.get_processed_transactions()))

    def kill_processes(self):
        """Shuts down all warehouse processes."""
        self.manager.shutdown()

    def print_inventory(self):
        """Prints the inventory of all warehouses."""
        self.manager.print_warehouses()

if __name__ == "__main__":
    manager = ShardedWarehouseManager()
    workload = Workload(manager)

    workload.generate_warehouses(3)
    workload.generate_transactions()
    workload.process_transactions(6)
    workload.print_inventory()
    workload.kill_processes()
