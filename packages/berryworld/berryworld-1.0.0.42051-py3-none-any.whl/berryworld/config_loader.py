import os


class ConfigLoader:
    """ Class to access credentials where it on the cloud or in local"""

    def __init__(self, file_local):
        try:
            self.secret_path = '/mnt/secrets-store/'
            if os.environ["KEY_VAULT_VOLUME_NAME"]:
                self.secret_path = os.environ["KEY_VAULT_VOLUME_NAME"]
        except:
            self.file_local = file_local

    def get(self, key_name):
        """I want here to execute creds"""
        if os.path.isfile(self.secret_path + key_name):
            return open(self.secret_path + key_name, 'r').read()
        elif os.environ[key_name]:
            return os.environ[key_name]

