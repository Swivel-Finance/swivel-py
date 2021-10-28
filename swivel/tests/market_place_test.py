import pytest
from unittest.mock import Mock

@pytest.fixture(scope='module')
def swivel_address():
    return '0x8e7bFA3106c0544b6468833c0EB41c350b50A5CA'

@pytest.fixture(scope='module')
def underlying(market_place):
    return market_place.vendor.instance.toChecksumAddress('0x5592ec0cfb4dbc12d3ab100b257153436a1f0fea')

@pytest.fixture(scope='module')
def maturity():
    return 1633988168

@pytest.fixture(scope='module')
def c_token(market_place):
    return market_place.vendor.instance.toChecksumAddress('0x6d7f0754ffeb405d23c51ce938289d4835be3b14')

def test_m_place_admin(market_place):
    addr = market_place.admin()
    assert addr == market_place.vendor.account

def test_swivel(market_place, swivel_address):
    #set it first...
    tx_hash = market_place.set_swivel_address(swivel_address)
    tx_rcpt = market_place.vendor.instance.eth.wait_for_transaction_receipt(tx_hash)
    assert tx_rcpt != None

    addr = market_place.swivel()
    assert addr == swivel_address

# NOTE this test is not transact mocked as it has no other dependencies, tho we _could_ mock it out... we'll leave it for now.
def test_create_get_market(market_place, underlying, maturity, c_token):
    name = 'token'
    sym = 'tkn'
    dig = 18
    tx_hash = market_place.create_market(underlying, maturity, c_token, name, sym, dig)
    tx_rcpt = market_place.vendor.instance.eth.wait_for_transaction_receipt(tx_hash)
    # should be able to retrieve the market now
    mkt = market_place.markets(underlying, maturity)
    # will return as a list len(3)
    assert mkt[0] == c_token

def test_c_token_addr(market_place, underlying, maturity, c_token):
    ctkn = market_place.c_token_address(underlying, maturity)
    assert ctkn == c_token

def test_mature_market(transactor, market_place, underlying, maturity):
    transactor.transact = Mock(return_value=None)
    # mock the actual call to the inner contract
    market_place.contract.functions.matureMarket = Mock(return_value=transactor)
    market_place.mature_market(underlying, maturity, { 'gas': 100000 })

    market_place.contract.functions.matureMarket.assert_called()
    # call_args[0] is a tuple of any positional args passed, should be underlying
    assert market_place.contract.functions.matureMarket.call_args[0][0] == underlying
    assert market_place.contract.functions.matureMarket.call_args[0][1] == maturity

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == market_place.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 100000

def test_mature(caller, market_place, underlying, maturity):
    caller.call = Mock(return_value=True)
    market_place.contract.functions.mature = Mock(return_value=caller)
    matured = market_place.mature(underlying, maturity)

    market_place.contract.functions.mature.assert_called()
    assert market_place.contract.functions.mature.call_args[0][0] == underlying
    assert market_place.contract.functions.mature.call_args[0][1] == maturity
    assert matured == True

def test_maturity_rate(caller, market_place, underlying, maturity):
    caller.call = Mock(return_value=7)
    market_place.contract.functions.maturityRate = Mock(return_value=caller)
    rate = market_place.maturity_rate(underlying, maturity)

    market_place.contract.functions.maturityRate.assert_called()
    assert market_place.contract.functions.maturityRate.call_args[0][0] == underlying
    assert market_place.contract.functions.maturityRate.call_args[0][1] == maturity
    assert rate == 7

def test_transfer_vault_notional(transactor, market_place, underlying, maturity):
    transactor.transact = Mock(return_value=None)
    # mock the actual call to the inner contract
    market_place.contract.functions.transferVaultNotional = Mock(return_value=transactor)
    market_place.transfer_vault_notional(underlying, maturity, '0x50MeDud3', 1000, { 'gas': 200000 })

    market_place.contract.functions.transferVaultNotional.assert_called()
    assert market_place.contract.functions.transferVaultNotional.call_args[0][0] == underlying
    assert market_place.contract.functions.transferVaultNotional.call_args[0][1] == maturity
    assert market_place.contract.functions.transferVaultNotional.call_args[0][2] == '0x50MeDud3'
    assert market_place.contract.functions.transferVaultNotional.call_args[0][3] == 1000

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == market_place.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 200000
