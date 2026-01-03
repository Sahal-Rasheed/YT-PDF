import json
import logging
from typing import Any
from openai import OpenAI

from core.config import settings
from constants.llm import (
    ANALYSIS_SYSTEM_PROMPT,
    ANALYSIS_USER_PROMPT,
    PDF_SYSTEM_PROMPT,
    PDF_USER_PROMPT,
)

logger = logging.getLogger(__name__)


class LLMService:
    """Service for handling OpenAI API interactions."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using OpenAI Whisper.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=settings.WHISPER_MODEL,
                    file=audio_file,
                    response_format="text",
                )

            logger.info(f"Successfully transcribed audio file: {audio_file_path}")
            logger.info(f"Transcript \n\n: {transcript}")
            return transcript

        except Exception as ex:
            logger.exception(f"Error transcribing audio: {str(ex)}")
            raise ValueError(f"Failed to transcribe audio: {str(ex)}")

    async def analyze_content(
        self, transcript: str, video_info: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Analyze transcript and generate actionable insights.
        """
        try:
            user_prompt = self.build_analysis_prompt(video_info, transcript)

            response = self.client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            analysis_text = response.choices[0].message.content

            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                analysis = self._parse_text_analysis(analysis_text)

            logger.info("Successfully analyzed content with GPT")
            logger.info(f"Analysis JSON \n\n: {json.dumps(analysis, indent=4)}")
            return analysis

        except Exception as ex:
            logger.exception(f"Error analyzing content: {str(ex)}")
            raise ValueError(f"Failed to analyze content: {str(ex)}")

    def _parse_text_analysis(self, text: str) -> dict[str, Any]:
        """
        Fallback method to parse text-based analysis into structured format.
        """
        return {
            "executive_summary": "Analysis completed successfully. Please refer to the detailed content below.",
            "key_concepts": [
                "Content analysis",
                "Video insights",
                "Learning materials",
            ],
            "actionable_insights": [
                "Review the transcript for key information",
                "Apply insights from the video content",
            ],
            "important_quotes": [],
            "resources_mentioned": [],
            "step_by_step_guides": [],
            "main_takeaways": [
                "Video content has been analyzed",
                "Transcript provides valuable information",
                "Content can be used for learning purposes",
            ],
            "detailed_summary": text,
        }

    async def generate_pdf_content(
        self, analysis: dict[str, Any], video_info: dict[str, Any]
    ) -> str:
        """
        Generate HTML content for PDF creation.
        """
        try:
            user_prompt = self.build_pdf_prompt(analysis, video_info)

            response = self.client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": PDF_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
            )

            html_content = response.choices[0].message.content

            html_content = self._clean_markdown_code_blocks(html_content)

            logger.info("Successfully generated PDF content")
            return html_content

        except Exception as ex:
            logger.exception(f"Error generating PDF content: {str(ex)}")
            return self._generate_fallback_html(analysis, video_info)

    def _format_duration(self, seconds: int) -> str:
        """
        Format duration from seconds to readable format.
        """
        if not seconds:
            return "Unknown"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def _clean_markdown_code_blocks(self, content: str) -> str:
        """
        Remove markdown code block markers from content.
        """
        import re

        # remove ```html, ``` etc. at the start
        content = re.sub(r"^```[\w]*\n?", "", content, flags=re.MULTILINE)

        # remove closing ``` at the end
        content = re.sub(r"\n?```$", "", content, flags=re.MULTILINE)

        # remove any standalone ``` markers
        content = content.replace("```", "")

        return content.strip()

    def _generate_fallback_html(
        self, analysis: dict[str, Any], video_info: dict[str, Any]
    ) -> str:
        """
        Generate fallback HTML content if GPT generation fails.
        """
        return f"""
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
            .title {{ color: #333; font-size: 28px; margin-bottom: 10px; }}
            .meta {{ color: #666; font-size: 14px; }}
            .section {{ margin-bottom: 30px; }}
            .section h2 {{ color: #333; border-left: 4px solid #007acc; padding-left: 15px; }}
            .section h3 {{ color: #555; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 5px; }}
            .summary {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        </style>

        <div class="header">
            <h1 class="title">{video_info.get("title", "Video Analysis")}</h1>
            <div class="meta">
                <p>Duration: {self._format_duration(video_info.get("duration", 0))} |
                   Uploader: {video_info.get("uploader", "Unknown")}</p>
            </div>
        </div>

        <div class="summary">
            <h2>Executive Summary</h2>
            <p>{analysis.get("executive_summary", "Comprehensive analysis of video content.")}</p>
        </div>

        <div class="section">
            <h2>Main Takeaways</h2>
            <ul>
                {"".join(f"<li>{takeaway}</li>" for takeaway in analysis.get("main_takeaways", []))}
            </ul>
        </div>

        <div class="section">
            <h2>Key Concepts</h2>
            <ul>
                {"".join(f"<li>{concept}</li>" for concept in analysis.get("key_concepts", []))}
            </ul>
        </div>

        <div class="section">
            <h2>Actionable Insights</h2>
            <ul>
                {"".join(f"<li>{insight}</li>" for insight in analysis.get("actionable_insights", []))}
            </ul>
        </div>

        <div class="section">
            <h2>Detailed Summary</h2>
            <p>{analysis.get("detailed_summary", "Detailed analysis not available.")}</p>
        </div>
        """

    def build_analysis_prompt(self, video_info: dict[str, Any], transcript: str) -> str:
        """
        Build analysis prompt for the LLM.
        """
        return ANALYSIS_USER_PROMPT.format(
            title=video_info.get("title", "N/A"),
            duration=video_info.get("duration", "N/A"),
            uploader=video_info.get("uploader", "N/A"),
            description=video_info.get("description", "N/A")[:500],
            transcript=transcript,
        )

    def build_pdf_prompt(
        self, analysis: dict[str, Any], video_info: dict[str, Any]
    ) -> str:
        """
        Build PDF prompt for the LLM.
        """
        # Format chapters section if available
        chapters_section = ""
        chapters = video_info.get("chapters", [])
        if chapters and len(chapters) > 0:
            chapters_section = "\nVideo Chapters:"
            for i, chapter in enumerate(chapters, 1):
                start_time = self._format_timestamp(chapter.get("start_time", 0))
                end_time = self._format_timestamp(chapter.get("end_time", 0))
                title = chapter.get("title", f"Chapter {i}")
                chapters_section += f"\n  {i}. {title} ({start_time} - {end_time})"

        return PDF_USER_PROMPT.format(
            title=video_info.get("title", "N/A"),
            duration=video_info.get("duration", "N/A"),
            uploader=video_info.get("uploader", "N/A"),
            upload_date=video_info.get("upload_date", "N/A"),
            chapters_section=chapters_section,
            analysis=analysis,
        )

    def _format_timestamp(self, seconds: float) -> str:
        """
        Format timestamp from seconds to HH:MM:SS or MM:SS.
        """
        if not seconds:
            return "00:00"

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


llm_service = LLMService()
