#!/usr/bin/env python
# -*- coding: utf-8 -*-
import allo
import click


@click.group(invoke_without_command=True, help="Lancement de allo")
@click.version_option()
@click.pass_context
def default(ctx):
    print("ALLO-NG v{} - Utilitaire de mise a jour automatique et telemaintenance".format(allo.__version__))
    """Allo CLI program."""
    if not ctx.invoked_subcommand:
        try:
            from allo.core import TestingAllo
            TestingAllo("PROD")
        except ImportError:
            install()
            from allo.core import TestingAllo
            TestingAllo("PROD")


@default.command(help="Installation de dependances allo")
def install():
    from allo.install import InstallDependencies
    InstallDependencies()


@default.command(help="Utilisation de allo en mode CLI, sans fichier de configuration")
def cli():
    # do something here
    print("TODO")
