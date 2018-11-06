#!/usr/bin/env python
import argparse

import global_config


def set_config():
    """
    It's going to manage the command line arguments. Everything is going to be set in a specific global variable

    :return: global_config.rds_action
        global_config.config_file_path
        global_config.sql_bak_file_path
    """

    parser = argparse.ArgumentParser(
        prog='aws-rds-mssql',
        description='''AWS RDS / MSSQL backup and restore utility''',
        epilog='''
            Made by Darvi | System Architect - SRE / DevOps
            https://www.linkedin.com/in/istvandarvas/
             ''')
    parser.add_argument('rds_action',
                        choices=['backup', 'restore'],
                        help="Action to take")
    parser.add_argument("-c", "--config-file",
                        dest="config_file_path",
                        type=str,
                        required=True,
                        help="Configuration file")
    parser.add_argument("-bak", "--sql-bak-file",
                        dest="sql_bak_file_path",
                        type=str,
                        required=True,
                        help="Path to the MSSQL \"bak\" file")

    args = parser.parse_args()

    global_config.rds_action = args.rds_action
    global_config.config_file_path = args.config_file_path
    global_config.sql_bak_file_path = args.sql_bak_file_path
