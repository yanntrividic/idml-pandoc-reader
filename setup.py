from setuptools import setup
from idml2docbook import VERSION

setup(
    name='idml2docbook',
    version=VERSION,
    description='IDML to DocBook file converter',
    author='Yann Trividic',
    author_email='bonjour@yanntrividic.fr',
    url='https://gitlab.com/deborderbollore/idml-pandoc-reader',
    packages=['idml2docbook'],
    install_requires=[
        "bs4==0.0.2",
        "lxml>=6.0.0",
        "python-dotenv>=1.1.0",
        "unidecode>=1.4.0",
        "packaging>=25.0"
    ],
)