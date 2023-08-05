import pytest

from pyfiguration.pyfiguration import PyFiguration
from pyfiguration.configuration import Configuration


@pytest.fixture()
def resource():

    # Create a new pyfiguration object
    newPyfiguration = PyFiguration()
    newPyfiguration.add_string_field(field="level1.level2.some_key")
    newPyfiguration.add_string_field(field="level1.level2.some_key")
    newPyfiguration.add_int_field(field="level1.level2.higher", minValue=0, maxValue=10)
    newPyfiguration.add_int_field(field="level1.level2.lower", minValue=0, maxValue=10)
    newPyfiguration.add_int_field(field="level1.level2.another_key", required=True)
    newPyfiguration.add_string_field(field="level1.choices", allowedValues=["A", "B"])

    yield newPyfiguration


def test_Configuration(resource):

    # Create a new configuration object
    newConfiguration = Configuration(
        pyfiguration=resource,
        **{"level1": {"level2": {"some_key": "some_value"}, "some_key": None}}
    )

    # Retrieve the key
    assert newConfiguration["level1"]["level2"]["some_key"] == "some_value"


def test_magics(resource):

    # Create a new configuration object
    newConfiguration = Configuration(
        pyfiguration=resource,
        **{
            "level1": {
                "level2": {
                    "some_key": 0,
                    "higher": 100,
                    "lower": -100,
                    "another_key": None,
                }
            }
        }
    )

    # Count the top level entries (should be one)
    assert len(newConfiguration) == 1

    # Turn into a string
    assert str(newConfiguration).startswith("{") and str(newConfiguration).endswith("}")

    # Remove an element
    del newConfiguration["level1"]


def test_invalidConfiguration(resource):

    # Create a new configuration object
    newConfiguration = Configuration(
        pyfiguration=resource,
        **{
            "level1": {
                "level2": {
                    "some_key": 0,
                    "higher": 100,
                    "lower": -100,
                    "another_key": None,
                },
                "choices": "C",
            }
        }
    )

    # Value is not a string, so this should throw an exception
    with pytest.raises(Exception) as excinfo:
        newConfiguration["level1"]["level2"]["some_key"]
    assert "not of the correct type" in str(excinfo.value)

    # Value too high
    with pytest.raises(Exception) as excinfo:
        newConfiguration["level1"]["level2"]["higher"]
    assert "is higher than the maximum value" in str(excinfo.value)

    # Value too low
    with pytest.raises(Exception) as excinfo:
        newConfiguration["level1"]["level2"]["lower"]
    assert "is lower than the minimum value" in str(excinfo.value)

    # Missing required value
    with pytest.raises(Exception) as excinfo:
        newConfiguration["level1"]["level2"]["another_key"]
    assert "empty but a value is required" in str(excinfo.value)

    # Not in list of allowed values
    with pytest.raises(Exception) as excinfo:
        newConfiguration["level1"]["choices"]
    assert "not an allowed value for" in str(excinfo.value)
