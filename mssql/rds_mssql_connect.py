#!/usr/bin/env python
import pymssql

import global_config


def rds_mssql_connect():
    global_config.aws_rds_mssql_connection = pymssql.connect(
        server=global_config.config_file_parameters['MSSQL']['host'],
        user=global_config.config_file_parameters['MSSQL']['user'],
        password=global_config.config_file_parameters['MSSQL']['pass'],
        database="tempdb",
        autocommit=True
    )
