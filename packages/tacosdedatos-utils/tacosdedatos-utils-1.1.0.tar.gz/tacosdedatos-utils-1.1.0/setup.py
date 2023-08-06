# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tacosdedatos_utils']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.16.1,<8.0.0',
 'pandas>=1.0.0,<2.0.0',
 'rich>=2.2.2,<3.0.0',
 'typer[all]>=0.2.1,<0.3.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['tacosdedatos-utils = tacosdedatos_utils.__main__:app']}

setup_kwargs = {
    'name': 'tacosdedatos-utils',
    'version': '1.1.0',
    'description': 'Una coleccion de herramientas para facilitar el analisis y visualizacion de datos por @tacosdedatos.',
    'long_description': '# Bienvenidx a la documentación de `tacosdedatos-utils`\n\nUna colección de herramientas para facilitar el análisis y visualización de datos por [@tacosdedatos](https://twitter.com/tacosdedatos).\n\n\n<div align="center">\n\n[![PyPI version](https://badge.fury.io/py/tacosdedatos-utils.svg)](https://badge.fury.io/py/tacosdedatos-utils)\n[![Documentation Status](https://readthedocs.org/projects/tacosdedatos-utils/badge/?version=latest)](https://tacosdedatos-utils.readthedocs.io/es/latest/?badge=latest)\n[![Build status](https://github.com/tacosdedatos/tacosdedatos-utils/workflows/build/badge.svg?branch=master&event=push)](https://github.com/tacosdedatos/tacosdedatos-utils/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/tacosdedatos-utils.svg)](https://pypi.org/project/tacosdedatos-utils/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/tacosdedatos/tacosdedatos-utils/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n[![Descargas mensuales](https://img.shields.io/pypi/dm/tacosdedatos-utils?color=%23dc0d7a&label=descargas)](https://img.shields.io/pypi/dm/tacosdedatos-utils?color=%23dc0d7a&label=descargas)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/tacosdedatos/tacosdedatos-utils/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/tacosdedatos/tacosdedatos-utils/releases)\n[![License](https://img.shields.io/github/license/tacosdedatos/tacosdedatos-utils)](https://github.com/tacosdedatos/tacosdedatos-utils/blob/master/LICENSE)\n\n</div>\n\n## Que trae\n\n* la función `arbol` para mostrar los contenidos de la carpeta que le pases.\n```python\nfrom tacosdedatos_utils.manejo_de_archivos import arbol\n\narbol("./notebooks")\n>>>> + notebooks\n        + Cpp.ipynb\n        + Data.ipynb\n        + Fasta.ipynb\n        + Lorenz.ipynb\n        + R.ipynb\n        + audio\n            + audio.wav\n        + bqplot.ipynb\n        + images\n            + marie.png\n            + xeus-cling.png\n            + xtensor.png\n            + xwidgets.png\n        + lorenz.py\n        + pandas.ipynb\n```\n\n* la función `crear_proyecto`\n```python\nfrom tacosdedatos_utils.manejo_de_proyectos import crear_proyecto\nfrom tacosdedatos_utils.manejo_de_archivos import arbol\n\ncrear_proyecto(nombre = "proyecto-de-analisis-de-datos")\n\narbol("proyecto-de-analisis-de-datos/")\n>>>> + proyecto-de-analisis-de-datos\n        + AUTORES.md\n        + README.md\n        + datos\n            + brutos\n            + externos\n            + finales\n            + interinos\n            + procesados\n        + docs\n        + notebooks\n        + reportes\n            + figuras\n        + src\n            + apps\n            + datos\n            + externos\n            + herramientas\n            + modelos\n            + visualizaciones\n```\nque también funciona desde tu línea de comandos.\n\n![GIF mostrando como usar la linea de comandos con tacosdedatos-utils](https://github.com/chekos/pics_for_github/blob/master/2020-06-17%2014.06.39.gif?raw=true)\n\n\n## 📃 Citeishon\n\n```\n@misc{tacosdedatos-utils,\n  author = {tacosdedatos},\n  title = {Una coleccion de herramientas para facilitar el analisis y visualizacion de datos por @tacosdedatos.},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/tacosdedatos/tacosdedatos-utils}}\n}\n```\n\n> Este proyecto fue generado con [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'tacosdedatos',
    'author_email': 'chekos@tacosdedatos.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tacosdedatos/tacosdedatos-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
