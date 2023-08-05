# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['texturize']

package_data = \
{'': ['*']}

install_requires = \
['creativeai>=0.1.1,<0.2.0',
 'docopt>=0.6.2,<0.7.0',
 'progressbar2>=3.51.3,<4.0.0',
 'schema>=0.7.2,<0.8.0']

entry_points = \
{'console_scripts': ['texturize = texturize.__main__:main']}

setup_kwargs = {
    'name': 'texturize',
    'version': '0.9.0',
    'description': '🤖🖌️ Automatically generate new textures similar to a source photograph.',
    'long_description': 'neural-texturize\n================\n\n.. image:: docs/gravel-x4.webp\n\nA command-line tool and Python library to automatically generate new textures similar\nto a source image or photograph.  It\'s useful in the context of computer graphics if\nyou want to make variations on a theme or expand the size of an existing texture.\n\nThis tool is powered by deep learning technology — using a combination of convolution\nnetworks and example-based optimization to synthesize images.  We\'re aiming to make\n``neural-texturize`` the highest-quality open source library available!\n\n1. `Examples & Demos <#1-examples--demos>`_\n2. `Installation <#2-installation>`_\n3. `Commands & Usage <#3-commands--usage>`_\n\n|Python Version| |License Type| |Project Stars|\n\n\n1. Examples & Demos\n===================\n\nThe examples are available as notebooks, and you can run them directly in-browser\nthanks to Jupyter and Google Colab:\n\n* **Gravel** — `online demo <https://colab.research.google.com/github/photogeniq/neural-texturize/blob/master/examples/Demo_Gravel.ipynb>`__ and `source notebook <https://github.com/photogeniq/neural-texturize/blob/master/examples/Demo_Gravel.ipynb>`__.\n* **Grass** — `online demo <https://colab.research.google.com/github/photogeniq/neural-texturize/blob/master/examples/Demo_Grass.ipynb>`__ and `source notebook <https://github.com/photogeniq/neural-texturize/blob/master/examples/Demo_Grass.ipynb>`__.\n\nThese demo materials are released under the Creative Commons `BY-NC-SA license <https://creativecommons.org/licenses/by-nc-sa/3.0/>`_, including the text, images and code.\n\n.. image:: docs/grass-x4.webp\n\n\n2. Installation\n===============\n\nIf you\'re a developer and want to install the library locally, start by cloning the\nrepository to your local disk:\n\n.. code-block:: bash\n\n    git clone https://github.com/photogeniq/neural-texturize.git\n\nThen, you can create a new virtual environment called ``myenv`` by installing\n`Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ and calling the following\ncommands, depending whether you want to run on CPU or GPU (via CUDA):\n\n.. code-block:: bash\n\n    cd neural-texturize\n\n    # a) Use this if you have an *Nvidia GPU only*.\n    conda env create -n myenv -f tasks/setup-cuda.yml\n\n    # b) Fallback if you just want to run on CPU.\n    conda env create -n myenv -f tasks/setup-cpu.yml\n\nOnce the virtual environment is created, you can activate it and finish the setup of\n``neural-texturize`` with these commands:\n\n.. code-block:: bash\n\n    conda activate myenv\n    poetry install\n\nFinally, you can check if everything worked by calling the script:\n\n.. code-block:: bash\n\n    texturize\n\nYou can use ``conda env remove -n myenv`` to delete the virtual environment once you\nare done.\n\n\n3. Commands & Usage\n===================\n\nThe main script takes a source image as a texture, and generates a new output that\ncaptures the style of the original.  Here are some examples:\n\n.. code-block:: bash\n\n    texturize samples/grass.webp --size=1440x960 --output=result.png\n    texturize samples/gravel.png --iterations=200 --precision=1e-5\n    texturize samples/sand.tiff  --output=tmp/{source}-{octave}.webp\n    texturize samples/brick.jpg  --device=cpu\n\n\nFor details about the command-line options, see the tool itself:\n\n.. code-block:: bash\n\n    texturize --help\n\nHere are the command-line options currently available::\n\n    Usage:\n        texturize SOURCE... [--size=WxH] [--output=FILE] [--variations=V] [--seed=SEED]\n                            [--mode=MODE] [--octaves=O] [--threshold=H] [--iterations=I]\n                            [--device=DEVICE] [--precision=PRECISION] [--quiet] [--verbose]\n\n    Options:\n        SOURCE                  Path to source image to use as texture.\n        -s WxH, --size=WxH      Output resolution as WIDTHxHEIGHT. [default: 640x480]\n        -o FILE, --output=FILE  Filename for saving the result, includes format variables.\n                                [default: {source}_gen{variation}.png]\n        --variations=V          Number of images to generate at same time. [default: 1]\n        --seed=SEED             Configure the random number generation.\n        --mode=MODE             Either "patch" or "gram" to specify critics. [default: gram]\n        --octaves=O             Number of octaves to process. [default: 5]\n        --threshold=T           Quality for optimization, lower is better. [default: 1e-4]\n        --iterations=I          Maximum number of iterations each octave. [default: 99]\n        --device=DEVICE         Hardware to use, either "cpu" or "cuda".\n        --precision=PRECISION   Floating-point format to use, "float16" or "float32".\n        --quiet                 Suppress any messages going to stdout.\n        --verbose               Display more information on stdout.\n        -h, --help              Show this message.\n\n----\n\n\nPyPI:\n\n.. image:: https://img.shields.io/pypi/dw/texturize?label=installs\n    :alt: PyPI - Installs\n\nSamples:\n\n.. image:: https://img.shields.io/github/downloads/photogeniq/neural-texturize/v0.0/total\n    :alt: GitHub Releases\n\nTotal:\n\n.. image:: https://img.shields.io/github/downloads/photogeniq/neural-texturize/total\n    :alt: GitHub - Downloads\n\nThat is for `image-encoders`:\n\n.. image:: https://img.shields.io/github/downloads/photogeniq/image-encoders/total\n    :alt: GitHub - Downloads\n\n----\n\n|Python Version| |License Type| |Project Stars|\n\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/texturize\n    :target: https://www.python.org/\n\n.. |License Type| image:: https://img.shields.io/badge/license-AGPL-blue.svg\n    :target: https://github.com/photogeniq/neural-texturize/blob/master/LICENSE\n\n.. |Project Stars| image:: https://img.shields.io/github/stars/photogeniq/neural-texturize.svg?style=flat\n    :target: https://github.com/photogeniq/neural-texturize/stargazers\n',
    'author': 'Alex J. Champandard',
    'author_email': '445208+alexjc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/photogeniq/neural-texturize',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
