import time
from multiprocessing import Process, Queue, Manager, Lock
from backend.warehouse import Warehouse
from backend.transaction import Transaction


def test_warehouse_initialization():
    # Create a warehouse
    lock = Lock()
    shared_inventories = Manager().dict()
    processed_transactions = Manager().list()
    warehouse = Warehouse(1, shared_inventories, lock, processed_transactions)

    # Test if attributes are set correctly
    assert warehouse.ID == 1
    assert dict(warehouse.shared_inventory) == {}  # Convert DictProxy to dict
    assert warehouse.lock == lock
    assert warehouse.processed_transactions == processed_transactions

def test_add_warehouse_transaction():
    # Create a warehouse
    lock = Lock()
    shared_inventories = Manager().dict()
    processed_transactions = Manager().list()
    warehouse = Warehouse(1, shared_inventories, lock, processed_transactions)

    # Create a transaction
    transaction = Transaction(1, 'apple', 5, 1.5, 1)
    warehouse.add_transaction(transaction)

    # Test if the transaction was added to the inventory
    assert warehouse.shared_inventory['apple'] == [5, 1.5]

def test_process_transactions():
    # Create a warehouse with shared memory structures
    lock = Lock()
    shared_inventories = Manager().dict()
    processed_transactions = Manager().list()
    warehouse = Warehouse(1, shared_inventories, lock, processed_transactions)

    # Create a transaction and a queue
    queue = Queue()
    transaction = Transaction(1, 'apple', 5, 1.5, 1)

    # Start the process_transactions method in a separate process
    process = Process(target=warehouse.process_transactions, args=(queue,))
    process.start()

    # Add transaction to queue
    queue.put(transaction)

    # Allow some time for processing
    time.sleep(0.1)

    # Send termination signal
    queue.put(None)

    # Wait for process to finish
    process.join()

    # Test if the transaction was processed
    assert len(warehouse.processed_transactions) == 1
    assert warehouse.processed_transactions[0].ID == transaction.ID

    # Test if inventory was updated correctly
    assert dict(warehouse.shared_inventory) == {'apple': [5, 1.5]}


def test_warehouse_str():
    # Create a warehouse
    lock = Lock()
    shared_inventories = Manager().dict()
    processed_transactions = Manager().list()
    warehouse = Warehouse(1, shared_inventories, lock, processed_transactions)

    # Add a transaction
    transaction = Transaction(1, 'apple', 5, 1.5, 1)
    warehouse.add_transaction(transaction)

    # Test if the string representation matches the expected format
    expected_str = 'Warehouse 1 Inventory:\napple: 5 units @ $1.5 each'
    assert str(warehouse) == expected_str
