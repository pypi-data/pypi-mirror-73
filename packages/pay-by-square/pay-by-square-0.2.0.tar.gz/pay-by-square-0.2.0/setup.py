# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pay_by_square']
setup_kwargs = {
    'name': 'pay-by-square',
    'version': '0.2.0',
    'description': 'Generate QR codes for by square payments',
    'long_description': "# PAY by square\n\nGenerate codes for [by square](https://bysquare.com/) payments.\n\n## Installation\n\nNote: `pay-by-square` generates string that can be passes to QR code generator to create\nimage. To run example below, you need to install\n[qrcode module](https://github.com/lincolnloop/python-qrcode) as well.\n\n```sh\npip install pay-by-square\n```\n\n## Usage\n\n### API\n\n```text\npay_by_square.generate(\n    *,\n    amount: float,\n    iban: str,\n    swift: str = '',\n    date: Optional[date] = None,\n    beneficiary_name: str = '',\n    currency: str = 'EUR',\n    variable_symbol: str = '',\n    constant_symbol: str = '',\n    specific_symbol: str = '',\n    note: str = '',\n    beneficiary_address_1: str = '',\n    beneficiary_address_2: str = '',\n) -> str:\n    Generate pay-by-square code that can by used to create QR code for banking apps\n\n    When date is not provided current date will be used.\n```\n\n### Example\n\n```python\nimport qrcode\nimport pay_by_square\n\n\ncode = pay_by_square.generate(\n    amount=10,\n    iban='SK7283300000009111111118',\n    swift='FIOZSKBAXXX',\n    variable_symbol='47',\n)\n\nprint(code)\nimg = qrcode.make(code)\nimg.show()\n```\n\n## Testing\n\n```sh\npython -m unittest tests.py\n```\n\n---\n\nKudos to [guys from devel.cz](https://devel.cz/otazka/qr-kod-pay-by-square)\n",
    'author': 'Matúš Ferech',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matusf/pay-by-square',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
