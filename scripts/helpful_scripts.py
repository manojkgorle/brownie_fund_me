from brownie import accounts,network,config,MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS =["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
#eth-usd price feed going to have 8 decimals
DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
        account = get_account()
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks..")
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE,{"from":account})
            print(DECIMALS,STARTING_PRICE)
        print("Mocks deployed")
       
        #mockaggregator is a list
        #if in development network then we need to mock the contracts so we need to deploy our own solidity code for the contracts
        #so, we create a folder named test in the contracts section
        #there we create a file called MockV3Aggregator.sol in which we write the code to deploy our priceFeed
        #MockV3Aggregator is copy pasted from chainlink mix