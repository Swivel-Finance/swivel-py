import pytest

def test_account(vendor):
    assert len(vendor.account) == 42
    # the fixture does not pass an account, so it should be accounts[0]
    assert vendor.account == vendor.instance.eth.accounts[0]
