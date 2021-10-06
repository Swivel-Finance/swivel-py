import pytest

from web3 import (
    Web3,
    EthereumTesterProvider
)

from swivel.vendors import W3

@pytest.fixture
def provider():
    return EthereumTesterProvider()

@pytest.fixture
def vendor(provider):
    return W3(provider)

@pytest.fixture
def tester(provider):
    return provider.ethereum_tester
