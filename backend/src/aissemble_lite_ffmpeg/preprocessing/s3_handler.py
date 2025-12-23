from pathlib import Path
import boto3
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class S3Handler():
    def __init__(self, bucket_name: Optional[str] = None, region: Optional[str] = None):
        # initialize boto3 s3 client
        # bucket name and region?
        self.bucket_name = bucket_name or os.getenv('S3_BUCKET_NAME', 'my-bucket')
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.s3_client = boto3.client('s3', region_name = self.region)


    def upload_file(self, file_path) -> str:
        """This function uploads file to the bucket and returns a uri"""
        try:
            from datetime import datetime
            filename = Path(file_path).name
            timestamp = datetime.now().strftime("Y%m%d+%H%M%S")
            s3_key = f"input/{timestamp}_{filename}"
            
            logger.info(f"uploading {file_path} to s3://{self.bucket_name}/{s3_key}")
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)

            s3_uri = f"s3://{self.bucket_name}/{s3_key}"
            logger.info(f'Upload successful: {s3_uri}')
            return s3_uri

        except Exception as e:
            logger.error(f'Error in s3 upload. file: {file_path}. error: {str(e)}')
            raise RuntimeError(f"Failed to upload to s3: {str(e)}")