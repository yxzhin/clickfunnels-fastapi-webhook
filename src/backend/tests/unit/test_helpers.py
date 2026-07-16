from pytest import mark, raises

from src.backend.app.utils.helpers import Helpers


@mark.parametrize(
    ("phone", "region", "expected"),
    [
        ("+16502530000", None, "+16502530000"),
        ("(650) 253-0000", "US", "+16502530000"),
        ("8 (999) 123-45-67", "RU", "+79991234567"),
        ("+381641234567", None, "+381641234567"),
    ],
)
async def test_helpers_normalize_phone_success(
    phone: str,
    region: str | None,
    expected: str,
):
    assert Helpers.normalize_phone(phone, default_region=region) == expected


@mark.parametrize(
    ("phone", "region"),
    [
        ("", None),
        ("abcdef", None),
        ("123", "US"),
        ("+999999", None),
    ],
)
async def test_helpers_normalize_phone_failure(phone: str, region: str):
    with raises(ValueError):
        Helpers.normalize_phone(phone, default_region=region)
