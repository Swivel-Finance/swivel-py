import os
from web3 import Web3
from .signer import Signer

class W3:
    def __init__(self, p, a=None):
        """
        Parameters:
            p (Web3.Provider) Provider being used to connect
            a (address) An optional default account to use. Will default to .eth.accounts[0] if omitted
        """

        self.instance = Web3(p)

        # normalize .account from the various scenarios
        if a != None:
            self.account = a
        else:
            if bool(self.instance.eth.default_account):
                self.account = self.instance.eth.default_account
            else:
                self.account = self.instance.eth.accounts[0]

        self.signer = Signer()

    def contract(self, address, abi):
        """Get an instance of the vedor low-level contract object

        Parameters:
            address (address) The address of the deployed smart contract
            abi (string) ABI of the deployed smart contract

        Returns:
            the vendor specific contract object
        """
        
        return self.instance.eth.contract(address=address, abi=abi)

    def sign_order(self, o, i, a):
        """Sign an order, producing an EIP712 compliant signature

        Parameters:
            o (dict) Swivel Order object
            i (int) ChainId
            a (string) Address of the deployed verifying contract

        Returns:
            The signature hex
        """

        key = os.getenv('PRIVATE_KEY')
        return self.signer.sign_order(o, i, a, self.instance.toBytes(hexstr=key))
