# Sharded_Warehouse

This application will simulate a warehouse workload and distribute transactions via a sharded algorithm.  
Each shard will correspond to a warehouse handling its specific transactions, which will be identifiable via the transaction data.

### Transaction Data
- Transaction ID
- Item
- Number of Items
- Item Price
- Warehouse


### Sharded Algorithm
The sharded algorithm will use the Warehouse to identify which shard to target, from here the transaction will be completed on the shard with the corresponding warehouse
dataframe and add/delete data correspondingly.

### Workload
The workload will produce a series of transactions to be completed across shards asyncronously. Transactions not yet processed will be held in a transaction pool until they are processed.

### TODO:
- Add workload class
- Make the application Multithreaded
- Make the application sharded
- Add error handling
- Make simple interface to interact with the application