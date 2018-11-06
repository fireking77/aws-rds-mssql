#!/usr/bin/env python
import time

import global_config


def rds_mssql_restore():
    cursor = global_config.aws_rds_mssql_connection.cursor()

    # Cheking ongoing tasks
    cursor.execute("exec msdb.dbo.rds_task_status")
    row = cursor.fetchone()
    if row[5] != "SUCCESS" and row[5] != "ERROR":
        raise Exception("Thre is a running task...")

    # Drop database if exists
    cursor.execute("DROP DATABASE IF EXISTS [{db_name}];".format(
        db_name=global_config.config_file_parameters['MSSQL']['name']
    ))

    # MSSQL Restore procedure
    cursor.execute("""
        exec msdb.dbo.rds_restore_database
            @restore_db_name='{db_name}',
            @s3_arn_to_restore_from='arn:aws:s3:::{s3_bucket}/{s3_object_key_name}';
    """.format(
        s3_bucket=global_config.config_file_parameters['AWS']['s3_bucket'],
        s3_object_key_name=global_config.config_file_parameters['AWS']['s3_object_key_name'],
        db_name=global_config.config_file_parameters['MSSQL']['name']))

    row = cursor.fetchone()
    task_id = row[0]

    # Checking Taskid
    cursor.execute("exec msdb.dbo.rds_task_status @task_id={id}".format(id=str(task_id)))
    row = cursor.fetchone()

    while row[5] != "SUCCESS" and row[5] != "ERROR" and row[3] != "100":
        time.sleep(5)
        print("\rMSSQL Restore: {progress}% ".format(
            progress=row[3]
        ), end='', flush=True)
        cursor.execute("exec msdb.dbo.rds_task_status @task_id={id}".format(id=str(task_id)))
        row = cursor.fetchone()
    print("", flush=True)

    if row[5] == "SUCCESS":
        print("MSSQL Restore: Done")
    else:
        print("MSSQL Restore: Error")
        raise Exception("Restore was not success...")
