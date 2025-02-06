import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from backend.sharded_warehouse_manager import ShardedWarehouseManager

def test_warehouse_manager_initialization():
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Test if attributes are set correctly
    assert warehouse_manager.transaction_pool.pool == []
    assert warehouse_manager.warehouses == {}
    assert dict(warehouse_manager.shared_inventories) == {}
    assert list(warehouse_manager.processed_transactions) == []

def test_create_warehouse():
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Create a warehouse
    warehouse_manager.create_warehouse(1)

    # Test if the warehouse was created
    assert 1 in warehouse_manager.warehouses
    assert 1 in warehouse_manager.shared_inventories

def test_create_transaction():
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Create a transaction
    warehouse_manager.create_transaction(1, "item", 10, 5, 1)

    # Test if the transaction was added to the pool by comparing attributes
    assert len(warehouse_manager.transaction_pool.pool) == 1
    assert warehouse_manager.transaction_pool.pool[0].ID == 1
    assert warehouse_manager.transaction_pool.pool[0].item == "item"
    assert warehouse_manager.transaction_pool.pool[0].number == 10
    assert warehouse_manager.transaction_pool.pool[0].price == 5
    assert warehouse_manager.transaction_pool.pool[0].warehouse == 1

def test_distribute_transactions():
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Create a warehouse
    warehouse_manager.create_warehouse(1)

    # Create a transaction
    warehouse_manager.create_transaction(1, "item", 10, 5, 1)

    # Distribute the transaction
    warehouse_manager.distribute_transactions()

    # Test if the transaction was removed from the pool
    assert len(warehouse_manager.transaction_pool.pool) == 0

def test_get_processed_transactions():
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Create a transaction
    warehouse_manager.processed_transactions.append(1)

    # Test if the processed transactions list is returned
    assert warehouse_manager.get_processed_transactions() == [1]

def test_print_warehouses(capsys):
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Create a warehouse
    warehouse_manager.create_warehouse(1)

    # Print the warehouses
    warehouse_manager.print_warehouses()

    # Capture the output
    captured = capsys.readouterr()

    # Test if the output is correct
    expected_output = "Warehouse 1 Inventory:\n - No inventory data found!\n\n"
    assert captured.out == expected_output

def test_shutdown():
    # Create a warehouse manager
    warehouse_manager = ShardedWarehouseManager()

    # Create a warehouse
    warehouse_manager.create_warehouse(1)

    # Shutdown the warehouse manager
    warehouse_manager.shutdown()

    # Test if the warehouses and inventories are cleared
    assert warehouse_manager.warehouses == {}
    assert dict(warehouse_manager.shared_inventories) == {}  # Convert DictProxy to a regular dict before checking
