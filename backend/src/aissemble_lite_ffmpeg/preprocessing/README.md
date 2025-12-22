# Transcription Protoype


1. use ffmpeg to extract audio to pass to a transcription function

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
3. chunking? if it makes sense, but if they aren't looking to stream does it make sense?
4. stub out a function that would be able to upload audio content to S3 and return a URI so we can pass it directly to aws transcribe
5. put pieces together in a main() and test it: input -> preprocess -> upload -> output


### what does AWS transcribe need?
- s3 uri format: `s3://bucket-name/path/to/file.wav`
- supported format, lets use wav
- recommended specs: 16kHz ssample rate, mono channel, 16-bit PCM
- file permissions? set to all read access?