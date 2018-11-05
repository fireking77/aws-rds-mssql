#!/usr/bin/env python
import time

import global_config


def rds_mssql_backup():
    cursor = global_config.aws_rds_mssql_connection.cursor()

    # Cheking ongoing tasks
    cursor.execute("exec msdb.dbo.rds_task_status")
    row = cursor.fetchone()
    if row[5] != "SUCCESS" and row[5] != "ERROR":
        raise Exception("Thre is a running task...")

    # MSSQL Backup procedure
    cursor.execute("""
        exec msdb.dbo.rds_backup_database 
            @source_db_name='{db_name}', 
            @s3_arn_to_backup_to='arn:aws:s3:::{s3_bucket}/{s3_object_key_name}',
            @overwrite_S3_backup_file=1,
            @type='full';
    """.format(
        s3_bucket=global_config.config_file_parameters['AWS']['s3_bucket'],
        s3_object_key_name=global_config.config_file_parameters['AWS']['s3_object_key_name'],
        db_name=global_config.config_file_parameters['MSSQL']['name'])
    )

    row = cursor.fetchone()
    task_id = row[0]

    # Checking Taskid
    cursor.execute("exec msdb.dbo.rds_task_status @task_id={id}".format(id=str(task_id)))
    row = cursor.fetchone()

    while row[5] != "SUCCESS" and row[5] != "ERROR" and row[3] != "100":
        time.sleep(5)
        print("\rMSSQL Backup - creating: {progress}% ".format(
            progress=row[3]
        ), end='', flush=True)
        cursor.execute("exec msdb.dbo.rds_task_status @task_id={id}".format(id=str(task_id)))
        row = cursor.fetchone()
    print("", flush=True)

    print("MSSQL Backup - copying: ", end='', flush=True)
    while row[5] != "SUCCESS" and row[5] != "ERROR":
        time.sleep(1)
        print(".", end='', flush=True)
        cursor.execute("exec msdb.dbo.rds_task_status @task_id={id}".format(id=str(task_id)))
        row = cursor.fetchone()

    if row[5] == "SUCCESS":
        print("Copied")
    else:
        print("Error")
        raise Exception("Backup was not success...")
