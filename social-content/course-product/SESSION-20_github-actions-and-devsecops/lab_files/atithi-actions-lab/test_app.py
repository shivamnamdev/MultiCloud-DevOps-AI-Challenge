import pytest

from app import nights


def test_three_nights():
    assert nights("2026-12-01", "2026-12-04") == 3


def test_checkout_must_be_after_checkin():
    with pytest.raises(ValueError):
        nights("2026-12-04", "2026-12-01")
