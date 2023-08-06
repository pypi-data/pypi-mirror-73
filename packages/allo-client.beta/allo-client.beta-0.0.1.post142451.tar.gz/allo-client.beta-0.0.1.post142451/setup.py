#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.install import install

import allo
from allo.ansible import AlloAnsible


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        AlloAnsible.do_install_dependencies()


setup(
    name='allo-client.beta',
    version=allo.__version__,
    author="Lukas Hameury",
    author_email="lukas.hameury@libriciel.coop",
    description="Libriciel upgrade package",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.libriciel.fr/libriciel/projets-internes/allo/allo-client",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyInquirer',
        'requests>=2.16.0',
        'gitpython',
        'PyYAML',
        'progressbar2',
        'jsons',
        'ansible'
    ],
    entry_points={
        'console_scripts': [
            'allo = allo.core:launch'
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)
