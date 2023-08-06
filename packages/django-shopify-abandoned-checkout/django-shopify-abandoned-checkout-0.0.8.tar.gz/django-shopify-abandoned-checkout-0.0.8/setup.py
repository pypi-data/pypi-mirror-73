# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shopify_abandoned_checkout',
 'shopify_abandoned_checkout.management',
 'shopify_abandoned_checkout.management.commands',
 'shopify_abandoned_checkout.migrations']

package_data = \
{'': ['*'], 'shopify_abandoned_checkout': ['templates/email/*']}

install_requires = \
['Django>=2.2.0', 'django-shopify-sync>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'django-shopify-abandoned-checkout',
    'version': '0.0.8',
    'description': 'Send Shopify abandoned checkout emails from Django',
    'long_description': None,
    'author': 'David Burke',
    'author_email': 'dburke@thelabnyc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/thelabnyc/django-shopify-abandoned-checkout',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
