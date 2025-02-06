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


### UI
The UI will access the processed transactions in order.  
Rectangles correspond to warehouses.  
Arrows correspond to transactions.  
The stock of the warehouse will be shown below the respective warehouse in a textbox

### Testing
Testing is done via pytest library:

- Navigate to project root directory
- Run below command
`python -m pytest tests`

### TODO:
- Fix UI to work with any amount of warehouses
- Make UI user interactive
- Make it a tool for companies to be able to map the warehouses to an actual map. They will be able to test different routes