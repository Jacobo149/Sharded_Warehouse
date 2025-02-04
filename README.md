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

### TODO:
- Fix UI
- Make the UI not an infinite loop, rather display what happened
- Fix Infinite Loop in Simulator
- Add Unit Testing
- Fix Directory Structure
- Rewrite the code adhering to clean code practices
- Make the code more modular
- Add random transaction generation
- Add any amount of warehouses can be created (User input)
- Make it a tool for companies to be able to map the warehouses to an actual map. They will be able to test different routes