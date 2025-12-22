import ffmpeg
import logging

from pathlib import Path

logger = logging.getLogger(__name__)

class FfmpegHandler():
    def __init__(self):
        logger.info('initializing ffmpeg object')

    def convert_to_wav(self, input_file):
        """This function will accept a file and convert it into a wav file and return a new file"""

        try:
            input_path = Path(input_file)
            output_name = f'{input_path.stem}_converted.wav'
            ffmpeg.input(input_file).output(
                output_name,
                ar=16000, # 16kHz sample rate
                ac=1, # mono channel 
                acodec='pcm_s16le' # 16-bit PCM
            ).run(overwrite_output=True)

            return output_name
        except Exception as e:
            logger.error(f"Ffmpeg conversion failed - {input_file}: {str(e)}")
            raise RuntimeError(f"FFmpeg conversion failed for {input_file}: {str(e)}")

