import re
import logging


logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe filesystem usage.
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_")
    return sanitized[:100]


def cleanup_files(audio_file_path: str = None, pdf_file_path: str = None) -> None:
    """
    Background task to cleanup temporary files.
    """
    from services.pdf import pdf_service
    from services.youtube import youtube_service

    try:
        if audio_file_path:
            youtube_service.cleanup_file(audio_file_path)

        if pdf_file_path:
            pdf_service.cleanup_pdf(pdf_file_path)

    except Exception as ex:
        logger.warning(f"Error during file cleanup: {str(ex)}")
