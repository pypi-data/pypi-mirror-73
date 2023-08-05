# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shrtcodes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shrtcodes',
    'version': '0.3.0',
    'description': 'Simple shortcodes for Python.',
    'long_description': '# shrtcodes\n\n[![Build Status](https://travis-ci.org/Peter554/shrtcodes.svg?branch=master)](https://travis-ci.org/Peter554/shrtcodes)\n\n`pip install shrtcodes`\n\nSimple shortcodes for Python.\n\n## Example\n\nText containing shortcodes.\n\n- `img` - a shortcode.\n- `details` - a paired shortcode.\n\n```text\nFoo bar baz.\n\n{% img "https://images.com/cutedog.jpg", "A cute dog!" %}\n\n{% details "Some extra info" %}\nThis is some extra info.\n{% enddetails %}\n\nFoo bar baz.\n```\n\nBuild your shortcodes:\n\n```python\n# shortcodes.py\n\nfrom shrtcodes.shrtcodes import Shrtcodes\n\nshortcodes = Shrtcodes()\n\n# `img_handler` is a shortcode handler. \n#   * Arguments correspond to the shortcode parameters.  \n@shortcodes.register(\'img\')\ndef img_handler(src, alt):\n    return f\'<img src="{src}" alt="{alt}"/>\'\n\n# `details_handler` is a paired shortcode handler.\n#   * First argument is the contained block.\n#   * Subsequent arguments correspond to the shortcode parameters.\n@shortcodes.register_paired(\'details\')\ndef details_handler(details, summary):\n    return f\'<details><summary>{summary}</summary>{details}</details>\'\n```\n\nUse your shortcodes:\n\n```python\nfrom shortcodes import shortcodes\ntext = shortcodes.process(\'...\')\n```\n\nOutput:\n\n```text\nFoo bar baz.\n\n<img src="https://images.com/cutedog.jpg" alt="A cute dog!"/>\n\n<details><summary>Some extra info</summary>This is some extra info.</details>\n\nFoo bar baz.\n```\n\n## Further examples\n\nSee the tests.\n',
    'author': 'Peter Byfield',
    'author_email': 'byfield554@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Peter554/shrtcodes#readme',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
