# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unicode_obfuscate']

package_data = \
{'': ['*'], 'unicode_obfuscate': ['data/*']}

setup_kwargs = {
    'name': 'unicode-obfuscate',
    'version': '0.1.1',
    'description': 'Replace unicode characters with visually similar ones.',
    'long_description': '# unicode obfuscate\n\nReplace unicode characters with visually similar ones.\n\n## Instalation \n\nBe sure to use python >= 3.7\n\n```bash\npip install unicode_obfuscate\n```\n\n## Usage\n\nSimple usage:\n\n```python\n>>> from unicode_obfuscate import Obfuscator\n>>> text = "And Now for Something Completely Different"\n>>> obfuscator = Obfuscator()\n>>> new_text = obfuscator.obfuscate(text)\n>>> new_text\n\'Αnd Νοw fοr Ѕοmеtһіng Сοmрlеtеlу Dіffеrеnt\'\n>>> text == new_text\nFalse\n\n# You can also pass a probability to change only some characters.\n>>> obfuscator.obfuscate(text, prob=0.3) \n\'And Νow for Ѕomething Сompletely Different\'\n```\n\nThere are two different datasets to map the characters:\n- intencional: A very short list with very similar characters (Only one option for each character). The data is taken from [here](https://www.unicode.org/Public/security/latest/intentional.txt).\n- confusables: A gigantic list of characters (and multiple possible characters for each one). The data is taken from [here](https://www.unicode.org/Public/security/latest/confusables.txt).\n\n\nBy default, `intencional` is used but it can change with keyword `kind`:\n\n```python\n# this uses the dataset \'intencional\'\n>>> obfuscator = Obfuscator()  \n\n# this uses the dataset \'confusables\'\n>>> obfuscator = Obfuscator(kind="confusables")  \n```\n\n',
    'author': 'Lucas Bellomo',
    'author_email': 'lbellomo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lbellomo/unicode_obfuscate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
