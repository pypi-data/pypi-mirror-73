from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '1.0.0'
download_url = 'https://github.com/philliphqs/hqscord/archive/1.0.0.tar.gz'

try:
    setup(
        name='hqscord',
        version=version,
        author='philliphqs',
        description='For hqs.bot to create cogs (faster)',
        license='MIT',
        keywords='hqs, philliphqs, hqs.bot, hqsartworks, hqsartworks.me, discord, discord.py',
        url='https://github.com/philliphqs/hqscord',
        download_url=download_url,
        packages=['hqscord'],
        install_requires=['discord', 'time'],
        classifiers=[
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"

        ]
    )
except Exception:
    setup(
        name='hqscord',
        version=version,
        author='philliphqs',
        description='For hqs.bot to create cogs (faster)',
        license='MIT',
        keywords='hqs, philliphqs, hqs.bot, hqsartworks, hqsartworks.me, discord, discord.py',
        url='https://github.com/philliphqs/hqscord',
        download_url=download_url,
        packages=['hqscord'],
        install_requires=['discord', 'time'],
        classifiers=[
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"

        ]
    )