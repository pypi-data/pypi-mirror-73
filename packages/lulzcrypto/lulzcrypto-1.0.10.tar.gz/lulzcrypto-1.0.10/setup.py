from setuptools import setup, find_packages

setup(
    name='lulzcrypto',
    version='1.0.1',
    packages=find_packages(),
    install_requires=['lulzcode', 'jwt', 'requests'],
    author='LulzLoL231',
    author_email='lznet@pm.me',
    description='simple way for some encrypting.',
    keywords='encrypt crypto lulz lulzcrypto jwt',
    project_urls={
        'Source Code': 'https://github.com/LulzLoL231/lulzcrypto'
    },
    zip_safe=False
)
