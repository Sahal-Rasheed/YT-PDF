from enum import Enum

from pydantic import BaseModel, HttpUrl, Field, field_validator


class ProcessingStatus(str, Enum):
    """Processing statuses."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Chapter(BaseModel):
    """Video chapter schema."""

    title: str
    start_time: float
    end_time: float


class ConvertRequest(BaseModel):
    """Request schema for YouTube to PDF conversion."""

    url: HttpUrl = Field(
        ...,
        description="YouTube video URL to convert",
        example="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    )

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, v):
        """
        Validate that the URL is a valid YouTube URL.
        """
        url_str = str(v)
        youtube_patterns = [
            "youtube.com/watch",
            "youtu.be/",
            "youtube.com/embed/",
            "youtube.com/v/",
        ]

        if not any(pattern in url_str for pattern in youtube_patterns):
            raise ValueError("URL must be a valid YouTube video URL")

        return v


class VideoInfo(BaseModel):
    """Video metadata schema."""

    id: str | None = None
    title: str | None = None
    description: str | None = None
    duration: int | None = None
    uploader: str | None = None
    upload_date: str | None = None
    view_count: int | None = None
    like_count: int | None = None
    tags: list[str] | None = Field(default_factory=list)
    categories: list[str] | None = Field(default_factory=list)
    thumbnail: str | None = None
    webpage_url: str | None = None
    chapters: list[Chapter] | None = Field(default_factory=list)


class PDFInfo(BaseModel):
    """PDF file information schema."""

    filename: str
    file_size: int
    file_size_mb: float
    created_at: float


class ContentAnalysis(BaseModel):
    """Content analysis result schema."""

    executive_summary: str
    key_concepts: list[str]
    actionable_insights: list[str]
    important_quotes: list[str]
    resources_mentioned: list[str]
    step_by_step_guides: list[str]
    main_takeaways: list[str]
    detailed_summary: str


class ConvertResponse(BaseModel):
    """Response schema for YouTube to PDF conversion."""

    status: ProcessingStatus
    message: str
    video_info: VideoInfo | None = None
    pdf_info: PDFInfo | None = None
    analysis: ContentAnalysis | None = None
    processing_time: float | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "message": "PDF generated successfully",
                "video_info": {
                    "id": "dQw4w9WgXcQ",
                    "title": "Sample Video Title",
                    "duration": 212,
                    "uploader": "Sample Channel",
                },
                "pdf_info": {
                    "filename": "sample_video_notes.pdf",
                    "file_size": 1024000,
                    "file_size_mb": 1.02,
                    "created_at": 1640995200.0,
                },
                "processing_time": 45.5,
            }
        }
