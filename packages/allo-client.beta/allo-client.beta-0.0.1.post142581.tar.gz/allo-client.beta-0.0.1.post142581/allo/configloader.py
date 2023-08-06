# -*- coding: utf-8 -*-
import pickle

from PyInquirer import prompt
from .model.config import AlloConfig
from .model.version import Version
from .model.colors import BColors
from .const import *
from .alloapi import AlloAPI
from .ansible import AlloAnsible


class ConfigLoader:
    config: AlloConfig

    __error_config_msg = "Erreur de configuration, sortie du programme Allo"

    def __init__(self, env):
        try:
            with open(CONFIG_PATH, 'rb') as config_dictionary_file:
                self.config = pickle.load(config_dictionary_file)
        except FileNotFoundError:
            self.config = AlloConfig()
            self.config.env = env
            self.ask_user_configuration()
            # Create specific user to access node
            AlloAnsible().create_user(self.config.code_produit)

    def ask_user_configuration(self):
        print(BColors.OKBLUE + "Merci de rentrer les informations suivantes afin d'initialiser Allo :")
        self.ask_for_client_info()
        
        versions = AlloAPI.list_version(self.config)
        if not versions:
            print(BColors.FAIL + self.__error_config_msg)
            exit(1)
        else:
            qversions = []
            for v in versions:
                qversions.append({"value": "0", "name": v['name']})
            questions = [{'type': 'list',
                          'name': 'version',
                          'message': 'Version du produit',
                          'choices': qversions}]
            answers = prompt(questions)
            self.config.version = Version(versions[int(answers['version'])])

        if self.verify():
            self.config.teleport_token = prompt(
                [{'type': 'input', 'name': 'teleport_token', 'message': 'Token de télémaintenance'}])['teleport_token']
            # disable repo_path for now
            # self.config.repo_path = prompt(
            #     [{'type': 'input', 'name': 'repo_path', 'message': 'Chemin d\'installation du logiciel'}])['repo_path']
            self.save()
        else:
            print(BColors.FAIL + "Erreur de configuration, sortie du programme Allo")
            exit(1)

    def verify(self):
        status = AlloAPI.register(self.config)
        if not status:
            print(BColors.FAIL + self.__error_config_msg)
            exit(1)
        if not status['active']:
            cfg = prompt([{'type': 'input', 'name': 'pin_code', 'message': 'Code PIN d\'activation Allo'}])
            AlloAPI.activate(self.config, cfg['pin_code'])
        print(BColors.OKGREEN + "Connexion Allo OK")
        return True

    def ask_for_client_info(self):
        questions = [{'type': 'input', 'name': 'id_client', 'message': 'Identifiant unique Client'},
                     {'type': 'input', 'name': 'code_produit', 'message': 'Code Produit'}]
        cfg = prompt(questions)
        self.config.id_client = cfg['id_client']
        self.config.code_produit = cfg['code_produit']

    def save(self):
        with open(CONFIG_PATH, 'wb') as config_dictionary_file:
            pickle.dump(self.config, config_dictionary_file)
