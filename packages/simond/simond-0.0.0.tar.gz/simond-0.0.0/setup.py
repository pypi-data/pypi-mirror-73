from os import path

from setuptools import setup, find_packages

import simond

def long_descr():
    with open(
        path.join(path.abspath(path.dirname(__file__)), 'README.md'),
        encoding='utf-8'
    ) as f:
        return f.read()

setup(
    name='simond',
    version=simond.__version__,
    description=simond.__doc__.strip(),
    license=simond.__license__,
    long_description=long_descr(),
    long_description_content_type='text/markdown',
    author=simond.__author__,
    author_email='ronnyhaase@fastmail.com',
    url='https://github.com/ronnyhaase/simon',
    project_urls={
        "Bug Tracker": "https://github.com/ronnyhaase/simon/issues",
        "Documentation": "https://github.com/ronnyhaase/simon/daemon",
        "Source Code": "https://github.com/ronnyhaase/simon/daemon",
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: System :: Monitoring"
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        'psutil>=5.7,<6',
        'setuptools'
    ],
    extras_require={
        'dev': [
            'pylint'
        ]
    },
    entry_points={
        'console_scripts': [
            'simond = simond.__main__:main'
        ]
    }
)
