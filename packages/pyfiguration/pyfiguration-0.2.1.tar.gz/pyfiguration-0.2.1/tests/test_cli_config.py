import io

from pyfiguration.cli import cli, inspectConfig
from contextlib import redirect_stderr, redirect_stdout


def test_inspectConfig():
    f = io.StringIO()
    with redirect_stdout(f):
        inspectConfig(
            "./examples/simple/script.py",
            sources=["./examples/simple/config_with_warnings.yaml"],
        )
    result = f.getvalue()
    assert "✗" in result
    assert "!" in result


def test_cliInspectConfig():
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
