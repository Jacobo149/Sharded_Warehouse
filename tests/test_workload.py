import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from backend.workload import Workload
from backend.sharded_warehouse_manager import ShardedWarehouseManager
import time

def test_workload_initialization():
    manager = ShardedWarehouseManager()
    # Create a workload
    workload = Workload(manager)

    # Test if the workload is initialized correctly
    assert workload.manager is not None

def test_generate_transactions():
    manager = ShardedWarehouseManager()
    # Create a workload
    workload = Workload(manager)

    # Generate transactions
    workload.generate_transactions()

    # Test if transactions were generated
    assert len(workload.manager.transaction_pool.pool) == 6

def test_process_transactions():
    manager = ShardedWarehouseManager()
    workload = Workload(manager)

    workload.generate_warehouses(3)
    workload.generate_transactions()
    workload.process_transactions()

    # Wait for transactions to be processed
    time.sleep(10)  # Adjusted sleep time to ensure all transactions are processed.

    # Test if transactions were processed
    assert len(workload.manager.get_processed_transactions()) == 6

def test_inventory_after_processing():
    manager = ShardedWarehouseManager()
    workload = Workload(manager)

    workload.generate_warehouses(3)  # Ensure warehouses are created before transactions
    workload.generate_transactions()
    workload.process_transactions()

    # Wait for processing
    time.sleep(5)  # Allow for processing and inventory updates

    # Check if warehouses contain processed transactions
    assert any(len(inventory) > 0 for inventory in manager.shared_inventories.values())

def test_kill_processes():
    manager = ShardedWarehouseManager()
    workload = Workload(manager)

    # Generate transactions
    workload.generate_transactions()

    # Process transactions
    workload.process_transactions()

    # Kill processes
    workload.kill_processes()

    # Test if processes were killed
    assert workload.manager.warehouses == {}  # Check if warehouses dict is empty
    assert dict(workload.manager.shared_inventories) == {}  # Ensure inventories are cleared
