import os
import yaml


def read_config(path: str):
    if path is None:
        path = get_config_path()
    with open(path, 'r') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    return config


def get_config_path():
    config_home = os.environ["XDG_CONFIG_HOME"]
    return config_home + "/cleaner-py/config.yaml"
