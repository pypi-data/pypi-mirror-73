# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowday',
 'snowday.objects',
 'snowday.privileges',
 'snowday.types',
 'snowday.util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snowday',
    'version': '0.1.0',
    'description': 'Tools for making Snowflake administration feel like a snow day.',
    'long_description': '# snowday\n\nMake every day a ❄️ day.\n\n\n### Installation\n\n```\npip install snowday\n```\n\n\n### Usage\n\n',
    'author': 'Jacob Thomas',
    'author_email': 'jake@bostata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bostata/snowday',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
