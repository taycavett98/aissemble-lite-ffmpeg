import os
import time
import ffmpeg
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

class FfmpegHandler():
    def __init__(self):
        logger.info('initializing ffmpeg object')

    def convert_to_wav(self, input_file) -> tuple[str, dict]:
        """This function will accept a file and convert it into a wav file and return a new file
        Args:
            input_file: Path to input file
            
        Returns:
            Tuple of (output_filename, metrics_dict)        
        """

        try:
            input_path = Path(input_file)
            output_name = f'{input_path.stem}_converted.wav'

            # collect metrics
            input_size_bytes = os.path.getsize(input_file)
            input_size_mb = input_size_bytes / (1024 * 1024)
            
            logger.info(f"Converting {input_file} ({input_size_mb:.2f} MB) to WAV format")

            convert_start = time.time()
            ffmpeg.input(input_file).output(
                output_name,
                ar=16000, # 16kHz sample rate
                ac=1, # mono channel 
                acodec='pcm_s16le' # 16-bit PCM
            ).run(overwrite_output=True)
            convert_duration = time.time() - convert_start

            output_size_bytes = os.path.getsize(output_name)
            output_size_mb = output_size_bytes / (1024 * 1024)

            metrics = {
                'ffmpeg_conversion_time_seconds': round(convert_duration, 3),
                'input_file_size_bytes': input_size_bytes,
                'input_file_size_mb': round(input_size_mb, 2),
                'output_file_size_bytes': output_size_bytes,
                'output_file_size_mb': round(output_size_mb, 2),
                'size_reduction_percent': round((1 - output_size_bytes/input_size_bytes) * 100, 2) if input_size_bytes > 0 else 0
            }
            
            logger.info(f"Conversion complete: {output_name} ({convert_duration:.2f}s, {output_size_mb:.2f} MB)")
            return output_name, metrics
        
        except Exception as e:
            logger.error(f"Ffmpeg conversion failed - {input_file}: {str(e)}")
            raise RuntimeError(f"FFmpeg conversion failed for {input_file}: {str(e)}")

