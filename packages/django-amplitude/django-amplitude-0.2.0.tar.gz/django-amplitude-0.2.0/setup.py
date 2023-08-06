# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amplitude']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.1', 'httpx>=0.13.2,<0.14.0', 'user-agents>=2.1,<3.0']

setup_kwargs = {
    'name': 'django-amplitude',
    'version': '0.2.0',
    'description': 'Integration between Django and Amplitude',
    'long_description': '# Django Amplitude\n\nIntegration between Django and [Amplitude.com](https://amplitude.com/) to help send events via the [Amplitude HTTP API (v2)](https://developers.amplitude.com/docs/http-api-v2)\n\n\n## Quick start\n\n### Installation\n\n```bash\npip install django-amplitude\n```\n\nSet a Amplitude API key in your Django settings:\n```python\n# Settings > Projects > <Your project> > General > API Key\nAMPLITUDE_API_KEY = \'<amplitude-project-api-key>\'\n\n# You can also choose if you want to include user and group data\n# IF not set will default to False\nAMPLITUDE_INCLUDE_USER_DATA = True\nAMPLITUDE_INCLUDE_GROUP_DATA = True\n```\n\nAdd `amplitude` to your `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS =(\n    ...\n    "amplitude",\n    ...\n)\n```\n\n\n## Usage\n\nIf you want to send an event to Amplitude on every page view you can use the django-amplitude `SendPageViewEvent` middleware to your `MIDDLEWARE` in your Django settings.\nThis will automatically create an event base on the url name that was hit and the Django request object.\n\n```python\nMIDDLEWARE = [\n    ...\n    \'amplitude.middleware.SendPageViewEvent\',\n    ...\n]\n```\n\nIf you want to send your own events:\n```python\nfrom amplitude import Amplitude\n\namplitude = Amplitude()\namplitude.send_events([event_data])  # https://developers.amplitude.com/docs/http-api-v2\n```\n\nThere are also few helper functions to build different parts of the event data:\n```python\namplitude.session_id_from_request(request)\namplitude.event_properties_from_request(request)\namplitude.device_data_from_request(request)\namplitude.user_properties_from_request(request)\namplitude.group_from_request(request)\n\namplitude.location_data_from_ip_address(ip_address)\n```\n\n* `user_properties_from_request` will return an empty dict is `AMPLITUDE_INCLUDE_USER_DATA` is `False`\n* `group_from_request` will return an empty dict is `AMPLITUDE_INCLUDE_GROUP_DATA` is `False`\n\n\n\n### SendPageViewEvent - missing event data keys\n\nThe `SendPageViewEvent` middleware currently does not record the following keys from `UploadRequestBody`:\n\n* event_id\n* app_version\n* device_id\n* carrier\n* price\n* quantity\n* revenue\n* productId\n* revenueType\n* idfa\n* idfv\n* adid\n* android_id\n* dma\n* insert_id\n\nIf you want to record an event in Amplitude with any of these keys you must use `amplitude.send_events([event_data])`\n',
    'author': 'Matt Pye',
    'author_email': 'pyematt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyepye/django-amplitude',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
