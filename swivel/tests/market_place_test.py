import pytest

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
