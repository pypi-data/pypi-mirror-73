# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_link']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-magic-link',
    'version': '0.1.dev1',
    'description': "Django app for managing tokenised 'magic link' logins.",
    'long_description': '# Django Magic Link\n\nOpinionated Django app for managing "magic link" logins.\n\nThis app is not intended for general purpose URL tokenisation; rather it is designed to support a\nsingle use case - so-called "magic link" logins.\n\nThere are lots of alternative apps that can support this use case, including the project from which\nthis has been extracted - `django-request-tokens`. The reason for yet another one is to handle the\nreal-world challenge of URL caching / pre-fetch, where intermediaries use URLs with unintended\nconsequences.\n\nThis packages supports a very specific model:\n\n1. User is sent a URL to log them in.\n2. User clicks on the link, and which does a GET request to the URL.\n3. User is presented with a confirmation page, but is _not_ logged in.\n4. User clicks on a button and performs a POST to the same page.\n5. The POST request authenticates the user, and deactivates the token.\n\nThe advantage of this is the email clients do not support POST links, and any prefetch that attempts\na POST will fail the CSRF checks.\n\nThe purpose is to ensure that someone actively, purposefully, clicked on a link to authenticate\nthemselves. This enables instant deactivation of the token, so that it can no longer be used.\n\nIn practice, without this check, many tokenised authentication links are "used up" before the\nintended recipient has clicked on the link.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-magic-link',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
