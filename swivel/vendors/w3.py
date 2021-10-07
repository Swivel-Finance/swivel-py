from web3 import Web3

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

    def contract(self, address, abi):
        """Get an instance of the vedor low-level contract object

        Parameters:
            address (address) the address of the deployed smart contract
            abi (string) the abi of the deployed smart contract

        Returns:
            the vendor specific contract object
        """
        
        # TODO we can implement a .Signer abstraction as well...
        return self.instance.eth.contract(address=address, abi=abi)
