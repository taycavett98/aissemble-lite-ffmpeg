import json
import logging
import os
from pathlib import Path
import time
from .ffmpeg_handler import FfmpegHandler
from .s3_handler import S3Handler

ACCEPTABLE_TYPES = {'.mp3', '.mp4', '.wav', '.m4a', '.flac', '.avi'}  # Use set for O(1) lookup

logger = logging.getLogger(__name__)

class InputHandler():
    def __init__(self):
        self.ffmpeg_handler = FfmpegHandler()
        self.s3_handler = S3Handler()
        self.output_dir = Path("output/metrics")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.save_metrics = os.getenv('SAVE_METRICS', 'true').lower() == 'true' # make it boolean by adding comperative operator

    def _check_file_extension(self, file_path: str):
        # check if file exists, raise error if not found
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File not found: {file_path}')

        file_path_obj = Path(file_path)
        extension = file_path_obj.suffix

        if extension not in ACCEPTABLE_TYPES:
            raise ValueError(f"Unsupported file type: {extension}. Supported files: {ACCEPTABLE_TYPES}")


    def _ensure_wav(self, input_file_path):
        """This function accepts an input file and returns .wav format. Always to ensure it is standardized."""
        output, metrics = self.ffmpeg_handler.convert_to_wav(input_file_path)
        
        return output, metrics
    
    def _save_metrics(self, metrics: dict, filename: str, s3_uri:str)->None:
        """
        This function will accept metrics from the filename and its s3 uri and write
        them to the output directory
        """
        filename_stem = Path(filename).stem
        metrics_filename = f"{filename_stem}.json"
        metrics_path = self.output_dir / metrics_filename

        full_metrics = {
            'filename': filename,
            's3_uri': s3_uri,
            'metrics': metrics
        }

        with open(metrics_path, 'w') as f:
            json.dump(full_metrics, f, indent=2)

        logger.info(f'metrics saved to {metrics_path}')

    def process_input(self, input: str, original_filename: str) -> tuple[str, dict]:
        """This function ensures the file is in .wav format and gets a uri from the s3
            bucket so that we can pass a uri to the aws transcribe function.

            FFmpegHandler class is used to convert the audio as well as standardize the
            audio input for the highest quality. 
        
        """
        start_time = time.time()
        wav_filepath = None
        try:
            # check if input extension is in acceptable types
            self._check_file_extension(input)

            wav_filepath, ffmpeg_metrics = self._ensure_wav(input)
            
            s3_uri, s3_metrics = self.s3_handler.upload_file(file_path=wav_filepath)

            if not s3_uri:
                raise RuntimeError(f"Failed to upload {wav_filepath} to S3")
            
            total_time = time.time() - start_time

            metrics = {
                'total_processing_time_seconds': round(total_time, 3),
                **ffmpeg_metrics,
                **s3_metrics
            }

            self._save_metrics(metrics, original_filename, s3_uri)

            return s3_uri, metrics
        
        finally:
            if wav_filepath and os.path.exists(wav_filepath):
                try:
                    os.unlink(wav_filepath)
                    logger.info(f"cleaned up temp WAV file: {wav_filepath}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {wav_filepath}, {str(e)}")