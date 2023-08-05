import os
import re
import io
import sys
import yaml
import argparse
import operator

from importlib.util import spec_from_file_location, module_from_spec
from importlib.abc import Loader

from typing import Any, List, Dict, Optional
from functools import reduce
from .configuration import Configuration


# Create the main parser
parser = argparse.ArgumentParser(
    description="""
PyFiguration commandline tool

Use this commandline tool to inspect scripts and have a look at the
configuration options that the script provides. Furthermore you can
inspect configuration files directly.
""",
    formatter_class=argparse.RawTextHelpFormatter,
)

# Create subparsers, command will be stored in dest command
subprasers = parser.add_subparsers(dest="command", title="Commands")

# Create a parser for the inspect command
inspectParser = subprasers.add_parser(
    "inspect",
    help="Inspect configurations and scripts",
    description="""Inspect configuration files, scripts or modules to
        see which values are allowed, or to check if a provided
        configuration file is valid for a specific script.""",
)

# Create nested commands for the inspect command
inspectSubparsers = inspectParser.add_subparsers(
    dest="inspect_type",
    title="Commands",
    description="""The type object you would like to inspect""",
)

# Add arguments for the configuration inspector
configParser = inspectSubparsers.add_parser(
    "config",
    help="Inspect a configuration file to see if it is valid for a given script",
    description="""This command will load the SCRIPT and look at the defintion. Then
        it will load the CONFIG file and makes sure the CONFIG file is valid
        for the provided SCRIPT. SCRIPT is the filename of the SCRIPT to inspect with PyFiguraton,
        CONFIG file is the configuration file to inspect, against the SCRIPT."""
)
configParser.add_argument(
    "-c", "--config", nargs="*", help="The configuration file to inspect",
)
configParser.add_argument(
    "-s", "--script", help="The script against which to inspect the config",
)

# Add arguments for the script inspector
scriptParser = inspectSubparsers.add_parser(
    "script",
    help="Inspect a script to see what configuration options are available",
    description="""Provide a file or script to inspect it with PyFiguration. This command
        will load the script from file and inspect the PyFiguration decorators
        to find out what the configuration options are. Then, it will display all
        the option as the output of this command. SCRIPT is the filename of the
        script to inspect with PyFiguraton"""
)
scriptParser.add_argument(
    "-s", "--script", help="The script against which to inspect the config",
)

# # Add arguments for the module inspector
# moduleParser = inspectSubparsers.add_parser(
#     "module",
#     help="Inspect a module to see what configuration options are available",
#     description="""Provide a file or script to inspect it with PyFiguration. This command
#         will load the script from file and inspect the PyFiguration decorators
#         to find out what the configuration options are. Then, it will display all
#         the option as the output of this command. SCRIPT is the filename of the
#         script to inspect with PyFiguraton"""
# )
# moduleParser.add_argument(
#     "-s", "--script", help="The script against which to inspect the config",
# )


def inspectConfig(script: str, *args, **kwargs):
    """ Inspect a configuration file

    This command will load the MODULE and look at the defintion. Then
    it will load the CONFIGFILE and makes sure the CONFIGFILE is valid
    for the provided MODULE.

    MODULE is the filename of the module to inspect with PyFiguraton
    CONFIGFILE is the configuration file to inspect, against the MODULE
    """

    # Extract the module name from the file
    scriptName = os.path.splitext(os.path.split(script)[-1])[0]

    # Load the module from file
    os.environ["CLI"] = "TRUE"
    spec = spec_from_file_location(scriptName, script)
    importedModule = module_from_spec(spec)
    if isinstance(spec.loader, Loader):
        spec.loader.exec_module(importedModule)

    # Get the configuration from the module
    conf = getattr(importedModule, "conf")

    # Set the configfile explicitly on the configuration of the module
    conf.set_configuration()

    # Access all keys to check if they're valid
    def checkConfig(
        configuration: Configuration, definition: dict, parents: List[str] = []
    ):
        """
        """
        errors: List[str] = []
        warnings: List[str] = []
        for key in configuration.keys():

            # Set the value to a default value (None = not set)
            value = None

            # Access the configuration (triggers the checks as well)
            try:
                value = configuration[key]
            except Warning as w:
                warnings.append(str(w))
            except Exception as e:
                errors.append(str(e))

            # Make sure it exists
            try:
                definitionForKey = reduce(operator.getitem, parents, definition)
                assert definitionForKey[key] != {}
            except Warning as w:
                warnings.append(str(w))
            except AssertionError:
                warnings.append(
                    f"Key '{'.'.join([*parents, key])}' doesn't exist in the definition and is not used in the module."
                )
            except Exception as e:
                errors.append(str(e))

            # Recursion
            if isinstance(value, Configuration):
                nestedErrors, nestedWarnings = checkConfig(
                    value, definition, parents=parents + [key]
                )
                errors += nestedErrors
                warnings += nestedWarnings

        # Return the errors and warnings
        return errors, warnings

    def checkDefinition(configuration: dict, definition: dict, parents: List[str] = []):
        """
        """
        errors: List[str] = []
        warnings: List[str] = []

        # Check from the definition
        for key, value in definition.items():

            # Make sure all required fields are in the configuration
            try:
                if (
                    isinstance(value, dict)
                    and "required" in value
                    and value["required"]
                ):
                    configurationForKey = reduce(
                        operator.getitem, parents, configuration
                    )
                    configurationForKey[key]
            except Warning as w:
                warnings.append(str(w))
            except Exception as e:
                errors.append(str(e))

            # Recursion
            if isinstance(value, dict):
                nestedErrors, nestedWarnings = checkDefinition(
                    configuration, value, parents=parents + [key]
                )
                errors += nestedErrors
                warnings += nestedWarnings

        return errors, warnings

    # Trigger the checks
    configErrors, configWarnings = checkConfig(
        configuration=conf.configuration, definition=conf.configuration.getDefinition()
    )
    definitionErrors, definitionWarnings = checkDefinition(
        configuration=conf.configuration, definition=conf.configuration.getDefinition()
    )

    # Make sure to show each error/warning only once
    errors = set([e for e in configErrors + definitionErrors])
    warnings = set([w for w in configWarnings + definitionWarnings])

    # Show the found warnings and errors
    if len(errors) > 0:
        print("--------\n Errors \n--------")
    for error in errors:
        print(f"   ✗ {error}")
    if len(warnings) > 0:
        print("----------\n Warnings \n----------")
    for warning in warnings:
        print(f"   ! {warning}")


def inspectScript(script: str, *args, **kwargs):
    """ Inspect a module

    Provide a file or module to inspect it with PyFiguration. This command
    will load the script from file and inspect the PyFiguration decorators
    to find out what the configuration options are. Then, it will display all
    the option as the output of this command.

    MODULE is the filename of the module to inspect with PyFiguraton
    """

    # Extract the module name from the file
    scriptName = os.path.splitext(os.path.split(script)[-1])[0]

    # Load the module from file
    spec = spec_from_file_location(scriptName, script)
    importedModule = module_from_spec(spec)
    if isinstance(spec.loader, Loader):
        spec.loader.exec_module(importedModule)

    # Get the configuration from the module
    conf = getattr(importedModule, "conf")

    print(
        f"The following options can be used in a configuration file for the module '{script}':"
    )
    printDefinition(conf.configuration.getDefinition())


def printDefinition(definition: Dict[str, Any], indent: int = 0):
    """ Helper method for printing a defintion in a nice way.

    Args:
        definition (dict): The definition to display
        indent (int, optional): The number of spaces to use for indentation
    """

    # Create a buffer to hold the YAML output (the YAML library can only write to file)
    buffer = io.StringIO()

    # Dump the definition as YAML in the buffer and convert back to text
    yaml.dump(definition, buffer)
    definitionYAML = buffer.getvalue()

    # Replace Python classes with their name (e.g. str, int, list, float, ...)
    definitionYAML = re.sub(r"!!python\/name:builtins\.(\w+).+", r"\1", definitionYAML)

    # Show the output
    print(definitionYAML)


def showHelp(exitCode: int = 1):
    """ Show the help text from the argument parser.

    Args:
        exitCode (int, optional): The exit code to return when shutting down. Defaults to 1.
    """

    parser.print_help(sys.stderr)
    sys.exit(1)


def cli(args: Optional[List[str]] = None):
    """ Parse the arguments from the command line and
    take the appropriate action.
    """

    # Parse the input arguments
    args = vars(parser.parse_known_args(args)[0])

    # Execute the selected action
    actions[args.get("command", None)][args.get("inspect_type", None)](**args)


actions = {
    "inspect": {
        "config": inspectConfig,
        "script": inspectScript,
        "module": inspectScript,
    },
    None: showHelp,
}


if __name__ == "__main__":
    cli(sys.argv[1:])
