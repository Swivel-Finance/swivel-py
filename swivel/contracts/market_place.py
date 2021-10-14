from swivel.constants.abi import MARKET_PLACE
from swivel.abstracts import MarketPlace as base

class MarketPlace(base):
    def __init__(self, v):
        """
        Parameters:
            v (W3) Instance of a vendor W3 class (no other vendors are supported as of now)
        """
        self.vendor = v
        self.abi = MARKET_PLACE

    def admin(self):
        return self.contract.functions.admin().call()

    def swivel(self):
        return self.contract.functions.swivel().call()

    def set_swivel_address(self, a, o=None):
        return self.contract.functions.setSwivelAddress(a).transact(self.tx_opts(o))

    def create_market(self, u, m, c, n, s, d, o=None):
        return self.contract.functions.createMarket(u, m, c, n, s, d).transact(self.tx_opts(o))

    def markets(self, u, m):
        return self.contract.functions.markets(u, m).call()

    def c_token_address(self, u, m):
        return self.contract.functions.cTokenAddress(u, m).call()
