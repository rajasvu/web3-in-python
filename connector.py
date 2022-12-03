from web3 import Web3

node_url = "HTTP://127.0.0.1:7545"

node_instance = Web3(Web3.HTTPProvider(node_url))

print(node_instance.isConnected())