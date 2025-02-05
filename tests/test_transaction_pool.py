from backend.transaction_pool import TransactionPool
from backend.transaction import Transaction

# Test initialization of TransactionPool
def test_transaction_pool_initialization():
    # Create a transaction pool
    transaction_pool = TransactionPool()

    # Test if the pool is empty
    assert len(transaction_pool.pool) == 0

# Test adding a transaction to the pool
def test_transaction_pool_add_transaction():
    # Create a transaction pool
    transaction_pool = TransactionPool()

    transaction = Transaction(1, 'apple', 5, 1.5, 1)
    # Add a transaction
    transaction_pool.add_transaction(transaction)

    # Test if the transaction was added
    assert len(transaction_pool.pool) == 1