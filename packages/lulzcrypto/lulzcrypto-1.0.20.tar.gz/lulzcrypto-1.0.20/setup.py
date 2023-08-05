from setuptools import setup, find_packages

setup(
    name='lulzcrypto',
    version='1.0.2',
    packages=find_packages(),
    install_requires=['lulzcode', 'pyjwt', 'requests'],
    author='LulzLoL231',
    author_email='lznet@pm.me',
    description='Simple way for some encrypting.',
    keywords='encrypt crypto lulz lulzcrypto pyjwt',
    project_urls={
        'Source Code': 'https://github.com/LulzLoL231/lulzcrypto'
    },
    zip_safe=False
)
