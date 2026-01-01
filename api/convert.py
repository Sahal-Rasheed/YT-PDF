import time
import logging
from typing import Any
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from core.config import settings
from services.llm import llm_service
from services.pdf import pdf_service
from services.youtube import youtube_service
from schemas.response import StandardResponse
from schemas.convert import (
    PDFInfo,
    VideoInfo,
    ConvertRequest,
    ConvertResponse,
    ContentAnalysis,
    ProcessingStatus,
)

logger = logging.getLogger(__name__)

convert_router = APIRouter()


@convert_router.post(
    "/convert",
    response_model=StandardResponse[ConvertResponse],
    status_code=status.HTTP_200_OK,
    description="Convert a YouTube video to actionable PDF notes with insights and analysis",
)
async def convert_to_pdf(
    request: ConvertRequest, background_tasks: BackgroundTasks
) -> Any:
    """
    Convert YouTube video to actionable PDF notes.
    """
    start_time = time.time()
    audio_file_path = None
    pdf_file_path = None

    try:
        logger.info(f"Starting conversion for URL: {request.url}")

        # validate yt url
        if not youtube_service.validate_youtube_url(str(request.url)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid YouTube URL provided",
            )

        # extract video information
        logger.info("Extracting video metadata...")
        video_info_dict = youtube_service.extract_video_info(str(request.url))
        video_info = VideoInfo(**video_info_dict)

        # download audio
        logger.info("Downloading and processing audio...")
        audio_file_path = youtube_service.download_audio(
            str(request.url), video_info_dict
        )

        # transcribe audio
        logger.info("Transcribing audio using Whisper...")
        transcript = await llm_service.transcribe_audio(audio_file_path)

        if not transcript or len(transcript.strip()) < 50:
            raise ValueError(
                "Transcript is too short or empty. The video might not have clear audio."
            )

        logger.info(f"Transcription completed. Length: {len(transcript)} characters")

        # analyze content
        logger.info("Analyzing content with GPT...")
        analysis_dict = await llm_service.analyze_content(transcript, video_info_dict)
        analysis = ContentAnalysis(**analysis_dict)

        # generate HTML content for PDF
        logger.info("Generating PDF content...")
        html_content = await llm_service.generate_pdf_content(
            analysis_dict, video_info_dict
        )

        # create PDF
        logger.info("Creating PDF document...")
        pdf_file_path = pdf_service.generate_pdf(html_content, video_info_dict)

        # get PDF information
        pdf_info_dict = pdf_service.get_pdf_info(pdf_file_path)
        pdf_info = PDFInfo(**pdf_info_dict)

        processing_time = round(time.time() - start_time, 2)

        convert_response = ConvertResponse(
            status=ProcessingStatus.COMPLETED,
            message="PDF generated successfully",
            video_info=video_info,
            pdf_info=pdf_info,
            analysis=analysis,
            processing_time=processing_time,
        )

        logger.info(f"Conversion completed successfully in {processing_time}s")

        return StandardResponse(
            success=True,
            message="YouTube video converted to PDF successfully",
            data=convert_response,
        )

    except ValueError as ex:
        logger.exception(f"Validation error: {str(ex)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    except Exception as ex:
        logger.exception(f"Unexpected error during conversion: {str(ex)}")

        processing_time = round(time.time() - start_time, 2)

        convert_response = ConvertResponse(
            status=ProcessingStatus.FAILED,
            message=f"Conversion failed: {str(ex)}",
            processing_time=processing_time,
        )

        return StandardResponse(
            success=False,
            message="Failed to convert YouTube video to PDF",
            data=convert_response,
        )

    # finally:
    #     if audio_file_path:
    #         background_tasks.add_task(cleanup_files, audio_file_path, pdf_file_path)


@convert_router.get(
    "/download/{filename}",
    response_class=FileResponse,
    description="Download a generated PDF file by filename",
)
async def download_pdf(filename: str) -> Any:
    """
    Download a generated PDF file.
    """
    try:
        safe_filename = Path(filename).name
        if not safe_filename.endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only PDF files are supported.",
            )

        pdf_path = Path(settings.UPLOAD_DIR) / "pdfs" / safe_filename

        if not pdf_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="PDF file not found"
            )

        logger.info(f"Serving PDF file: {pdf_path}")

        return FileResponse(
            path=str(pdf_path),
            filename=safe_filename,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={safe_filename}",
                "Cache-Control": "no-cache",
            },
        )

    except Exception as ex:
        logger.error(f"Error serving PDF file: {str(ex)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to serve PDF file",
        )
