import pytest
from consumer.helper.validators import get_env_variable


def test_get_env_variable():
    value_env = "PORT"
    check_port_env = get_env_variable(value_env)
    if not check_port_env:
        pytest.fail(f"Error from test get_env_variable")

    print("Test handler collection catalog passed!")
