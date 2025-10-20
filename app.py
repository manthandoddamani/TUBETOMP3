from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import re
from datetime import datetime

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.strip()
    return filename[:200]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            duration_seconds = info.get('duration', 0)
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            
            video_info = {
                'title': info.get('title', 'Unknown'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': f"{minutes}:{seconds:02d}",
                'channel': info.get('uploader', 'Unknown'),
                'url': url
            }
            
            return jsonify(video_info)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        format_type = data.get('format', 'mp3')
        quality = data.get('quality', '192')
        
        if not url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
        
        # Get sanitized title first
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get('title', 'video'))
        
        # Use sanitized title in the output template
        output_path = os.path.join(DOWNLOAD_FOLDER, f'{title}.%(ext)s')
        
        if format_type == 'mp3':
            # Validate MP3 quality parameter
            if quality not in ['192', '320']:
                quality = '192'
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
            }
            
            file_extension = 'mp3'
            mimetype = 'audio/mpeg'
            
        elif format_type == 'mp4':
            # Validate MP4 quality parameter
            if quality not in ['360', '480', '720', '1080']:
                quality = '720'
            
            # Format string for video quality
            if quality == '360':
                format_str = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
            elif quality == '480':
                format_str = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            elif quality == '720':
                format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif quality == '1080':
                format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            else:
                format_str = 'bestvideo+bestaudio/best'
            
            ydl_opts = {
                'format': format_str,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',
            }
            
            file_extension = 'mp4'
            mimetype = 'video/mp4'
        else:
            return jsonify({'error': 'Invalid format. Use mp3 or mp4'}), 400
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        filename = f"{title}.{file_extension}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        # Check if file exists, if not try to find any file with the extension
        if not os.path.exists(filepath):
            # Look for the most recently created file with the right extension
            files = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(f'.{file_extension}')]
            if files:
                # Get the most recent file
                files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
                filepath = os.path.join(DOWNLOAD_FOLDER, files[0])
                filename = files[0]
            else:
                return jsonify({'error': 'File not found after conversion'}), 500
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype=mimetype
            )
        else:
            return jsonify({'error': 'File not found after conversion'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_mp3', methods=['POST'])
def download_mp3():
    # Redirect to new download endpoint for backward compatibility
    data = request.get_json()
    data['format'] = 'mp3'
    request._cached_json = data
    return download()

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        for filename in os.listdir(DOWNLOAD_FOLDER):
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
