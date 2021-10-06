from abc import ABC, abstractmethod

class MarketPlace(ABC):
    @abstractmethod
    def admin(self):
        """The stored admin address for this contract"""

        pass

    @abstractmethod
    def swivel(self):
        """The address of the associated Swivel contract deployment"""

        pass
