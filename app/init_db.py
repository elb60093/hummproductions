"""
init_db.py: Initialize or reset the DocuPod database and optionally insert sample data.

Usage:
    python init_db.py --reset --sample

Options:
    --reset   Drop and recreate tables using schema.sql
    --sample  Insert sample data from sample_data.yaml

This script is intended for local development and testing. It helps ensure the database schema is up to date
and optionally populates the database with example data for demonstration or testing purposes.
"""

import sqlite3
import click
import yaml  # pip install pyyaml
import os
import sys


@click.command()
@click.option('--reset', is_flag=True, help='Drop existing tables and recreate schema.')
@click.option('--sample', is_flag=True, help='Insert sample data from YAML file.')
def init_db(reset, sample):
    """
    Initialize database with optional reset and sample data.

    Args:
        reset (bool): If True, drop and recreate tables using schema.sql.
        sample (bool): If True, insert sample data from sample_data.yaml.
    """
    db_path = 'docupod.db'
    # Build absolute paths to schema and sample data files
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    sample_path = os.path.join(os.path.dirname(__file__), 'sample_data.yaml')

    try:
        # Connect to the SQLite database (creates file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # If --reset flag is used, drop and recreate all tables
        if reset:
            print("Resetting database...")
            try:
                with open(schema_path) as f:
                    conn.executescript(f.read())
            except FileNotFoundError:
                print(f"Error: {schema_path} not found.")
                sys.exit(1)

        # Always ensure tables exist by running schema.sql
        try:
            with open(schema_path) as f:
                conn.executescript(f.read())
        except FileNotFoundError:
            print(f"Error: {schema_path} not found.")
            sys.exit(1)

        # If --sample flag is used, insert sample data from YAML
        if sample:
            print("Inserting sample data...")
            try:
                with open(sample_path) as f:
                    data = yaml.safe_load(f)
            except FileNotFoundError:
                print(f"Error: {sample_path} not found.")
                sys.exit(1)

            # Iterate over each video entry in the YAML file
            for video in data['videos']:
                # Insert video record into videos table
                cur.execute('''
                    INSERT INTO videos (title, youtube_id, description)
                    VALUES (?, ?, ?)
                ''', (video['title'], video['youtube_id'], video['description']))
                video_id = cur.lastrowid  # Get the auto-generated video ID

                # Insert associated podcasts for this video
                for podcast in video.get('podcasts', []):
                    cur.execute('''
                        INSERT INTO podcasts (video_id, platform, episode_id)
                        VALUES (?, ?, ?)
                    ''', (video_id, podcast['platform'], podcast['episode_id']))

        # Commit all changes to the database
        conn.commit()
        print("Database initialized successfully!")

    except Exception as e:
        # Roll back any changes if an error occurs
        conn.rollback()
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Always close the database connection
        conn.close()


if __name__ == '__main__':
    init_db()
