import pytest
from app.validator import InvalidAgeError,validate_age

@pytest.mark.parametrize("age", [0, 1, 26, 100])
def test_non_negative_age_is_accepted(age):
    assert validate_age(age)==age

def test_negative_age_is_rejected():
    with pytest.raises(InvalidAgeError):
        validate_age(-5)

