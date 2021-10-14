import os
import pytest
import logging

from web3 import Web3, EthereumTesterProvider
from eth_tester import PyEVMBackend, EthereumTester

from swivel.vendors import W3

@pytest.fixture(scope='module')
def logger():
    return logging.getLogger(__name__)

@pytest.fixture(scope='module')
def eth_tester():
    override = {'gas_limit': 6700000}
    params = PyEVMBackend._generate_genesis_params(overrides=override)
    backend = PyEVMBackend(params)
    return EthereumTester(backend)

@pytest.fixture(scope='module')
def provider(eth_tester):
    return EthereumTesterProvider(eth_tester)

@pytest.fixture(scope='module')
def vendor(provider):
    return W3(provider)


