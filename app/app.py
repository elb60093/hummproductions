"""
DocuPod Video-Podcast Bridge - Flask Application

This module initializes the Flask app, configures routes, and handles database operations.
"""

from flask import Flask, render_template, abort, g
import sqlite3
from typing import List, Tuple, Optional

# Initialize Flask application
app = Flask(__name__)

# Configuration for podcast platforms
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


class Database:
    """Database handler for SQLite operations"""

    def __init__(self, db_path: str = 'docupod.db'):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Get a new database connection"""
        return sqlite3.connect(self.db_path)

    def query_videos(self) -> List[Tuple]:
        """
        Retrieve all videos from database

        Returns:
            List of video tuples (id, title)
        """
        with self.get_connection() as conn:
            return conn.execute('SELECT id, title FROM videos').fetchall()

    def query_video_details(self, video_id: int) -> Optional[Tuple]:
        """
        Retrieve details for a specific video

        Args:
            video_id: ID of the video to retrieve

        Returns:
            Video details tuple or None if not found
        """
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM videos WHERE id = ?',
                (video_id,)
            ).fetchone()

    def query_podcasts(self, video_id: int) -> List[Tuple]:
        """
        Retrieve associated podcasts for a video

        Args:
            video_id: ID of the video to retrieve podcasts for

        Returns:
            List of podcast tuples (platform, episode_id)
        """
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT platform, episode_id FROM podcasts WHERE video_id = ?',
                (video_id,)
            ).fetchall()


@app.route('/')
def index():
    """
    Home page endpoint

    Renders:
        Template with list of available videos
    """
    db = Database()
    try:
        videos = db.query_videos()
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {str(e)}")
        abort(500)

    return render_template('index.html', videos=videos)


@app.route('/video/<int:video_id>')
def video(video_id: int):
    """
    Video detail page endpoint

    Args:
        video_id: ID of the video to
"""
