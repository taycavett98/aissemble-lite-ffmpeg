from pathlib import Path
import time
import boto3
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class S3Handler():
    def __init__(self, bucket_name: Optional[str] = None, region: Optional[str] = None):
        # initialize boto3 s3 client
        self.bucket_name = bucket_name or os.getenv('S3_BUCKET_NAME', 'aissemble-transcribe')
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.s3_client = boto3.client('s3', region_name = self.region)


    def upload_file(self, file_path) -> tuple[str, dict]:
        """This function uploads file to the bucket and returns a uri
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            Tuple of (s3_uri, metrics_dict)
        """
        try:
            from datetime import datetime

            # collect metrics
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)

            filename = Path(file_path).name
            timestamp = datetime.now().strftime("Y%m%d+%H%M%S")
            s3_key = f"input/{timestamp}_{filename}"
            
            logger.info(f"uploading {file_path} to s3://{self.bucket_name}/{s3_key}")

            # time upload
            upload_start = time.time()
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            upload_duration = time.time() - upload_start

            upload_speed_mbps = file_size_mb / upload_duration if upload_duration > 0 else 0

            s3_uri = f"s3://{self.bucket_name}/{s3_key}"

            metrics = {
                's3_upload_time_seconds': round(upload_duration, 3),
                's3_upload_speed_mbps': round(upload_speed_mbps, 2),
                'output_file_size_bytes': file_size_bytes,
                'output_file_size_mb': round(file_size_mb, 2)                
            }

            logger.info(f'Upload successful: {s3_uri} ({upload_duration:.2f}s @ {upload_speed_mbps:.2f} MB/s)')
            return s3_uri, metrics

        except Exception as e:
            logger.error(f'Error in s3 upload. file: {file_path}. error: {str(e)}')
            raise RuntimeError(f"Failed to upload to s3: {str(e)}")