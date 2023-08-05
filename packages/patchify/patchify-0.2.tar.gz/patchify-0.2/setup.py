# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patchify', 'patchify.tests']

package_data = \
{'': ['*']}

install_requires = \
['scikit-image>=0.17.2,<0.18.0']

setup_kwargs = {
    'name': 'patchify',
    'version': '0.2',
    'description': 'A library that helps you split image into small, overlappable patches, and merge patches back into the original image.',
    'long_description': '# patchify\n\npatchfy can split images into small overlappable patches by given patch cell size, and merge patches into original image.\n\nThis library provides two functions: `patchify`, `unpatchify`.\n\nUsage:\n\n#### `patchify(image_to_patch, patch_shape, step=1)`\n\nExample: <br>\n2D images:\n```python\n#This will split the image into small images of shape [3,3]\npatches = patchify(image, (3, 3), step=1)\n```\n3D images:\n```python\n#This will split the image into small images of shape [3,3,3]\npatches = patchify(image, (3, 3, 3), step=1)\n```\n\nPatches can merged using:\n#### `unpatchify(patches_to_merge, merged_image_size)`\n\nExample:\n```python\nreconstructed_image = unpatchify(patches, image.shape)\n```\nThis will reconstruct the original image that was patchified in previous code.\n\nA full example:\n\n##### 2D images\n```python\nimport numpy as np\nfrom patchify import patchify, unpatchify\n\nimage = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])\n\npatches = patchify(image, (2,2), step=1) # split image into 2*3 small 2*2 patches.\n\nassert patches.shape == (2, 3, 2, 2)\nreconstructed_image = unpatchify(patches, image.shape)\n\nassert (reconstructed_image == image).all()\n```\n\n##### 3D images\n```python\nimport numpy as np\nfrom patchify import patchify, unpatchify\n\nimage = np.random.rand(512,512,3)\n\npatches = patchify(image, (2,2,3), step=1) # patch shape [2,2,3]\nprint(patches.shape) # (511, 511, 1, 2, 2, 3). Total patches created: 511x511x1\n\nassert patches.shape == (511, 511, 1, 2, 2, 3)\nreconstructed_image = unpatchify(patches, image.shape)\nprint(reconstructed_image.shape) # (512, 512, 3)\n\nassert (reconstructed_image == image).all()\n```\n',
    'author': 'Weiyuan Wu',
    'author_email': 'doomsplayer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dovahcrow/patchify.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
