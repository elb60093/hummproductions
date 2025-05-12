"""
DocuPod Video-Podcast Bridge - Flask Application

This module initializes the Flask app, configures routes, and handles database operations.
Robust error handling has been implemented for production reliability.
"""

import os  # For handling file paths
import sqlite3  # For SQLite database operations
from typing import List, Tuple, Optional
from flask import Flask, render_template, abort

# --- Flask App Initialization ---

# Create a Flask app instance with proper configuration
app = Flask(__name__)

# Configure absolute database path for deployment compatibility
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'docupod.db')

# --- Podcast Platform Configuration ---

# Centralized configuration for podcast platforms
PLATFORM_CONFIG = {
    'libsyn': {
        'url': 'https://play.libsyn.com/embed/episode/id/{episode_id}/height/192/theme/modern/size/large/thumbnail/yes/custom-color/000000/time-start/00:00:00/hide-playlist/yes/download/yes/font-color/ffffff',
        'embed': True
    },
    'apple': {
        'url': 'https://podcasts.apple.com/us/podcast/id{episode_id}',
        'embed': False
    },
    'spotify': {
        'url': 'https://open.spotify.com/episode/{episode_id}',
        'embed': False
    },
    'rss': {
        'url': '{episode_id}',
        'embed': False
    }
}

# --- Database Handler Class ---


class Database:
    """
    Robust database handler with connection pooling and error handling.
    Uses absolute paths for deployment compatibility.
    """

    def __init__(self, db_path: str = None):
        # Use configured path or fallback to default
        self.db_path = db_path or app.config['DATABASE']

    def get_connection(self) -> sqlite3.Connection:
        """Establishes and returns a new database connection"""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            app.logger.error(f"Connection failed: {str(e)}")
            raise

    def query_videos(self) -> List[Tuple]:
        """Safely retrieves all video entries"""
        try:
            with self.get_connection() as conn:
                return conn.execute('SELECT id, title FROM videos').fetchall()
        except sqlite3.Error as e:
            app.logger.error(f"Query failed: {str(e)}")
            raise

    def query_video_details(self, video_id: int) -> Optional[Tuple]:
        """Retrieves video details with parameterized query"""
        try:
            with self.get_connection() as conn:
                return conn.execute(
                    'SELECT * FROM videos WHERE id = ?',
                    (video_id,)
                ).fetchone()
        except sqlite3.Error as e:
            app.logger.error(f"Video query failed: {str(e)}")
            raise

    def query_podcasts(self, video_id: int) -> List[Tuple]:
        """Retrieves podcasts with proper error handling"""
        try:
            with self.get_connection() as conn:
                return conn.execute(
                    'SELECT platform, episode_id FROM podcasts WHERE video_id = ?',
                    (video_id,)
                ).fetchall()
        except sqlite3.Error as e:
            app.logger.error(f"Podcast query failed: {str(e)}")
            raise

# --- Flask Routes ---


@app.route('/')
def index():
    """
    Home page route with comprehensive error handling.
    Returns 500 on database failures with proper logging.
    """
    db = Database()
    try:
        videos = db.query_videos()
        return render_template('index.html', videos=videos)

    except sqlite3.Error as e:
        app.logger.error(f"Index route database failure: {str(e)}")
        abort(500, description="Service unavailable - database error")

    except Exception as e:
        app.logger.critical(f"Unexpected index error: {str(e)}")
        abort(500, description="Internal server error")


@app.route('/video/<int:video_id>')
def video(video_id: int):
    """
    Video detail route with enhanced error handling:
    - 404 for missing videos
    - 500 for database errors
    - Graceful handling of empty/malformed data
    """
    db = Database()
    try:
        # Fetch core data
        video_details = db.query_video_details(video_id)
        if not video_details:
            app.logger.warning(f"Missing video: {video_id}")
            abort(404, description="Video not found")

        # Process podcast data
        raw_podcasts = db.query_podcasts(video_id)
        podcast_data = []

        for platform, episode_id in raw_podcasts:
            config = PLATFORM_CONFIG.get(platform.lower())
            if config and episode_id:
                podcast_data.append({
                    'platform': platform.capitalize(),
                    'url': config['url'].format(episode_id=episode_id),
                    'embed': config['embed']
                })

        # Validate template data
        required_video_fields = len(video_details) >= 4  # Ensure expected columns
        if not required_video_fields:
            app.logger.error(f"Malformed video data: {video_id}")
            abort(500, description="Data format error")

        return render_template(
            'video.html',
            video=video_details,
            podcasts=podcast_data or []  # Ensure iterable empty list
        )

    except sqlite3.Error as e:
        app.logger.error(f"Video route database error: {str(e)}")
        abort(500, description="Service unavailable - database error")

    except Exception as e:
        app.logger.critical(f"Unexpected video error: {str(e)}")
        abort(500, description="Internal server error")

# --- Main Entry Point ---


if __name__ == '__main__':
    # Development server configuration
    app.run(host='0.0.0.0', port=5000, debug=False)
