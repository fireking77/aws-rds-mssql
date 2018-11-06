# AWS RDS MSSQL Backup and Restore Utility

# Prolog

First of all, this is my first Python project. So feel free to make a codereview and give me some constructive advice if you see something and would like to mention.

## What is this?

In one of my automatisation project We have to use AWS RDS MSSQL, not just in production in the development pipeline also.
So it is hard to use it and script it with aws.cli.

This script has only 2 purpose:
- Backup and download from an RDS deployment.
- Upload and restore into an RDS deployment.

Tested platforms:
- Linux
- Windows 10


#### AWS Magic is used by me

We use the AWS stored procedure to make and restore backup
- [msdb.dbo.rds_backup_database](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/SQLServer.Procedural.Importing.html#SQLServer.Procedural.Importing.Native.Using.Backup)
- [msdb.dbo.rds_restore_database](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/SQLServer.Procedural.Importing.html#SQLServer.Procedural.Importing.Native.Using.Restore)

## Build

```bash
git clone <this poject>
pip install -r requirements.txt
pyinstaller --onefile aws-rds-mssql.py
```

## Config file (Yaml style)
```
AWS:
  aws_access_key_id: "aws_access_key_id"
  aws_secret_access_key: "aws_secret_access_key"
  aws_region_name: "aws_region_name"
  s3_bucket: "s3_bucket"
  s3_object_key_name: "<TIER>/<DB Name>.bak"  # bak_file_name

MSSQL:
  tier: "DEVELOPMENT"   #DEVELOPMENT, PRODUCTION(extra caution)
  user: "db-user"
  pass: "db-pass"
  host: "db-host" #RDS Host
  port: 1433
  name: "db-name"
```

## Howto use?
```bash
 help:
    aws-rds-mssql --help

 backup:
    aws-rds-mssql --config-file config.yml --sql-bak-file mssql.bak backup

 restore:
    aws-rds-mssql --config-file config.yml --sql-bak-file mssql.bak restore   
```

## Happy backuping :)

## TODO
 - There is no error handling
 - Compressed backup
 - support some scenario with cache in the intermediate S3 storage
 - extra security with PROD tiers
 - and so on :)

##### Contact with me on Linkedin
[Istvan Darvas](https://www.linkedin.com/in/istvandarvas/)
