# YouTube Downloader (MP3 & MP4)

## Overview
A web application that downloads YouTube videos as MP3 (audio) or MP4 (video) files. Users can paste a YouTube URL, preview video information (title, thumbnail, duration, channel), select output format and quality, and download the file with the video's title as the filename.

## Features
- **URL Input**: Paste button for easy URL insertion and manual input field
- **Video Preview**: Displays video information before conversion including:
  - Video thumbnail
  - Video title
  - Channel name
  - Duration
- **Format Selection**: Choose between MP3 (audio) or MP4 (video) output
- **Quality Selection**: 
  - **MP3 Quality Options:**
    - Normal (192 kbps) - Good quality, smaller file size
    - HD (320 kbps) - High quality, larger file size
  - **MP4 Quality Options:**
    - 360p (Low) - Smaller file size
    - 480p (SD) - Standard definition
    - 720p (HD) - High definition
    - 1080p (Full HD) - Full high definition
- **Automatic Download**: Downloads file with the video's title as filename
- **Clean UI**: Modern, responsive design with gradient background

## Technology Stack
- **Backend**: Python Flask
- **Video Processing**: yt-dlp for downloading and FFmpeg for video/audio extraction
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## Project Structure
```
├── app.py                 # Flask application with routes
├── templates/
│   └── index.html        # Frontend interface
├── static/
│   └── style.css         # Styling
├── downloads/            # Temporary storage for downloaded files
└── replit.md            # This file
```

## How It Works
1. User pastes or enters a YouTube URL
2. Clicks "Generate Info" to fetch video information
3. Video details are displayed (thumbnail, title, channel, duration)
4. User selects desired format (MP3 or MP4)
5. User selects desired quality based on format
6. User clicks "Download" button to convert and download
7. File is downloaded with the video's title as the filename

## Recent Updates
- October 20, 2025: Added format selection (MP3/MP4) with quality options for both formats
- October 20, 2025: Added quality selection feature for MP3 (Normal 192kbps, HD 320kbps)
- October 20, 2025: Initial creation

## Date Created
October 20, 2025
