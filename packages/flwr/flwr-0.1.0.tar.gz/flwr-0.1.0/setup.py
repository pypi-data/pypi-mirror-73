# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flwr',
 'flwr.app',
 'flwr.app.client',
 'flwr.app.server',
 'flwr.grpc_client',
 'flwr.grpc_server',
 'flwr.proto',
 'flwr.strategy',
 'flwr_example',
 'flwr_example.pytorch',
 'flwr_example.tf_fashion_mnist',
 'flwr_experimental',
 'flwr_experimental.benchmark',
 'flwr_experimental.benchmark.common',
 'flwr_experimental.benchmark.dataset',
 'flwr_experimental.benchmark.model',
 'flwr_experimental.benchmark.plot',
 'flwr_experimental.benchmark.tf_cifar',
 'flwr_experimental.benchmark.tf_fashion_mnist',
 'flwr_experimental.benchmark.tf_hotkey',
 'flwr_experimental.logserver',
 'flwr_experimental.ops',
 'flwr_experimental.ops.compute']

package_data = \
{'': ['*']}

install_requires = \
['google>=2.0.3,<3.0.0',
 'grpcio>=1.27.2,<2.0.0',
 'numpy>=1.18.1,<2.0.0',
 'protobuf==3.12.1']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.6'],
 'benchmark': ['tensorflow-cpu==2.1.0',
               'boto3>=1.12.36,<2.0.0',
               'boto3_type_annotations>=0.3.1,<0.4.0',
               'paramiko>=2.7.1,<3.0.0',
               'docker>=4.2.0,<5.0.0',
               'matplotlib>=3.2.1,<4.0.0'],
 'examples-pytorch': ['torch==1.5.1', 'torchvision==0.6.1'],
 'examples-tensorflow': ['tensorflow-cpu==2.1.0'],
 'http-logger': ['tensorflow-cpu==2.1.0',
                 'boto3>=1.12.36,<2.0.0',
                 'boto3>=1.12.36,<2.0.0',
                 'boto3_type_annotations>=0.3.1,<0.4.0',
                 'boto3_type_annotations>=0.3.1,<0.4.0',
                 'paramiko>=2.7.1,<3.0.0',
                 'docker>=4.2.0,<5.0.0',
                 'matplotlib>=3.2.1,<4.0.0'],
 'ops': ['boto3>=1.12.36,<2.0.0',
         'boto3_type_annotations>=0.3.1,<0.4.0',
         'paramiko>=2.7.1,<3.0.0',
         'docker>=4.2.0,<5.0.0']}

setup_kwargs = {
    'name': 'flwr',
    'version': '0.1.0',
    'description': 'See `README.md`',
    'long_description': '# Flower - A Friendly Federated Learning Research Framework\n\n[![GitHub license](https://img.shields.io/github/license/adap/flower)](https://github.com/adap/flower/blob/master/LICENSE)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/adap/flower/blob/master/CONTRIBUTING.md)\n![Build](https://github.com/adap/flower/workflows/Build/badge.svg)\n\nFlower is a research framework for building federated learning systems. The\ndesign of Flower is based on a few guiding principles:\n\n* **Customizable**: Federated learning systems vary wildly from one use case to\n  another. Flower allows for a wide range of different configurations depending\n  on the needs of each individual use case.\n\n* **Extendable**: Flower originated from a research project at the Univerity of\n  Oxford, so it was build with AI research in mind. Many components can be\n  extended and overridden to build new state-of-the-art systems. \n\n* **Framework-agnostic**: Different machine learning frameworks have different\n  strengths. Flower can be used with any machine learning framework, for\n  example, [PyTorch](https://pytorch.org),\n  [TensorFlow](https://tensorflow.org), or even raw [NumPy](https://numpy.org/)\n  for users who enjoy computing gradients by hand.\n\n* **Understandable**: Flower is written with maintainability in mind. The\n  community is encouraged to both read and contribute to the codebase.\n\n> Note: Even though Flower is used in production, it is published as\n> pre-release software. Incompatible API changes are possible.\n\n## Installation\n\nFlower can be installed directly from the GitHub repository using `pip`:\n\n```bash\n$ pip install git+https://github.com/adap/flower.git\n```\n\nOfficial [PyPI](https://pypi.org/) releases will follow once the API matures.\n\n## Run Examples\n\nWe built a number of examples showcasing different usage scenarios in\n`src/flower_example`. To run an example, first install the necessary extras\n(available extras: `examples-tensorflow`):\n\n```bash\npip install git+https://github.com/adap/flower.git#egg=flower[examples-tensorflow]\n```\n\nOnce the necessary extras (e.g., TensorFlow) are installed, you might want to\nrun the Fashion-MNIST example by starting a single server and multiple clients\nin two terminals using the following commands.\n\nStart server in the first terminal:\n\n```bash\n$ ./src/flower_example/tf_fashion_mnist/run-server.sh\n```\n\nStart the clients in a second terminal:\n\n```bash\n$ ./src/flower_example/tf_fashion_mnist/run-clients.sh\n```\n\n### Docker\n\nIf you have Docker on your machine you might want to skip most of the setup and\ntry out the example using the following commands:\n\n```bash\n# Create docker network `flower` so that containers can reach each other by name\n$ docker network create flower\n# Build the Flower docker containers\n$ ./dev/docker_build.sh\n\n# Run the docker containers (will tail a logfile created by a central logserver)\n$ ./src/flower_example/tf_fashion_mnist/run-docker.sh\n```\n\nThis will start a slightly reduced setup with only four clients.\n\n## Documentation\n\n* [Documentation](https://flower.adap.com/docs/)\n\n## Contributing to Flower\n\nWe welcome contributions. Please see [CONTRIBUTING.md](CONTRIBUTING.md) to get\nstarted!\n',
    'author': 'Daniel J. Beutel',
    'author_email': 'daniel@adap.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adap/flower',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
