import pytest

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
