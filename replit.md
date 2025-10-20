# YouTube to MP3 Converter

## Overview
A web application that converts YouTube videos to MP3 files. Users can paste a YouTube URL, preview video information (title, thumbnail, duration, channel), select audio quality, and download the audio as an MP3 file with the video's title as the filename.

## Features
- **URL Input**: Paste button for easy URL insertion and manual input field
- **Video Preview**: Displays video information before conversion including:
  - Video thumbnail
  - Video title
  - Channel name
  - Duration
- **Quality Selection**: Choose between two audio quality options:
  - Normal (192 kbps) - Good quality, smaller file size
  - HD (320 kbps) - High quality, larger file size
- **MP3 Conversion**: Converts YouTube videos to MP3 format with selected quality
- **Automatic Download**: Downloads MP3 file with the video's title as filename
- **Clean UI**: Modern, responsive design with gradient background

## Technology Stack
- **Backend**: Python Flask
- **Video Processing**: yt-dlp for downloading and FFmpeg for audio extraction
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## Project Structure
```
├── app.py                 # Flask application with routes
├── templates/
│   └── index.html        # Frontend interface
├── static/
│   └── style.css         # Styling
├── downloads/            # Temporary storage for MP3 files
└── replit.md            # This file
```

## How It Works
1. User pastes or enters a YouTube URL
2. Clicks "Generate Info" to fetch video information
3. Video details are displayed (thumbnail, title, channel, duration)
4. User selects desired audio quality (Normal or HD)
5. User clicks "Download MP3" to convert and download
6. MP3 file is downloaded with the video's title as the filename

## Recent Updates
- October 20, 2025: Added quality selection feature (Normal 192kbps, HD 320kbps)

## Date Created
October 20, 2025
