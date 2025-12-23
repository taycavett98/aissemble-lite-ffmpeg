"""
Docstring for aissemble-lite-ffmpeg.backend.tests.performance.baseline_test

process test videos/audio files through endpoints: `audio/process` and `/transcribe` collected end-2-end metrics
including speeds for the WAV conversion with FFMPEG, S3 upload time, and transcription time
"""
# imports
from typing import Any
from pathlib import Path

# configuration set up paths for api url, video directory and result/summary destination files


def process_file(file_path: Path) -> dict[str, Any]:
    """Process single file through audio processing endpoint"""
    pass

def transcribe_file(s3_uri: str)-> dict[str, Any]:
    """Transcribe file using transcription endpoint"""
    pass

def run_pipeline(file_path: str)-> dict[str, Any]:
    """Run full pipeline for isngle file"""
    # start clock

    # get file information

    # process file

    # transcribe file

    # end clock

    # gather results

    pass

def save_results(result: dict[str, Any])-> None:
    """Write results to jsonl file"""
    # open file path
    # write results w json dump
    pass

def generate_summary(results: list[dict[str, Any]])->None:
    """Generate summary from all results jsonl"""
    pass

def main():
    # iterate over files in /test_files

    # pass in one file at a time to run_pipeline()

    # read all jsonl files and call generate summary passing the list of jsonl files

    # print results/write file
    pass


if __name__ == "__main__":
    main()