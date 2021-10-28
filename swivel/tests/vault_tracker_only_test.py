import pytest
from unittest.mock import Mock
from swivel.constants.bin import VAULT_TRACKER
from swivel.contracts import VaultTracker

@pytest.fixture
def vault_tracker(vendor):
    # the HOC has it's abi available
    tracker = VaultTracker(vendor)
    # our W3 vendor .contract method is not for deployment, use the primitive here
    deployed = vendor.instance.eth.contract(abi=tracker.abi, bytecode=VAULT_TRACKER)
    # web3 will complain about a non-checksum address like the ctoken...
    c_token_addr = vendor.instance.toChecksumAddress('0x6d7f0754ffeb405d23c51ce938289d4835be3b14')
    tx_hash = deployed.constructor(123456789, c_token_addr, '0x8e7bFA3106c0544b6468833c0EB41c350b50A5CA').transact({ 'from': vendor.account })
    tx_rcpt = vendor.instance.eth.wait_for_transaction_receipt(tx_hash)
    tracker.at(tx_rcpt['contractAddress'])
    return tracker

@pytest.fixture
def vault():
    return { 'notional': 1000, 'redeemable': 500, 'exchangeRate': 10 }

def test_admin(vault_tracker):
    addr = vault_tracker.admin()
    # the vendor will normalize .account...
    assert addr == vault_tracker.vendor.account

def test_c_token_addr(vault_tracker):
    addr = vault_tracker.c_token_addr()
    assert addr == vault_tracker.vendor.instance.toChecksumAddress('0x6d7f0754ffeb405d23c51ce938289d4835be3b14')

def test_swivel_addr(vault_tracker):
    addr = vault_tracker.swivel()
    assert addr == '0x8e7bFA3106c0544b6468833c0EB41c350b50A5CA'

def test_maturity(vault_tracker):
    mty = vault_tracker.maturity()
    assert mty == 123456789

def test_matured(caller, vault_tracker, vault):
    caller.call = Mock(return_value=True)
    vault_tracker.contract.functions.matured = Mock(return_value=caller)
    matured = vault_tracker.matured()

    vault_tracker.contract.functions.matured.assert_called()
    assert matured == True

def test_maturity_rate(caller, vault_tracker):
    caller.call = Mock(return_value=11)
    vault_tracker.contract.functions.maturityRate = Mock(return_value=caller)
    rate = vault_tracker.maturity_rate()

    vault_tracker.contract.functions.maturityRate.assert_called()
    assert rate == 11

def test_vaults(caller, vault_tracker, vault):
    caller.call = Mock(return_value=vault)
    vault_tracker.contract.functions.vaults = Mock(return_value=caller)
    owned = vault_tracker.vaults('0xG1mM3mYVaU1t')

    vault_tracker.contract.functions.vaults.assert_called()
    assert vault_tracker.contract.functions.vaults.call_args[0][0] == '0xG1mM3mYVaU1t'
    assert owned == vault

def test_balances_of(caller, vault_tracker, vault):
    caller.call = Mock(return_value=(vault['notional'], vault['redeemable']))
    vault_tracker.contract.functions.balancesOf = Mock(return_value=caller)
    owned = vault_tracker.balances_of('0xG1mM3mYBa1anC35')

    vault_tracker.contract.functions.balancesOf.assert_called()
    assert vault_tracker.contract.functions.balancesOf.call_args[0][0] == '0xG1mM3mYBa1anC35'
    assert owned[0] == vault['notional']
    assert owned[1] == vault['redeemable']
