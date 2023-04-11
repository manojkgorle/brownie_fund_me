from scripts.helpful_scripts import get_account,LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network,accounts,exceptions
import pytest 
def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from":account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee 
    #assert is for checking proof of correctness
    #here we are checking if the amount sent was actually into the address which sent it or not
    tx2 = fund_me.withdraw({"from":account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 1, f"The accountToAmountFunded returned a value {fund_me.amountToAccountFunded({'from':account})}"

def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add() #creates a new account in cli with a different mnemonic
    #fund_me.withdraw({"from":bad_actor})
    with pytest.raises(exceptions.VirtualMachineError): 
        fund_me.withdraw({"from": bad_actor})

    #mainnet forking