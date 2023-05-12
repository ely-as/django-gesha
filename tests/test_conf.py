import pytest

from gesha.conf import get_setting


def test_get_setting_raises_ValueError_with_invalid_name() -> None:
    with pytest.raises(ValueError):
        get_setting("ABCD")
