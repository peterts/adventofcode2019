import pytest
from src.password_cracker import is_valid_password


@pytest.mark.parametrize('number, output', [
    (111111, False),
    (223450, False),
    (123789, False),
    (112233, True),
    (123444, False),
    (123444, False),
    (111122, True),
    (222333, False),
    (122345, True)
])
def test_is_valid_password(number, output):
    assert is_valid_password(number) == output
