import io

from pyfiguration.cli import cli
from contextlib import redirect_stdout


def test_cli_module():
    f = io.StringIO()
    with redirect_stdout(f):
        cli(
            args=[
                "inspect",
                "config",
                "-c",
                "./examples/basic/config/defaults",
                "./examples/basic/config/deployments/a.yaml",
                "-s",
                "./examples/basic/basic.py",
            ]
        )
    result = f.getvalue()
    assert result == ""
