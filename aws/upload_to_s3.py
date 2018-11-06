#!/usr/bin/env python
import os
import threading

import boto3
from boto3.s3.transfer import TransferConfig

import global_config


def upload_to_s3():
    s3 = boto3.resource(
        's3',
        aws_access_key_id=global_config.config_file_parameters['AWS']['aws_access_key_id'],
        aws_secret_access_key=global_config.config_file_parameters['AWS']['aws_secret_access_key'],
        region_name=global_config.config_file_parameters['AWS']['aws_region_name'])

    config = TransferConfig(  # TODO: We should put these into the global config
        multipart_threshold=1048576,
        max_concurrency=10,
        multipart_chunksize=1048576,
        use_threads=True)

    s3.meta.client.upload_file(
        global_config.sql_bak_file_path,
        global_config.config_file_parameters['AWS']['s3_bucket'],
        global_config.config_file_parameters['AWS']['s3_object_key_name'],
        Config=config,
        Callback=UploadProgressPercentage(global_config.sql_bak_file_path))
    print("")


class UploadProgressPercentage(object):
    def __init__(self, filename):
        # self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print("\rMSSQL Uploading: {so_far} / {total}  {percentage:5.2f}%".format(
                so_far=self._seen_so_far,
                total=self._size,
                percentage=percentage), end='', flush=True)
