# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['merkle_tree_stream']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'flat-tree>=0.0.1-alpha.8,<0.0.2']

setup_kwargs = {
    'name': 'merkle-tree-stream',
    'version': '0.0.1a5',
    'description': 'A stream that generates a merkle tree based on the incoming data',
    'long_description': '# merkle-tree-stream\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/merkle-tree-stream/status.svg)](https://drone.autonomic.zone/hyperpy/merkle-tree-stream)\n\n## A stream that generates a merkle tree based on the incoming data\n\n> A hash tree or merkle tree is a tree in which every leaf node is labelled\n> with the hash of a data block and every non-leaf node is labelled with the\n> cryptographic hash of the labels of its child nodes. Merkle trees in Dat are\n> specialized flat trees that contain the content of the archives.\n\n## Install\n\n```sh\n$ pip install merkle-tree-stream\n```\n\n## Example\n\n```python\nimport hashlib\n\ndef _leaf(node, roots=None):\n    return hashlib.sha256(node.data).digest()\n\ndef _parent(first, second):\n    sha256 = hashlib.sha256()\n    sha256.update(first.data)\n    sha256.update(second.data)\n    return sha256.digest()\n\nmerkle = MerkleTreeGenerator(leaf=leaf, parent=parent)\n\nmerkle.write(b"a")\nmerkle.write(b"b")\n\nassert len(merkle) == 2 + 1\n```\n',
    'author': 'decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/merkle-tree-stream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
