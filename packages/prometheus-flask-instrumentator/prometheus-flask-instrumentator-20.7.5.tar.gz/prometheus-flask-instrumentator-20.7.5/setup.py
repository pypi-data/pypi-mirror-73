# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prometheus_flask_instrumentator']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1,<2', 'prometheus-client>=0.8,<0.9']

setup_kwargs = {
    'name': 'prometheus-flask-instrumentator',
    'version': '20.7.5',
    'description': 'Instruments Flask API transparently',
    'long_description': '# Prometheus Flask Instrumentator\n\n[![PyPI version](https://badge.fury.io/py/prometheus-flask-instrumentator.svg)](https://pypi.python.org/pypi/prometheus-flask-instrumentator/)\n[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![downloads](https://img.shields.io/pypi/dm/prometheus-flask-instrumentator)](https://pypi.org/project/prometheus-flask-instrumentator/)\n\n[![release](https://github.com/trallnag/prometheus-flask-instrumentator/workflows/release/badge.svg)](https://github.com/trallnag/prometheus-flask-instrumentator)\n[![test branches](https://github.com/trallnag/prometheus-flask-instrumentator/workflows/test%20branches/badge.svg)](https://github.com/trallnag/prometheus-flask-instrumentator)\n[![codecov](https://codecov.io/gh/trallnag/prometheus-flask-instrumentator/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/prometheus-flask-instrumentator)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSmall package to instrument your Flask app transparently. Install with:\n\n    pip install prometheus-flask-instrumentator\n\n## Fast Track\n\n```python\nfrom prometheus_flask_instrumentator import FlaskInstrumentator\nFlaskInstrumentator(flask_app).instrument()\n```\n\n**Important: This does not expose the `/metrics` endpoint.** You will have to \ndo that manually. The reason for this is that there are a multitude of \napproaches depending on specific details like running the Flask app in a \npre-fork server like Gunicorn etc. See below for an example on how to do that \nor refer to the repository of the official Prometheus client for Python.\n\nThe API is instrumented with a single metric:\n\n`http_request_duration_seconds{handler, method, status}`\n\nWith the time series included in this metric you can get everything from total \nrequests to the average latency. Here are distinct features of this \nmetric, all of them can be **configured and deactivated** if you wish:\n\n* Status codes are grouped into `2xx`, `3xx` and so on. This reduces \n    cardinality. \n* Requests without a matching template are grouped into the handler `none`.\n* If exceptions occur during request processing and no status code was returned \n    it will default to a `500` server error.\n\n## Prerequesites\n\nYou can also check the `pyproject.toml` for detailed requirements.\n\n* `python = "^3.6"` (tested with 3.6 and 3.8)\n* `fastapi = "^1"` (tested with 1.1.2)\n* `prometheus-client = "^0.8.0"` (tested with 0.8.0)\n\nMetrics endpoint exposition not included. `metrics` must be made available by \nother means for example by adding an endpoint manually (see examples) or \nrelying on `start_http_server()` provided by the prometheus client library.\n\n## Example with all parameters\n\n```python\nfrom prometheus_flask_instrumentator import FlaskInstrumentator\n\nFlaskInstrumentator(\n    app=flask_app,\n    should_group_status_codes=False,\n    should_ignore_untemplated=False,\n    should_group_untemplated=False,\n    excluded_handlers=[\n        "admin",  # Unanchored regex.\n        "^/secret/.*$"],  # Full regex example.  \n    buckets=(1, 2, 3, 4,),\n    label_names=("method", "handler", "status",)\n).instrument()\n```\n\n## Exposing metric endpoint\n\nHere is one way to do it:\n\n```python\nfrom prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest\n\n@app.route("/metrics")\n@FlaskInstrumentator.do_not_track()\ndef metrics():\n    data = generate_latest(REGISTRY)\n    headers = {\n        \'Content-Type\': CONTENT_TYPE_LATEST,\n        \'Content-Length\': str(len(data))}\n    return data, 200, headers\n```\n\n## Development\n\nDeveloping and building this package on a local machine requires \n[Python Poetry](https://python-poetry.org/). I recommend to run Poetry in \ntandem with [Pyenv](https://github.com/pyenv/pyenv). Once the repository is \ncloned, run `poetry install` and `poetry shell`. From here you may start the \nIDE of your choice.\n\nFor formatting, the [black formatter](https://github.com/psf/black) is used.\nRun `black .` in the repository to reformat source files. It will respect\nthe black configuration in the `pyproject.toml`.\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim.schwenke+trallnag@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trallnag/prometheus-flask-instrumentator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
