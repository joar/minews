from distutils.core import setup

setup(
    name='minews',
    description='Libre Projects feed aggregator',
    version='0.1',
    packages=['minews'],
    install_requires=[
        'tornado',
        'django',
        'feedparser'
        ])
