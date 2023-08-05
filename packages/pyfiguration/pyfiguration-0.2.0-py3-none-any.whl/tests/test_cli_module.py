import io

from contextlib import redirect_stdout
from pyfiguration.cli import cli


def test_cli_module():
    f = io.StringIO()
    with redirect_stdout(f):
        cli(
            args=[
                "inspect",
                "script",
                "-s",
                "./examples/basic/basic.py",
            ]
        )
    result = f.getvalue()
    assert result.startswith(
        "The following options can be used in a configuration file for the module"
    )
