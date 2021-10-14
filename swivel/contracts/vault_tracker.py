from swivel.constants.abi import VAULT_TRACKER
from swivel.abstracts import VaultTracker as base

class VaultTracker(base):
    def __init__(self, v):
        """
        Parameters:
            v (W3) Instance of a vendor W3 class (no other vendors are supported as of now)
        """
        self.vendor = v
        self.abi = VAULT_TRACKER

    def admin(self):
        return self.contract.functions.admin().call()

    def c_token_addr(self):
        return self.contract.functions.cTokenAddr().call()

    def swivel(self):
        return self.contract.functions.swivel().call()

    def matured(self):
        return self.contract.functions.matured().call()

    def maturity(self):
        return self.contract.functions.maturity().call()

    def maturity_rate(self):
        return self.contract.functions.maturityRate().call()

    # TODO
    def vaults(self):
        pass 
    
    # TODO
    def balances_of(self):
        pass
