from abc import abstractmethod
from swivel.abstracts import Deployed

class Swivel(Deployed):
    @abstractmethod
    def NAME(self):
        """The stored name constant for this contract"""

        pass

    @abstractmethod
    def VERSION(self):
        """The stored version constant for this contract"""

        pass

    @abstractmethod
    def HOLD(self):
        """The stored hold constant for this contract

        Description:
            TODO
        """

        pass

    @abstractmethod
    def domain(self):
        """The stored EIP712 domain hash for this contract"""

        pass

    @abstractmethod
    def market_place(self):
        """The stored address of a market place contract associated with this contract"""

        pass

    @abstractmethod
    def admin(self):
        """The stored admin address for this contract"""

        pass

    @abstractmethod
    def fenominator(self, i):
        """The stored fee constants for this contract

        Parameters:
            i (int) Index of the fenominator array to return
        """

        pass

    @abstractmethod
    def initiate(self, orders, a, s, opts=None):
        """Allows a user to initiate a position

        Parameters:
            orders (list) Offline swivel orders
            a (list) Order volume (principal) amounts relative to orders list
            s (list) Valid ECDSA signatures for each order
            opts (dict) Optional tx opts
        """

        pass

    @abstractmethod
    def exit(self, orders, a, s, opts=None):
        """Allows a user to exit (sell) a currently held position to the marketplace

        Parameters:
            orders (list) Offline swivel orders
            a (list) Order volume (principal) amounts relative to orders list
            s (list) Valid ECDSA signatures for each order
            opts (dict) Optional tx opts
        """

        pass

    @abstractmethod
    def cancel(self, order, s, opts=None):
        """Allows the cancellation of an order, preventing it from being filled further

        Parameters:
            order (dict) An offline swivel order
            s (string) Valid ECDSA signature for the order
            opts (dict) Optional tx opts
        """

        pass
        
    @abstractmethod
    def split_underlying(self, u, m, a, opts=None):
        """Allows users to deposit underlying and in the process split it into/mint zcTokens and vault notional

        Parameters:
            u (string) Address of the underlying token
            m (int) Maturity timestamp of the market
            a (int) Amount of underlying being deposited
            opts (dict) Optional tx opts
        """

        pass

    @abstractmethod
    def combine_tokens(self, u, m, a, opts=None):
        """Allows users to deposit/burn 1:1 amounts of both zcTokens and vault notional, in the process 'combining' the two and redeeming underlying

        Parameters:
            u (string) Address of the underlying token
            m (int) Maturity timestamp of the market
            a (int) Amount of zctokens being redeemed
            opts (dict) Optional tx opts
        """

        pass

    @abstractmethod
    def redeem_zc_token(self, u, m, a, opts=None):
        """Allows zctoken holders to redeem their tokens for underlying tokens after maturity has been reached

        Parameters:
            u (string) Address of the underlying token
            m (int) Maturity timestamp of the market
            a (int) Amount of zctokens being redeemed
            opts (dict) Optional tx opts
        """

        pass

    @abstractmethod
    def redeem_vault_interest(self, u, m, opts=None):
        """Allows vault owners to redeem any currently accrued interest

        Parameters:
            u (string) Address of the underlying token
            m (int) Maturity timestamp of the market
            opts (dict) Optional tx opts
        """

        pass
