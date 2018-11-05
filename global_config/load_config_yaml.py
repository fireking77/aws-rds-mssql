#!/usr/bin/env python
import yaml

import global_config


def load_config_yaml():
    """
    It's going to load and set the configuration parameters

    :return: global_config.config_file_parameters
    """

    config_yaml = open(global_config.config_file_path, 'r')
    global_config.config_file_parameters = yaml.load(config_yaml)
