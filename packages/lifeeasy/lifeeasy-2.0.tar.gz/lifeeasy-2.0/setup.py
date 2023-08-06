from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "lifeeasy",
packages = ["lifeeasy"],
version = "2.0",
license = "MIT",
description = "A simple python toolbox.",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/lifeeasy",
download_url = "https://github.com/Animenosekai/lifeeasy/archive/v1.6.tar.gz",
keywords = ['tools', 'one-line', 'easy', 'lifeeasy', 'library', 'toolbox', 'developer'],
install_requires = ['requests', 'psutil', 'imagehash', 'Pillow', 'numpy'],
classifiers = ['Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Topic :: Software Development :: Build Tools'],
long_description = readme_description,
long_description_content_type = "text/markdown",
)
