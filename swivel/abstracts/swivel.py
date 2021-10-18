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
            i (int) index of the fenominator array to return

        Description:
            TODO
        """

        pass
