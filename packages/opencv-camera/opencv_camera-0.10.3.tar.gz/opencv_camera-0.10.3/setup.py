# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opencv_camera', 'opencv_camera.bin']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'numpy', 'opencv_python', 'pyyaml', 'simplejson', 'slurm']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['create_monitor = opencv_camera.bin.camera_calibrate:main',
                     'create_reset = opencv_camera.bin.mjpeg_server:main',
                     'create_shutdown = opencv_camera.bin.video_capture:main']}

setup_kwargs = {
    'name': 'opencv-camera',
    'version': '0.10.3',
    'description': 'An OpenCV camera library',
    'long_description': '# OpenCV Camera\n\n![CheckPackage](https://github.com/MomsFriendlyRobotCompany/opencv_camera/workflows/CheckPackage/badge.svg)\n\nSimple threaded camera and calibration code.\n\n## Install\n\nThe preferred way to install is using `pip`:\n\n    pip install opencv_camera\n\n\n# Change Log\n\n| Data       | Version| Notes                                     |\n|------------|--------|-------------------------------------------|\n| 2018-07-19 | 0.10.0 |  renamed and focused on camera |\n| 2018-07-19 |  0.9.4 |  simple clean-up and updating some things |\n| 2017-10-29 |  0.9.3 |  bug fixes |\n| 2017-04-09 |  0.9.0 |  initial python 3 support |\n| 2017-03-31 |  0.7.0 |  refactored and got rid of things I don\'t need |\n| 2017-01-29 |  0.6.0 |  added video capture (video and images) program |\n| 2016-12-30 |  0.5.3 |  typo fix |\n| 2016-12-30 |  0.5.1 |  refactored |\n| 2016-12-11 |  0.5.0 |  published to PyPi |\n| 2014-3-11  |  0.2.0 |  started |\n\n# MIT License\n\n**Copyright (c) 2014 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/opencv_camera/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
