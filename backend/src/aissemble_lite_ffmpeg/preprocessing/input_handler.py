import os
from pathlib import Path
from .ffmpeg_handler import FfmpegHandler
from .s3_handler import S3Handler

ACCEPTABLE_TYPES = {'.mp3', '.mp4', '.wav', '.m4a', '.flac', '.avi'}  # Use set for O(1) lookup

class InputHandler():
    def __init__(self):
        self.ffmpeg_handler = FfmpegHandler()
        self.s3_handler = S3Handler()


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
        output = self.ffmpeg_handler.convert_to_wav(input_file_path)
        
        return output


    def process_input(self, input: str):
        """This function ensures the file is in .wav format and gets a uri from the s3
            bucket so that we can pass a uri to the aws transcribe function.

            FFmpegHandler class is used to convert the audio as well as standardize the
            audio input for the highest quality. 
        
        """
        # check if input extension is in acceptable types
        self._check_file_extension(input)
        wav_filepath = self._ensure_wav(input)
        s3_uri = self.s3_handler.upload_file(wav_filepath=wav_filepath)

        if not s3_uri:
            raise RuntimeError(f"Failed to upload {wav_filepath} to S3")

        return s3_uri


# # usage
# def main():

#     input_path = "/Users/sallyecavett/Downloads/aiSSEMBLE Daily Standup-20251219_110209-Meeting Recording.mp4"

#     input_handler = InputHandler()

#     file_uri = input_handler.process_input(input_path)

#     if file_uri is not None:
#         print(f'got the file uri!: {file_uri}')
#     else:
#         print('failed somewhere...')

# if __name__ == "__main__":
#     main()