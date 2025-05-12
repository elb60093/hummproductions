"""
init_db.py - Enhanced Database Initialization Script

Key Improvements:
1. Absolute path resolution for all file operations
2. Foreign key constraint enforcement
3. Comprehensive data validation
4. Granular error handling with cleanup
5. Production-grade logging
6. Schema existence checks
7. YAML format validation
8. Platform normalization
9. Transaction safety
10. Verbose mode support
"""

import sqlite3
import click
import yaml
import os
import sys
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def validate_video_data(video: Dict[str, Any]) -> bool:
    """Validate video entry structure from YAML"""
    required_fields = {'title', 'youtube_id', 'description'}
    if not all(field in video for field in required_fields):
        logger.error("Missing required video fields")
        return False
    if len(video['youtube_id']) < 5:  # Minimum YouTube ID length
        logger.error(f"Invalid YouTube ID: {video['youtube_id']}")
        return False
    return True

def validate_podcast_data(podcast: Dict[str, Any]) -> bool:
    """Validate podcast entry structure"""
    required_fields = {'platform', 'episode_id'}
    if not all(field in podcast for field in required_fields):
        logger.error("Missing required podcast fields")
        return False
    if not podcast['episode_id']:
        logger.error("Empty episode ID")
        return False
    return True

@click.command()
@click.option('--reset', is_flag=True, help='Recreate database schema from scratch')
@click.option('--sample', is_flag=True, help='Insert sample data from YAML')
@click.option('--verbose', is_flag=True, help='Enable detailed logging')
def init_db(reset: bool, sample: bool, verbose: bool) -> None:
    """
    Robust database initialization workflow with safety checks

    Features:
    - Ensures foreign key constraints
    - Validates data before insertion
    - Maintains transaction integrity
    - Provides detailed error reporting
    """

    # Configure paths using absolute references
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'docupod.db')
    schema_path = os.path.join(base_dir, 'schema.sql')
    sample_path = os.path.join(base_dir, 'sample_data.yaml')

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Configuration:")
        logger.debug(f"Database path: {db_path}")
        logger.debug(f"Schema path: {schema_path}")
        logger.debug(f"Sample path: {sample_path}")

    conn = None  # Initialize for finally block safety
    try:
        # Establish connection with foreign key support
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        cur = conn.cursor()

        # --- Schema Management ---
        if reset:
            logger.info("Resetting database schema...")
            if not os.path.exists(schema_path):
                raise FileNotFoundError(f"Schema file missing: {schema_path}")

            with open(schema_path) as f:
                conn.executescript(f.read())
            logger.debug("Schema reset complete")
        else:
            # Check for existing tables
            cur.execute("""SELECT name FROM sqlite_master
                        WHERE type='table' AND name='videos'""")
            if not cur.fetchone():
                logger.info("Creating initial schema...")
                with open(schema_path) as f:
                    conn.executescript(f.read())

        # --- Sample Data Insertion ---
        if sample:
            logger.info("Loading sample data...")
            if not os.path.exists(sample_path):
                raise FileNotFoundError(f"Sample data missing: {sample_path}")

            # Validate YAML structure
            try:
                with open(sample_path) as f:
                    data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML format: {e}") from None

            if 'videos' not in data or not isinstance(data['videos'], list):
                raise ValueError("Invalid sample data structure")

            # Transaction block for data insertion
            inserted_videos = 0
            inserted_podcasts = 0

            for video in data['videos']:
                if not validate_video_data(video):
                    raise ValueError(f"Invalid video: {video.get('title')}")

                # Insert video
                cur.execute("""
                    INSERT INTO videos (title, youtube_id, description)
                    VALUES (?, ?, ?)
                """, (
                    video['title'],
                    video['youtube_id'],
                    video['description']
                ))
                video_id = cur.lastrowid
                inserted_videos += 1

                # Insert podcasts
                for podcast in video.get('podcasts', []):
                    if not validate_podcast_data(podcast):
                        raise ValueError(f"Invalid podcast in video {video_id}")

                    # Normalize platform name
                    platform = podcast['platform'].lower()

                    cur.execute("""
                        INSERT INTO podcasts (video_id, platform, episode_id)
                        VALUES (?, ?, ?)
                    """, (
                        video_id,
                        platform,
                        podcast['episode_id']
                    ))
                    inserted_podcasts += 1

            logger.info(f"Inserted {inserted_videos} videos and {inserted_podcasts} podcasts")

        # Final commit
        conn.commit()
        logger.info("Database initialization completed successfully")

    except (sqlite3.Error, FileNotFoundError, ValueError) as e:
        logger.error(f"Initialization failed: {str(e)}")
        if conn:
            conn.rollback()
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            logger.debug("Database connection closed")

if __name__ == '__main__':
    init_db()
