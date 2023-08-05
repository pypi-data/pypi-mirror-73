import pytest

from pyfiguration.pyfiguration import PyFiguration


def test_createConfig():

    # Create a new configuration
    newConfiguration = PyFiguration()

    # Load some configuration files (this shouldn't result in an Exception)
    newConfiguration.set_configuration(
        sources=[
            "./examples/basic/config/defaults",
            "./examples/basic/config/defaults/server.json",
            "./examples/basic/config/deployments/a.yaml",
        ]
    )


def test_readInvalidConfigFile():

    # Create a new configuration
    newConfiguration = PyFiguration()

    # Oops, try to load a file that is not a configuration file
    with pytest.raises(Exception) as excinfo:
        newConfiguration.set_configuration(sources=["./examples/basic/script.py"])
    assert "Unable to read configuration from" in str(excinfo)


def test_magicMethods():

    # Create a new configuration
    newConfiguration = PyFiguration()

    # Create a decorated test method
    @newConfiguration.add_int_field(field="db.port")
    def test():
        port = newConfiguration["db"]["port"]
        return port

    # Set the configuration from a file
    newConfiguration.set_configuration(sources=["./examples/basic/config/defaults"])

    # Test retrieval (__get__)
    assert isinstance(newConfiguration["db"]["port"], int)

    # Test string representation (__str__)
    asString = str(newConfiguration)
    assert asString.startswith("{") and asString.endswith("}")

    # Test object representation (__repr__)
    asRepr = repr(newConfiguration)
    assert asRepr.startswith("{") and asRepr.endswith("}")

    # Test conversion to a dict (__iter__)
    asDict = dict(newConfiguration)
    assert isinstance(asDict, dict) and asDict is not None

    # Test conversion to a list (__iter__)
    asList = list(iter(newConfiguration))
    assert len(asList) > 0
    for key, value in asList:
        assert isinstance(key, str)

    # Test the decorated test method (__get__)
    assert test() == newConfiguration["db"]["port"]


def test_addingDataTypes():

    # Create a new configuration
    newConfiguration = PyFiguration()

    # Trigger all "add_..._field" methods
    @newConfiguration.add_boolean_field(field="test1")
    @newConfiguration.add_float_field(field="test2")
    @newConfiguration.add_int_field(field="test3")
    @newConfiguration.add_list_field(field="test4")
    @newConfiguration.add_string_field(field="test5")
    def test():
        pass

    # Run the wrapped function (should not result in an Exception)
    test()
