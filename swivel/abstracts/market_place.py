from abc import abstractmethod
from swivel.abstracts import Deployed

class MarketPlace(Deployed):
    @abstractmethod
    def admin(self):
        """The stored admin address for this contract"""

        pass

    @abstractmethod
    def swivel(self):
        """The address of the associated Swivel contract deployment"""

        pass

    @abstractmethod
    def set_swivel_address(self, a, o=None):
        """Sets the address of the Swivel smart contract this market place is associated with

        Description:
            Note that this method is only callable by the admin

        Parameters:
            a (address) The address of a deployed Swivel smart contract
            o (dict) Optional transaction options
        """

        pass

    @abstractmethod
    def create_market(self, u, m, c, n, s, d, o=None):
        """Creates a new market

        Description:
            New instances of both ZcToken and VaultTracker are deployed, their addresses then being associated
            with the newly created market.

            Note that this method is only callable by the admin

        Parameters:
            u (string) Address of the underlying token
            m (int) Epoch in seconds, the maturity of the market
            c (string) Address of the Compound token associated with the market
            n (string) Name for the new ZcToken
            s (string) Name for the new ZcToken
            d (int) Number of digits expected for the new ZcToken
            o (dict) Optional transaction options
        """

        pass

    @abstractmethod
    def markets(self, u, m):
        """Gets the market associated with the given underlying and maturity arguments

        Description:
            The returned Market object is { cTokenAddr, ZcTokenAddr, vaultAddr }

        Parameters:
            u (string) Underlying token address
            m (int) Muturity epoch

        Returns:
            Market object if present
        """

        pass

    @abstractmethod
    def c_token_address(self, u, m):
        """Gets the compound token address associated with a given market

        Parameters:
            u (string) Underlying token address
            m (int) Maturity epoch

        Returns:
            Compound token address
        """

        pass
