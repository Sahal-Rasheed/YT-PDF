# YT-PDF

FastAPI backend service that converts YouTube videos into actionable PDF notes with AI-powered insights and analysis.

## 📸 Screenshots
![YT-PDF Demo](/uploads/sample/yt-pdf-demo.jpeg)

*Example PDF generated from a YouTube video. [View full sample →](/uploads/sample/yt-pdf-demo.pdf)*

## 🚀 Features

- **YouTube Video Processing**: Extract metadata and download high-quality audio from YouTube videos
- **AI-Powered Transcription**: Use OpenAI Whisper for accurate speech-to-text conversion
- **Content Analysis**: Generate actionable insights, key concepts, and takeaways using OpenAI
- **Professional PDF Generation**: Create beautifully formatted PDF documents with structured content

## 🛠 Tech Stack

- **Backend**: FastAPI (Python 3.12+)
- **AI Services**: OpenAI Whisper & GPT-4
- **PDF Generation**: WeasyPrint with professional styling
- **Video Processing**: yt-dlp for YouTube content extraction
- **Audio Processing**: pydub for audio format conversion

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key
- FFmpeg (for audio processing)
- [UV](https://github.com/astral-sh/uv) (recommended)

## 🛠️ Installation

1. **Clone the repository**

2. **Install dependencies**

   ```bash
   # Include optional dependencies for development
   uv sync --all-extras

   # OR

   # Exclude optional dependencies
   uv sync
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Add your OpenAI API key and other configurations in the .env file
   ```

## 🚀 Running the Application

1. **Development mode**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Production mode**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Access the API**
   - API Documentation: /api/v1/docs
   - OpenAPI Schema: /api/v1/openapi.json
