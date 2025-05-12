# DocuPod™ Video-Podcast Bridge: Design Document

This document provides a technical overview of the design, architecture, and implementation decisions for the DocuPod™ Video-Podcast Bridge.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Database Design](#database-design)
- [Backend Implementation](#backend-implementation)
- [Frontend Implementation](#frontend-implementation)
- [Deployment & Configuration](#deployment--configuration)
- [Design Decisions & Rationale](#design-decisions--rationale)
- [Known Issues & Future Improvements](#known-issues--future-improvements)

---

## Overview

DocuPod™ bridges video and podcast content using a simple, maintainable tech stack. The goal was to minimize custom infrastructure, use pre-existing podcast and video platforms, and provide a seamless, branded user experience.

---

## Architecture

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** Bootstrap, custom CSS, Jinja2 templates, vanilla JavaScript
- **Data Initialization:** CLI tool (`init_db.py`) with YAML sample data
- **Deployment:** Designed for cloud platforms (e.g., Render, GitHub Pages via iframe), with DNS support for custom subdomains

---

## Database Design

**Schema Overview:**

- `videos` table: Stores video metadata (title, YouTube ID, description)
- `podcasts` table: Stores podcast platform, episode ID, and foreign key to video

**Schema (schema.sql):**
DROP TABLE IF EXISTS podcasts;
DROP TABLE IF EXISTS videos;
CREATE TABLE videos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
youtube_id TEXT NOT NULL UNIQUE,
description TEXT
);
CREATE TABLE podcasts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
video_id INTEGER NOT NULL,
platform TEXT NOT NULL,
episode_id TEXT NOT NULL,
FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
);
text

**Rationale:**
- **Normalization:** Avoids data duplication.
- **ON DELETE CASCADE:** Maintains referential integrity.
- **UNIQUE YouTube ID:** Prevents duplicate videos.

---

## Backend Implementation

- **Flask App (`app.py`):**
  - Provides routes for the home page, video detail pages, and error handling.
  - Uses a `Database` helper class for all DB operations, ensuring absolute paths and robust error handling.
  - Passes all data to templates via Jinja2 context.

- **Database Initialization (`init_db.py`):**
  - CLI tool using Click and PyYAML.
  - Supports full reset and sample data loading.
  - Validates YAML structure before insertion.
  - Enforces foreign key constraints.

---

## Frontend Implementation

- **Templates:**
  - `index.html`: Lists all videos, links to video detail pages.
  - `video.html`: Embeds YouTube video, displays podcast links/embeds, branded with logos.
  - `404.html`: Custom error page with navigation.

- **Static Assets:**
  - Custom CSS for branding and accessibility.
  - Logos for Humm Productions, Apple Podcasts, Spotify.

- **JavaScript:**
  - Enables dynamic video switching on the detail page.

- **Accessibility:**
  - Semantic HTML, alt text for images, accessible focus styles.

---

## Deployment & Configuration

- Designed for deployment to cloud platforms (e.g., Render) with environment variable support.
- Uses absolute paths for database and assets for compatibility.
- DNS for custom subdomain (e.g., `app.hummproductions.org`) is pending.

---

## Design Decisions & Rationale

- **Flask & SQLite:** Chosen for simplicity, portability, and ease of setup.
- **Bootstrap:** Ensures responsive design with minimal custom CSS.
- **YAML Sample Data:** Human-readable, easy to edit for demos and development.
- **Minimal Backend:** Leverages YouTube and podcast platforms for hosting and playback, reducing server complexity.
- **Error Handling:** Custom 404 and robust error logging for maintainability.

---

## Known Issues & Future Improvements

- **Read-only:** No user uploads or authentication.
- **Static Platform Config:** Podcast platforms are hardcoded.
- **Scalability:** For large-scale use, migrate to PostgreSQL or another RDBMS.
- **Admin Interface:** Consider adding an admin dashboard for content management.
- **Testing:** Add automated tests (unit/integration) for production readiness.

---
