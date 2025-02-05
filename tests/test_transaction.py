from backend.transaction import Transaction  # Adjust the import if necessary

# Test initialization of Transaction
def test_transaction_initialization():
    # Create a transaction
    transaction = Transaction(1, 'apple', 5, 1.5, 1)

    # Test if attributes are set correctly
    assert transaction.ID == 1
    assert transaction.item == 'apple'
    assert transaction.number == 5
    assert transaction.price == 1.5
    assert transaction.warehouse == 1

# Test string representation of Transaction
def test_transaction_str():
    transaction = Transaction(1, 'apple', 5, 1.5, 1)
    
    # Test if the string representation matches the expected format
    expected_str = '1 apple 5 1.5 1'
    assert str(transaction) == expected_str
