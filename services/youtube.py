import os
import re
import logging
from typing import Any
from pathlib import Path

import yt_dlp
from pydub import AudioSegment

from core.config import settings
from utils.helpers import sanitize_filename

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for handling YouTube video processing and audio extraction."""

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR) / "youtube"
        self.upload_dir.mkdir(exist_ok=True)

    def extract_video_info(self, url: str) -> dict[str, Any]:
        """
        Extract video metadata without downloading.
        """
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # extract chapters if available
                chapters = []
                if info.get("chapters"):
                    chapters = [
                        {
                            "title": ch.get("title", "Untitled Chapter"),
                            "start_time": ch.get("start_time", 0),
                            "end_time": ch.get("end_time", 0),
                        }
                        for ch in info.get("chapters", [])
                    ]

                video_info = {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "duration": info.get("duration"),
                    "uploader": info.get("uploader"),
                    "upload_date": info.get("upload_date"),
                    "view_count": info.get("view_count"),
                    "like_count": info.get("like_count"),
                    "tags": info.get("tags", []),
                    "categories": info.get("categories", []),
                    "thumbnail": info.get("thumbnail"),
                    "webpage_url": info.get("webpage_url"),
                    "chapters": chapters,
                }

                if (
                    video_info["duration"]
                    and video_info["duration"] > settings.MAX_VIDEO_DURATION
                ):
                    raise ValueError(
                        f"Video duration ({video_info['duration']}s) exceeds maximum allowed duration ({settings.MAX_VIDEO_DURATION}s)"
                    )

                logger.info(f"Successfully extracted info for video \n\n: {video_info}")
                return video_info

        except Exception as ex:
            logger.exception(f"Error extracting video info: {str(ex)}")
            raise ValueError(f"Failed to extract video information: {str(ex)}")

    def download_audio(self, url: str, video_info: dict[str, Any] | None = None) -> str:
        """
        Download audio from YouTube video and convert to MP3.
        """
        try:
            if not video_info:
                video_info = self.extract_video_info(url)

            title = sanitize_filename(video_info["title"])
            video_id = video_info["id"]
            audio_filename = f"{title}_{video_id}"

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": str(self.upload_dir / audio_filename),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "quiet": True,
                "no_warnings": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_path = self.upload_dir / f"{audio_filename}.mp3"

            if not mp3_path.exists():
                for ext in ["mp3", "webm", "m4a", "wav"]:
                    potential_path = self.upload_dir / f"{audio_filename}.{ext}"
                    if potential_path.exists():
                        if ext != "mp3":
                            audio = AudioSegment.from_file(str(potential_path))
                            audio.export(str(mp3_path), format="mp3")
                            potential_path.unlink()
                        else:
                            mp3_path = potential_path
                        break
                else:
                    raise FileNotFoundError("Downloaded audio file not found")

            file_size = mp3_path.stat().st_size
            if file_size > settings.MAX_FILE_SIZE:
                mp3_path.unlink()
                raise ValueError(f"Audio file too large: {file_size} bytes")

            logger.info(f"Successfully downloaded audio: {mp3_path}")
            return str(mp3_path)

        except Exception as ex:
            logger.exception(f"Error downloading audio: {str(ex)}")
            raise ValueError(f"Failed to download audio: {str(ex)}")

    def cleanup_file(self, file_path: str) -> None:
        """
        Clean up downloaded files.
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as ex:
            logger.warning(f"Failed to cleanup file {file_path}: {str(ex)}")

    def validate_youtube_url(self, url: str) -> bool:
        """
        Validate if the URL is a valid YouTube URL.

        Possible patterns:
        - https://www.youtube.com/watch?v=LDB4uaJ87e0
        - https://youtu.be/LDB4uaJ87e0?feature=shared
        - https://www.youtube.com/embed/LDB4uaJ87e0?si=Z-c99q_ZXh2jT5RQ
        """
        youtube_patterns = [
            r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+",
            r"(?:https?://)?(?:www\.)?youtu\.be/[\w-]+",
            r"(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+",
        ]

        return any(re.match(pattern, url) for pattern in youtube_patterns)


youtube_service = YouTubeService()
