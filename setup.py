from setuptools import setup

# TODO:
# * [x] Check installed Java version
# * [x] Check installed Python version
# * [x] Install dependencies from requirements.txt? Or is it not necessary?
# * [ ] Install idml2xml-frontend
# * [ ] Instantiate a .env file

setup(
    name='idml2docbook',
    version='0.1.0',
    description='IDML to DocBook file converter',
    author='Yann Trividic',
    author_email='bonjour@yanntrividic.fr',
    url='https://gitlab.com/deborderbollore/idml-pandoc-reader',
    packages=['idml2docbook'],
    # scripts=['idml2docbook.py'],
    # packages=find_packages()
    install_requires=[
        "bs4==0.0.2",
        "lxml>=6.0.0",
        "python-dotenv>=1.1.0",
        "unidecode>=1.4.0"
    ],
)