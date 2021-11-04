from py_eth_sig_utils.signing import signature_to_v_r_s
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

    def initiate(self, orders, a, s, opts=None):
        # normalize the full signatures to a list of vrs components. TODO is the list what is expected?
        components = tuple(map(lambda sig: signature_to_v_r_s(self.vendor.instance.toBytes(hexstr=sig)), s))
        return self.contract.functions.initiate(orders, a, components).transact(self.tx_opts(opts))

    def exit(self, orders, a, s, opts=None):
        # normalize the full signatures to a list of vrs components. TODO is the list what is expected?
        components = tuple(map(lambda sig: signature_to_v_r_s(self.vendor.instance.toBytes(hexstr=sig)), s))
        return self.contract.functions.exit(orders, a, components).transact(self.tx_opts(opts))

    def cancel(self, order, s, opts=None):
        components = signature_to_v_r_s(self.vendor.instance.toBytes(hexstr=s))
        return self.contract.functions.cancel(order, components).transact(self.tx_opts(opts))

    def split_underlying(self, u, m, a, opts=None):
        return self.contract.functions.splitUnderlying(u, m, a).transact(self.tx_opts(opts))

    def combine_tokens(self, u, m, a, opts=None):
        return self.contract.functions.combineTokens(u, m, a).transact(self.tx_opts(opts))
    
    def redeem_zc_token(self, u, m, a, opts=None):
        return self.contract.functions.redeemZcToken(u, m, a).transact(self.tx_opts(opts))

    def redeem_vault_interest(self, u, m, opts=None):
        return self.contract.functions.redeemVaultInterest(u, m).transact(self.tx_opts(opts))
