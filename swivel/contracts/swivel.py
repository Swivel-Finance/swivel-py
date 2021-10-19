from swivel.constants.abi import SWIVEL
from swivel.abstracts import Swivel as base

class Swivel(base):
    def __init__(self, v):
        """
        Parameters:
            v (W3) Instance of a vendor W3 class (no other vendors are supported as of now)
        """
        self.vendor = v
        self.abi = SWIVEL

    def NAME(self):
        return self.contract.functions.NAME().call()

    def VERSION(self):
        return self.contract.functions.VERSION().call()

    def HOLD(self):
        return self.contract.functions.HOLD().call()

    def domain(self):
        return self.contract.functions.domain().call()

    def market_place(self):
        return self.contract.functions.marketPlace().call()

    def admin(self):
        return self.contract.functions.admin().call()

    def fenominator(self, i):
        return self.contract.functions.fenominator(i).call()
