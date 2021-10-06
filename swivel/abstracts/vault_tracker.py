from abc import ABC, abstractmethod

class VaultTracker(ABC):
    """Persists and curates Vault objects associated with users

    Note that a Vault is a Dict object in this form:

        { notional, redeemable, exchangerate }
    """

    @abstractmethod
    def admin(self):
        """The stored admin address for this contract

        Note that this should always be the MarketPlace address

        Returns:
            The address of the admin (MarketPlace contract)
        """

        pass

    @abstractmethod
    def c_token_addr(self):
        """Adress of the compound token referenced by this vault tracker"""

        pass

    @abstractmethod
    def swivel(self):
        """Address of the associated Swivel contract deployment"""

        pass
    
    @abstractmethod
    def matured(self):
        """A boolean flag indicating maturity

        Set to True if the maturity date has been surpassed
        """

        pass

    @abstractmethod
    def maturity(self):
        """An Epoch (in seconds) representing the time of maturity"""

        pass

    @abstractmethod
    def maturity_rate(self):
        """The maturity rate (TODO: better description)"""

        pass

    @abstractmethod
    def vaults(self):
        """Get a Vault for a given address

        Parameters:
            o (address) Owner of the Vault

        Returns:
            A Vault dict
        """

        pass
    
    @abstractmethod
    def balances_of(self):
        """Get Vault balances for a given user

        Parameters:
            o (address) Owner of the Vault

        Returns:
            A tuple containing Vault notional and redeemable amounts
        """
        pass

    @abstractmethod
    def mature_vault(self, o=None):
        """Attempts to set the mature flag of a vault

        If the maturity has been reached, set the matured flag to True and set the maturity_rate to the
        current exchange rate for the c_token
        """

        pass
