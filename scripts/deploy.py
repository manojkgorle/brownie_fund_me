from brownie import FundMe,network,config, MockV3Aggregator
from scripts.helpful_scripts import get_account,deploy_mocks,LOCAL_BLOCKCHAIN_ENVIRONMENTS
def deploy_fund_me():
    account = get_account()
    print(network.show_active())
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS :
        #we use config[][] for listing the value in the config file
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        #mockaggregator is a list
        #if in development network then we need to mock the contracts so we need to deploy our own solidity code for the contracts
        #so, we create a folder named test in the contracts section
        #there we create a file called MockV3Aggregator.sol in which we write the code to deploy our priceFeed
        #MockV3Aggregator is copy pasted from chainlink mix
    #input parameters are passed before the dict for transactions which interact with the block chain
    verify = config['networks'][network.show_active()].get('verify') #get makes lives easier if we forget adding verify field
    fund_me = FundMe.deploy(price_feed_address,{"from":account},publish_source = verify)
    #publish_source fails when we are in development, so again working on that based on the network we are in
    #after the dictonary we are adding the publish source = true to get the contract verified to us by brownie, when the contract is published or created
    print(f"contract deployed at address {fund_me.address}")
    print(price_feed_address)
    return fund_me

#while verifing the smart contracts on platforms like EtherScan, we need to replace the import files with the actual files
#removing the imports & copy pasting the code is known as flattening
#brownie has a more programtic way to do it

def main():
    deploy_fund_me()

#for testing purposes & for making testing purposes much easy, we need to deploy the contract in our local block chain
#so we are having 2 options in front of us: 1) forking the block chain in which the contract is deployed
# or 2) mocking
#mocking implies creating a fake intrfaces & priceFeed(or similar requirements) on the local blockchain for the testing purposes
#mocking was a common industrial practice used for testing of the contracts
#so we make a change to our FundMe.sol file: instead of declaring the AggregatorV3Interface at its address on a particular chain
#we decalre the priceFeed AggreagatorV3Interface in the constructor portion & supply the address using the input format instead of HARDCODING
#so we can use it cross chain & also uses MockV3Aggregator



#while using mainnet forking --> the brownie is making the gas fee as 0, to facilitate the transaction
#so getting additional funds while mainnet forking is done by using method
#while forking alchemy is much better than infura on the basis of performance