# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shadowselenium']

package_data = \
{'': ['*']}

install_requires = \
['pytest-logger>=0.5.1,<0.6.0',
 'pytest>=5.4.3,<6.0.0',
 'selenium>=3.141.0,<4.0.0',
 'webdriver-manager>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'shadowselenium',
    'version': '1.0.0',
    'description': 'This can be used along with selenium to identify Shadow Elements present under Shadow DOM/Shadow Root',
    'long_description': 'Used along with selenium to identify Shadow Elements present under Shadow DOM.\n\nThe Structure of shadow DOM would be as below:\n\nShadow Host -> Shadow Root -> Shadow DOM Elements\n\ncheck the shadow dom by inspecting the website here:\n\nhttps://shrinivasbb.github.io/ShadowDomSite\n\nUse this module to get Shadow DOM Elements matching the CSS selectors.\n\nFor usage check the below link:\n\nhttps://github.com/shrinivasbb/shadowselenium\n\n\nFor implementation check the tests folder.\n\n\n.. code-block:: python\n\n    from shadowselenium import ShadowElement\n\n    shadowdom = ShadowElement(driver) #argument should be driver instance of opened browser i.e chromedriver etc.\n\n    shadowelement = shadowdom.find_shadow_element_by_css("shadow-hostnav", ".nav-link")   \n    \n\n',
    'author': 'Shrinivas Bagewadi',
    'author_email': 'shrinivasbagewadi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
