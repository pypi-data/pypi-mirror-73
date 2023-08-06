from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='api_vk',
    version='1.1',
    author_email='Guerro.dev@mail.ru',
    url='https://github.com/D-Guerro/ApiVk',
    license='Apache 2.0',
    author='Guerro',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
)