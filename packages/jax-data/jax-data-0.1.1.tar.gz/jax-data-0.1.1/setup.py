# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jax_data']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.1.72,<0.2.0', 'jaxlib>=0.1.51,<0.2.0', 'numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'jax-data',
    'version': '0.1.1',
    'description': 'Native data handling for JAX',
    'long_description': '# Jax Datasets\n---\n## data\n---\nTo load data, first subclass the `jax_data.Dataset` class, implementing the __len__ and __getitem__ methods.\nThe `jax_data.Dataloader` class is a simplified adaptation of torch.utils.data.DataLoader.\n',
    'author': 'Ashrit Yarava',
    'author_email': 'ashrity01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ashrit-Yarava/jax-data.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
