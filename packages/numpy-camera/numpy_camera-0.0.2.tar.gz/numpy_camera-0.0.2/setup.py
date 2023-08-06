# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numpy_camera']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'numpy', 'slurm']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'], 'picamera': ['picamera']}

setup_kwargs = {
    'name': 'numpy-camera',
    'version': '0.0.2',
    'description': '???',
    'long_description': '# Numpy Camera\n\n**Look away! Still in dev**\n\nSimple threaded camera that doesn\'t need OpenCV.\n\n## Install\n\n```\npip install -U numpy_camera\n```\n\n## Usage\n\n```\nc = ThreadedCamera((640,480))\nc.start()        # starts internal loop\nframe = c.read() # numpy array\nc.stop()         # stops internal loop\nc.join()         # gathers back up the thread\n```\n\n# MIT License\n\n**Copyright (c) 2020 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
