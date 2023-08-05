import os


class AlloAnsible:
    @staticmethod
    def do_install_dependencies():
        corepath = os.path.dirname(os.path.realpath(__file__))
        command = "ansible-playbook {}/playbooks/install_allo.yml".format(corepath)
        oscall_result = os.system(command)
        if os.WEXITSTATUS(oscall_result) != 0:
            print("Error on dependencies installation")
            return os.WEXITSTATUS(oscall_result)
        return 0

    @staticmethod
    def do_add_product_user(product):
        corepath = os.path.dirname(os.path.realpath(__file__))
        command = "ansible-playbook " \
                  "--extra-vars \"user_name=libriciel-{}\" " \
                  "{}/playbooks/create_user.yml".format(product.lower(), corepath)
        oscall_result = os.system(command)
        if os.WEXITSTATUS(oscall_result) != 0:
            print("Error on user creation")
            return os.WEXITSTATUS(oscall_result)
        return 0
