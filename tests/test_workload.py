from backend.workload import Workload
from backend.sharded_warehouse_manager import ShardedWarehouseManager
import time

def test_workload_initialization():
    manager = ShardedWarehouseManager()
    # Create a workload
    workload = Workload(manager)

    # Test if the workload is initialized correctly
    assert workload.manager is not None
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

    workload.generate_transactions()
    workload.process_transactions()

    # Wait for transactions to be processed
    time.sleep(2)  

    # Test if transactions were processed
    assert len(workload.manager.processed_transactions) == 6

def test_inventory_after_processing():
    manager = ShardedWarehouseManager()
    workload = Workload(manager)

    workload.generate_transactions()
    workload.process_transactions()

    # Wait for processing
    time.sleep(2)  

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

