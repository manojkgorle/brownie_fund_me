from brownie import FundMe
from scripts.helpful_scripts import get_account

def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    price = fund_me.getPrice()
    print(price)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from":account, "value": entrance_fee})

def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from":account})
def main():
    fund()
    print("Withdrawing the funds")
    withdraw()