# DocuPod™ Video-Podcast Bridge

DocuPod™ is a lightweight, cross-platform web application that bridges DocuPod™ videos with their associated podcasts, providing a branded, user-friendly interface for browsing, watching, and listening. This project was developed as a CS50 final project.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation & Usage](#installation--usage)
- [Project Structure](#project-structure)
- [Demo Video](#demo-video)
- [Known Issues & Limitations](#known-issues--limitations)
- [Contact](#contact)

---

## Project Overview

DocuPod™ connects video content with related podcasts, leveraging pre-existing services (YouTube, Libsyn, Apple Podcasts, Spotify) and a minimal custom backend. The app is designed for easy deployment and cross-platform compatibility, with a focus on maintainability and a branded user experience.

---

## Features

- **Responsive Home Page:** Browse all available DocuPod™ videos.
- **Video Detail Pages:** Watch embedded YouTube videos and access dynamically generated podcast links/embeds for each platform.
- **Dynamic Video Switching:** Seamless video changes via JavaScript without page reloads.
- **Branding:** Includes Humm Productions, Apple Podcasts, and Spotify logos.
- **Custom 404 Page:** Friendly error page for missing resources.
- **CLI Tool:** Easily initialize/reset the database and load sample data.

---

## Installation & Usage

### 1. Install dependencies

pip install flask click pyyaml
text

### 2. Initialize the database

python init_db.py --reset --sample
text

### 3. Run the app

python app.py
text
- Open [http://localhost:5000](http://localhost:5000) in your browser.

### 4. Deployment

- The app is ready for deployment to a custom subdomain or cloud service. (DNS for the custom subdomain is pending and will be updated here upon resolution.)

---

## Project Structure

/
├── app.py
├── init_db.py
├── sample_data.yaml
├── docupod.db
├── schema.sql
├── static/
│ ├── css/
│ │ └── styles.css
│ └── images/
│ ├── humm_logo.png
│ ├── humm_icon.png
│ ├── apple.png
│ └── spotify.png
├── templates/
│ ├── index.html
│ ├── video.html
│ └── 404.html
├── README.md
└── DESIGN.md
text

---

## Demo Video

A short demo video (≤3 min) will be uploaded to YouTube and linked here before submission.

---

## Known Issues & Limitations

- **Read-only app:** No user uploads or authentication.
- **Static Podcast Platforms:** Podcast platforms are statically configured in code.
- **Scalability:** For larger content libraries, consider migrating from SQLite to a more robust database.

---

## Contact

- **Lee Bechtold**
- Email: Lee@Bechtold4.com
