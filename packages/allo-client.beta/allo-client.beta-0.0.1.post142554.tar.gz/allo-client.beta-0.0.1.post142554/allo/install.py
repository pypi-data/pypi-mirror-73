#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import progressbar


class InstallDependencies:

    def __init__(self):
        widgets = [
            'Installation des dépendances : ', progressbar.AnimatedMarker()
        ]
        corepath = os.path.dirname(os.path.realpath(__file__))
        fh = open("NUL","w")
        self.process = subprocess.Popen(('ansible-playbook', corepath + "/playbooks/install_allo.yml"), stdout = fh, stderr = fh)
        self.ended = False
        self.iterations = 0
        self.bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=widgets)

        while not self.ended:
            self.iterations += 1
            self.bar.update(self.iterations)
            self.ended = self._wait()

        fh.close()

    def _wait(self):
        try:
            self.process.wait(0.2)
            return True
        except subprocess.TimeoutExpired:
            return False
