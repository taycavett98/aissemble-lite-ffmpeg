# Transcription Pipeline
end to end pipeline for processing audio/video files and transcribing them using AWS transcribe

## Architecture
2 main stages in the pipeline:
1. audio processing - `/audio/process`: converts video/audio files into standard WAV files, uploads to s3 bucket and returns s3_uri
example response:
```bash
{
  "s3_uri": "s3://aissemble-transcribe/input/20251223-124027_file_converted.wav",
  "original_filename": "video.mp4",
  "message": "Audio Processed Successfully",
  "metrics": {
    "total_processing_time_seconds": 183.683,
    "ffmpeg_conversion_time_seconds": 0.423,
    "s3_upload_time_seconds": 183.26,
    "s3_upload_speed_mbps": 0.19,
    "input_file_size_mb": 146.25,
    "output_file_size_mb": 34.71,
    "size_reduction_percent": 76.27
  }
}
```
2. transcription - `/transcribe`: uses AWS transcribe to generate transcripts from s3_uri 
example input:
```bash
{
  "s3_uris": [
    "s3://aissemble-transcribe/input/20251223-124027_file_converted.wav"
  ]
}
```

example output:
```bash
{
  "total_files": 1,
  "successful": 1,
  "failed": 0,
  "results": [
    {
      "s3_uri": "s3://aissemble-transcribe/input/20251223-124027_file_converted.wav",
      "success": true,
      "s3_output_uri": "s3://aissemble-transcribe/output/file_transcription.json",
      "error": null
    }
  ]
}
```

## Metrics
`/audio/process` endpoint returns the following metrics:
- total_processing_time_seconds : end to end time from upload to s3_uri response
- ffmpeg_conversion_time_seconds: time spent converting file to WAV format
- s3_upload_time_seconds : time spent uploading WAV file to s3 bucket
- input_file_size_mb : size of original uploaded file
- output_file_size_mb : size of converted WAV file
- size_reduction_percent : reduction in size after conversion 

## project goals
- quick MVP/prototype to satisfy a customer in 3 weeks
### key components
1. aws deployable
2. integrate with an existing team , so end goal is to pass off to them
3. inputs/outputs for me in this notebook to prove concept and be able to pass off to teammate working on transcription
    - inputs: audio or video file, start with 15-30 mins worth of content now, but eventually we want hour long (if possible)
    - outputs: whatever the transcription accepts, this i believe is raw audio data like byte encoded
    - processing: thinking we will use ffmpeg for processing. i know we can grab metadata. i know we can chunk up files.

## steps
1. create input handler : accept file path or valid format (like .mp3, .mp4, etc); handle both types
2. build ffmpeg audio extractor - extract audio from video, do preprocessing here. lesson learned from previous project was to standardize audio inputs like decrease
    background noises and I think there was one other standardization we applied to all audio files to improve quality
3. stub out a function that would be able to upload audio content to S3 and return a URI so we can pass it directly to aws transcribe
4. put pieces together in a main() and test it: input -> preprocess -> upload -> output


### what does AWS transcribe need?
- s3 uri format: `s3://bucket-name/path/to/file.wav`
- supported format, lets use wav
- recommended specs: 16kHz ssample rate, mono channel, 16-bit PCM
- file permissions? set to all read access?

# TESTING 

## Audio Processing Endpoint

### Start the Server

From the `backend` directory:

```bash
uv run aissemble_lite_ffmpeg serve
```
### Navigate to SwaggerUI -> `localhost:8080/docs`
use UI to upload a file to `/auio/process` endpoint

## needs env configuration for setting up s3 bucket