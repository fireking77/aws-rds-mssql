#!/usr/bin/env python
import global_config
from aws.download_from_s3 import download_from_s3
from aws.upload_to_s3 import upload_to_s3
from cmd_line_parser.set_config import set_config
from global_config.load_config_yaml import load_config_yaml
from mssql.rds_mssql_backup import rds_mssql_backup
from mssql.rds_mssql_connect import rds_mssql_connect
from mssql.rds_mssql_restore import rds_mssql_restore


def main():
    set_config()
    load_config_yaml()

    print('''
Remote Database Tier:   {db_tier}
Remote Database Server: {db_host}
Remote Database Name:   {db_name}
Local MSSQL BAK File:   {sql_bak}
        '''.format(
        db_host=global_config.config_file_parameters['MSSQL']['host'],
        db_name=global_config.config_file_parameters['MSSQL']['name'],
        db_tier=global_config.config_file_parameters['MSSQL']['tier'],
        sql_bak=global_config.sql_bak_file_path))

    if global_config.rds_action == "restore":
        print("This is going to drop the remote database: {db_name}. CTRL+C to break...".format(
            db_name=global_config.config_file_parameters['MSSQL']['name']))
        upload_to_s3()
        rds_mssql_connect()
        rds_mssql_restore()
    else:
        rds_mssql_connect()
        rds_mssql_backup()
        download_from_s3()


if __name__ == '__main__':
    main()
