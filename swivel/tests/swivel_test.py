import pytest
from unittest.mock import Mock

@pytest.fixture(scope='module')
def key(vendor):
    return vendor.instance.toBytes(hexstr='0xfb28b03032bbb105e1199e496b23a6435a077375cbea9c6c4998b971a672873c')

@pytest.fixture(scope='module')
def orders(key):
    # we can use the same order 2x here for the purpose of this test...
    order = {
        'key': key,
        'maker': '0x7111F9Aeb2C1b9344EC274780dc9e3806bdc60Ef',
        'underlying': '0x5592EC0cfb4dbc12D3aB100b257153436a1f0FEa',
        'vault': False,
        'exit': False,
        'principal': 1000,
        'premium': 60,
        'maturity': 1655255622,
        'expiry': 1625173101,
    }

    return [order, order]

@pytest.fixture(scope='module')
def signatures(vendor):
    # again, just using same thing 2x
    sig = '06aa9b426a48ff92d3b940eea498ba8bf9cf4e3e05987bdf4c68c66382385f5e59dd5f013c2b13eb7958234ad441c53675b196d88d143eccf93192b5b9758d571b'
    return [sig, sig]

@pytest.fixture(scope='module')
def amounts():
    return [1000, 500]

def test_name(swivel):
    name = swivel.NAME()
    assert name == 'Swivel Finance'

def test_version(swivel):
    verz = swivel.VERSION()
    assert verz == '2.0.0'

def test_hold(swivel):
    hold = swivel.HOLD()
    assert hold == 259200

def test_domain(swivel):
    dom = swivel.domain()
    assert dom != None

def test_market_place_address(market_place, swivel):
    m_place_addr = swivel.market_place()
    assert m_place_addr == market_place.address

def test_swivel_admin(swivel):
    addr = swivel.admin()
    assert addr == swivel.vendor.account

def test_fenominator(swivel, logger):
    fee1 = swivel.fenominator(0)
    assert fee1 == 200
    fee2 = swivel.fenominator(1)
    assert fee2 == 600
    fee3 = swivel.fenominator(2)
    assert fee3 == 400
    fee4 = swivel.fenominator(3)
    assert fee4 == 200

def test_initiate(transactor, swivel, orders, amounts, signatures):
    # mock the fluid call to .transact
    transactor.transact = Mock(return_value=None)
    # mock the actual call to the inner contract
    swivel.contract.functions.initiate = Mock(return_value=transactor)
    swivel.initiate(orders, amounts, signatures, { 'gas': 1000000 })

    swivel.contract.functions.initiate.assert_called()
    # call_args[0] is a tuple of any positional args passed. should be 2 orders
    assert len(swivel.contract.functions.initiate.call_args[0][0]) == 2
    # 2 amounts
    assert len(swivel.contract.functions.initiate.call_args[0][1]) == 2
    # 2 tuples of vrs
    assert len(swivel.contract.functions.initiate.call_args[0][2]) == 2
    # should be (v,r,s)
    assert len(swivel.contract.functions.initiate.call_args[0][2][0]) == 3

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 1000000

def test_exit(transactor, swivel, orders, amounts, signatures):
    transactor.transact = Mock(return_value=None)
    swivel.contract.functions.exit = Mock(return_value=transactor)
    swivel.exit(orders, amounts, signatures, { 'gas': 250000 })

    swivel.contract.functions.exit.assert_called()
    assert len(swivel.contract.functions.exit.call_args[0][0]) == 2
    assert len(swivel.contract.functions.exit.call_args[0][1]) == 2
    assert len(swivel.contract.functions.exit.call_args[0][2]) == 2
    assert len(swivel.contract.functions.exit.call_args[0][2][0]) == 3

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 250000

def test_cancel(transactor, swivel, orders, signatures):
    transactor.transact = Mock(return_value=None)
    swivel.contract.functions.cancel = Mock(return_value=transactor)
    swivel.cancel(orders[0], signatures[0], { 'gas': 15000 })

    swivel.contract.functions.cancel.assert_called()
    # check the sig components tuple
    assert len(swivel.contract.functions.cancel.call_args[0][1]) == 3

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 15000

def test_split_underlying(transactor, swivel):
    transactor.transact = Mock(return_value=None)
    swivel.contract.functions.splitUnderlying = Mock(return_value=transactor)
    swivel.split_underlying('0xUnd3r', 1234567890, 1000, { 'gas': 17000 })

    swivel.contract.functions.splitUnderlying.assert_called()
    assert swivel.contract.functions.splitUnderlying.call_args[0][0] == '0xUnd3r'
    assert swivel.contract.functions.splitUnderlying.call_args[0][2] == 1000

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 17000   

def test_combine_tokens(transactor, swivel):
    transactor.transact = Mock(return_value=None)
    swivel.contract.functions.combineTokens = Mock(return_value=transactor)
    swivel.combine_tokens('0xUnd3r', 1234567890, 500, { 'gas': 1000 })

    swivel.contract.functions.combineTokens.assert_called()
    assert swivel.contract.functions.combineTokens.call_args[0][2] == 500

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 1000

def test_redeem_zctoken(transactor, swivel):
    transactor.transact = Mock(return_value=None)
    swivel.contract.functions.redeemZcToken = Mock(return_value=transactor)
    swivel.redeem_zc_token('0xUnd3r', 1234567890, 700, { 'gas': 2000 })

    swivel.contract.functions.redeemZcToken.assert_called()
    assert swivel.contract.functions.redeemZcToken.call_args[0][2] == 700

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 2000

def test_redeem_vault_interest(transactor, swivel):
    transactor.transact = Mock(return_value=None)
    swivel.contract.functions.redeemVaultInterest = Mock(return_value=transactor)
    swivel.redeem_vault_interest('0xUnd3r', 1234567899, { 'gas': 2500 })

    swivel.contract.functions.redeemVaultInterest.assert_called()
    assert swivel.contract.functions.redeemVaultInterest.call_args[0][1] == 1234567899

    transactor.transact.assert_called()
    assert transactor.transact.call_args[0][0]['from'] == swivel.vendor.account
    assert transactor.transact.call_args[0][0]['gas'] == 2500
