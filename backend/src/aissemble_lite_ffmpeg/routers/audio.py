""" Audio processing router for file upload and processing """

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os
import tempfile

from ..preprocessing.input_handler import InputHandler

router = APIRouter(prefix="/audio", tags=["audio"])

class PerformanceMetrics(BaseModel):
    """Performance metrics for audio processing."""
    total_processing_time_seconds: float
    input_metadata: dict
    ffmpeg_conversion_time_seconds: float
    s3_upload_time_seconds: float
    s3_upload_speed_mbps: float
    input_file_size_mb: float
    output_file_size_mb: float
    size_reduction_percent: float

class AudioProcessResponse(BaseModel):
    """Response model for audio processing."""
    s3_uri: str
    original_filename: str
    message: str = "Audio Processed Successfully"
    metrics: PerformanceMetrics

@router.post("/process", response_model=AudioProcessResponse)
async def process_audio(file: UploadFile = File(...)) -> AudioProcessResponse:
    """
    Upload and process audio/video files 

    Converts to WAV format and uploads to s3. 

    Args:

    Returns:
        s3 URI
    """
    # save file temporarily so we can send it across network
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        handler = InputHandler()
        uri, metrics = handler.process_input(tmp_file_path, file.filename)

        return AudioProcessResponse(
            s3_uri=uri, 
            original_filename=file.filename,
            metrics=PerformanceMetrics(**metrics)
        )
    
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)