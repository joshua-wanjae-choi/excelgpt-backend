import shutil
import os


class SecretUtil:
    @staticmethod
    def load_secret(secret_path: str, docker_secret_name: str):
        if os.path.isfile(secret_path):
            return True

        docker_secret_dir_path = "/run/secrets"
        docker_secret_path = f"{docker_secret_dir_path}/{docker_secret_name}"
        if not os.path.isfile(docker_secret_path):
            return False

        shutil.copyfile(docker_secret_path, secret_path)

