import os
import subprocess
import progressbar


class AlloAnsible:
    def create_user(self, product):
        self.widgets = [
            'Création de l\'utilisateur de télémaintenance : ', progressbar.AnimatedMarker()
        ]
        self._run_playbook("create_user.yml", '"user_name=libriciel-{}"'.format(product.lower()))

    def install_dependencies(self):
        self.widgets = [
            'Installation des dépendances : ', progressbar.AnimatedMarker()
        ]
        self._run_playbook("install_allo.yml", "")

    def _run_playbook(self, ymlfile, vars):
        corepath = os.path.dirname(os.path.realpath(__file__))
        fh = open("NUL", "w")
        self.process = subprocess.Popen(
            ('ansible-playbook', corepath + "/playbooks/" + ymlfile, "--extra-vars " + vars), stdout=fh, stderr=fh)
        self.ended = False
        self.iterations = 0
        self.bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=self.widgets)

        while not self.ended:
            self.iterations += 1
            self.bar.update(self.iterations)
            self.ended = self._wait()

        fh.close()
        self.bar.finish()

    def _wait(self):
        try:
            self.process.wait(0.2)
            return True
        except subprocess.TimeoutExpired:
            return False
