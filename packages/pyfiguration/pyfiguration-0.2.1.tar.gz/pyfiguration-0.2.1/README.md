![Tests](https://img.shields.io/github/workflow/status/gijswobben/pyfiguration/Python%20test%20package/master?label=Test%20pipeline&logo=github&logoColor=%23959da5&style=for-the-badge)
[![TestCoverage](https://img.shields.io/codecov/c/github/gijswobben/pyfiguration/master?label=Test%20Coverage&logo=Codecov&logoColor=%23959da5&style=for-the-badge)](https://codecov.io/gh/gijswobben/pyfiguration)
[![Release](https://img.shields.io/pypi/v/pyfiguration?color=%233775A9&label=PyPi%20package%20version&logo=PyPi&logoColor=%23959da5&style=for-the-badge)](https://pypi.org/project/pyfiguration/)
[![PythonVersion](https://img.shields.io/pypi/pyversions/pyfiguration?color=%233775A9&label=Python%20versions&logo=Python&logoColor=%23959da5&style=for-the-badge)](https://pypi.org/project/pyfiguration/)
[![ReadTheDocs](https://img.shields.io/badge/READTHEDOCS-Available-555555?style=for-the-badge&color=brightgreen&logo=Read%20the%20docs&logoColor=%23959da5)](https://pyfiguration.readthedocs.io/en/latest/index.html)
# PyFiguration
PyFiguration is a configuration tool for Python. It allows you to define which configuration are used from right inside your code. The PyFiguration command line tool helps you inspect which configurations are available, what the allowed values are, and helps to inspect the validity of a configuration file for a specific script.

## Basic usage
In your code you can define which configurations should be available. This example creates a simple Flask server. The port on which the server should start depends on the configuration.

```python
""" script.py
"""
from pyfiguration import conf
from flask import Flask


@conf.addIntField(
    field="server.port",
    description="The port on which the server will start",
    default=8000,
    minValue=80,
    maxValue=9999,
)
def startServer():
    app = Flask(__name__)
    port = conf["server"]["port"]
    print(f"Starting on port {port}")
    app.run(port=port)


if __name__ == "__main__":
    startServer()

```

You can use the PyFiguration command line tool to inspect this module/script:

```console
$ pyfiguration inspect script -s script.py
The following options can be used in a configuration file for the module 'script.py':
server:
  port:
    allowedDataType: int
    default: 8000
    description: The port on which the server will start
    maxValue: 9999
    minValue: 80
    required: true
```

This tells you that the default value for server.port is 8000, and that it should be an integer between 80 and 9999. Running the script (`python script.py`) will start the server on the default port. Lets create a configuration file to overwrite the default:

```yaml
# config.yaml
server:
  port: 5000
```

Now we can start the script again, pointing to the config file to use it:

```console
$ python script.py --config ./config.yaml
Starting on port 5000
 * Serving Flask app "script" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Success! The script has used the configuration we've defined in `config.yaml` file. It's possible to use multiple configuration files, and both in `YAML` and `JSON` formats. Note that the keys will be overwritten if there are duplicates. This is a useful feature that you can use, for example, to set defaults in `defaults.yaml` and then overwrite with deployment specific settings in `deployment.yaml`. It's also possible to reference a full folder. PyFiguration will read all the files in the folder. For a full example checkout the `./examples` folder of this repository.

If you have a configuration file and a script, you can also use the PyFiguration command line to check the config file for errors. Imaging this configuration file:

```yaml
# config_with_warnings.yaml
server:
  port: 500.0
  not_needed_key: some random value
```

We've obviously made 2 mistakes here: 1: the port is a float, 2: there is a key that is not being used by our script. Lets use the command line tool to investigate.

```console
$ pyfiguration inspect config -s script.py -c config_with_warnings.yaml
--------
 Errors
--------
   ✗ Value '500.0' is not of the correct type. The allowed data type is: int
----------
 Warnings
----------
   ! Key 'server.not_needed_key' doesn't exist in the definition and is not used in the module.
```
