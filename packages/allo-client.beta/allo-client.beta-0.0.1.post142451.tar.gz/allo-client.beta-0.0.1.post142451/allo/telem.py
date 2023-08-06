# -*- coding: utf-8 -*-

import os
import subprocess
from .model.config import AlloConfig
from .const import *


class AlloTelem:
    config_file = str(Path.home()) + "/teleport-config.yml"

    def __init__(self, config: AlloConfig):
        if not os.path.exists(self.config_file):
            self.save_config(config)

    def save_config(self, config):
        teleport_yaml = ("teleport:",
                         "    nodename: {}-{}".format(config.id_client, config.code_produit),
                         '    auth_token: "{}"'.format(config.teleport_token),
                         '    ca_pin: "sha256:dd7a6f23f45a08ca2f80d00aa03aa81cbaf5b230614d7cf4f85f813d70d46abd"',
                         '    auth_servers:',
                         '        - {}:443'.format(ALLO_URL),
                         'auth_service:',
                         '    enabled: no',
                         'proxy_service:',
                         '    enabled: no',
                         'ssh_service:',
                         '    enabled: "yes"',
                         '    labels:',
                         '        product: {}'.format(config.code_produit),
                         '        client_id: {}'.format(config.id))

        with open(self.config_file, 'w+') as yaml_file:
            yaml_file.write('\n'.join(teleport_yaml))

    def connect(self):
        with subprocess.Popen(["sudo", "teleport", "start", '-c', self.config_file],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            try:
                print("Télémaintenance ouverte. Pour l'interrompre, utilisez le raccourci clavier CTRL+C")
                proc.wait()
            except KeyboardInterrupt:
                print("Fin de télémaintenance")
