#!/usr/bin/env python
import threading

import boto3
from boto3.s3.transfer import TransferConfig

import global_config


def download_from_s3():
    s3 = boto3.resource(
        's3',
        aws_access_key_id=global_config.config_file_parameters['AWS']['aws_access_key_id'],
        aws_secret_access_key=global_config.config_file_parameters['AWS']['aws_secret_access_key'],
        region_name=global_config.config_file_parameters['AWS']['aws_region_name']
    )

    config = TransferConfig(  # TODO: We should put these into the global config
        multipart_threshold=1048576,
        max_concurrency=10,
        multipart_chunksize=1048576,
        use_threads=True
    )

    s3_object = s3.Object(
        global_config.config_file_parameters['AWS']['s3_bucket'],
        global_config.config_file_parameters['AWS']['s3_object_key_name']
    )

    with open(global_config.sql_bak_file_path, 'wb') as sql_bak_file:
        s3_object.download_fileobj(
            sql_bak_file,
            Config=config,
            Callback=DownloadProgressPercentage(s3_object))
    print("")


class DownloadProgressPercentage(object):
    def __init__(self, object):
        self._size = object.content_length
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print("\rMSSQL Downloading: {so_far} / {total}  {percentage:5.2f}%".format(
                so_far=self._seen_so_far,
                total=self._size,
                percentage=percentage), end='', flush=True)
