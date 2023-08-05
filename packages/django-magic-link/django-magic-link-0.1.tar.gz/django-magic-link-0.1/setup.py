# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic_link', 'magic_link.migrations']

package_data = \
{'': ['*'], 'magic_link': ['templates/*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-magic-link',
    'version': '0.1',
    'description': "Django app for managing tokenised 'magic link' logins.",
    'long_description': '# Django Magic Link\n\nOpinionated Django app for managing "magic link" logins.\n\n**WARNING**\n\nIf you send a login link to the wrong person, they will gain full access to the user\'s account. Use\nwith extreme caution, and do not use this package without reading the source code and ensuring that\nyou are comfortable with it. If you have an internal security team, ask them to look at it before\nusing it. If your clients have security sign-off on your application, ask them to look at it before\nusing it.\n\n**/WARNING**\n\nThis app is not intended for general purpose URL tokenisation; it is designed to support a single\nuse case - so-called "magic link" logins.\n\nThere are lots of alternative apps that can support this use case, including the project from which\nthis has been extracted -\n[`django-request-token`](https://github.com/yunojuno/django-request-token). The reason for yet\nanother one is to handle the real-world challenge of URL caching / pre-fetch, where intermediaries\nuse URLs with unintended consequences.\n\nThis packages supports a very specific model:\n\n1. User is sent a link to log them in automatically.\n2. User clicks on the link, and which does a GET request to the URL.\n3. User is presented with a confirmation page, but is _not_ logged in.\n4. User clicks on a button and performs a POST to the same page.\n5. The POST request authenticates the user, and deactivates the token.\n\nThe advantage of this is the email clients do not support POST links, and any prefetch that attempts\na POST will fail the CSRF checks.\n\nThe purpose is to ensure that someone actively, purposefully, clicked on a link to authenticate\nthemselves. This enables instant deactivation of the token, so that it can no longer be used.\n\nIn practice, without this check, valid magic links may be requested a number of times via GET\nrequest before the intended recipient even sees the link. If you use a "max uses" restriction to\nlock down the link you may find this limit is hit, and the end user then finds that the link is\ninactive. The alternative to this is to remove the use limit and rely instead on an expiry window.\nThis risks leaving the token active even after the user has logged in. This package is targeted at\nthis situation.\n\n## Use\n\n### Prerequisite: Override the default templates.\n\nThis package has two HTML templates that must be overridden in your local application.\n\n**logmein.html**\n\nThis is the landing page that a user sees when they click on the magic link. You can add any content\nyou like to this page - the only requirement is that must contains a simple form with a csrf token\nand a submit button. This form must POST back to the link URL. The template render context includes\nthe `link` which has a `get_absolute_url` method to simplify this:\n\n```html\n<form method="POST" action="{{ link.get_absolute_url }}>\n    {% csrf_token %}\n    <button type="submit">Log me in</button>\n</form>\n```\n\n**error.html**\n\nIf the link has expired, been used, or is being accessed by someone who is already logged in, then\nthe `error.html` template will be rendered. The template context includes `link` and `error`.\n\n```html\n<p>Error handling magic link {{ link }}: {{ error }}.</p>\n```\n\n### 1. Create a new login link\n\nThe first step in managing magic links is to create one. Links are bound to a user, and can have a\ncustom expiry and post-login redirect URL.\n\n```python\n# create a link with the default expiry and redirect\nlink = MagicLink.objects.create(user=user)\n\n# create a link with a specific redirect\nlink = MagicLink.objects.create(user=user, redirect_to="/foo")\n\n# create a link with a specific expiry (in seconds)\nlink = MagicLink.objects.create(user=user, expiry=60)\n```\n\n### 3. Send the link to the user\n\nThis package does not handle the sending on your behalf - it is your responsibility to ensure that\nyou send the link to the correct user. If you send the link to the wrong user, they will have full\naccess to the link user\'s account. **YOU HAVE BEEN WARNED**.\n\n## Settings\n\nSettings are read from the environment first, then Django settings.\n\n-   `MAGIC_LINK_DEFAULT_EXPIRY`: the default link expiry, in seconds (defaults to 600 - 5 minutes).\n\n-   `MAGIC_LINK_DEFAULT_REDIRECT`: the default redirect URL (defaults to "/").\n',
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
