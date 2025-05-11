# hummproductions
Humm Productions DocuPod™ Video-Podcast Bridge App

DocuPod™ is a lightweight, cross-platform web application that bridges DocuPod™ videos with their associated podcasts. The app provides an elegant, branded interface for users to browse available DocuPod™ videos, watch them, and access related podcast episodes on various platforms.

Features
•	Responsive, accessible web interface using Flask, Bootstrap, and custom CSS.
•	Video listing page (index.html) displaying all available DocuPod™ videos.
•	Individual video detail pages (video.html) with embedded YouTube player and associated podcast links/embeds (Libsyn, Apple, Spotify, RSS).
•	Dynamic video switching on the detail page (via JavaScript, no page reload).
•	Logos for Humm Productions, Apple Podcasts, and Spotify for clear branding and user recognition.
•	SQLite database backend for videos and podcasts.
•	Easy database initialization with CLI tool (init_db.py) and YAML sample data.
•	Custom 404 error page.
•	Clean project structure with separated static assets and templates.
•	Ready for deployment to GitHub Pages and custom subdomain with iframe integration.
Setup & Usage
1. Install dependencies
bash
pip install flask click pyyaml
2. Initialize the database
bash
python init_db.py --reset --sample
•	This will create docupod.db and populate it with sample data (sample_data.yaml).
3. Run the app locally
bash
flask run
or
bash
python app.py
4. Access the app
•	Open your browser to http://localhost:5000
Deployment
•	To deploy on GitHub Pages, build a static version of the site or use a service like Render or Heroku for Flask apps.
•	To use a custom subdomain (e.g., app.hummproductions.org), point your DNS to the deployed app and embed it with an <iframe> on your main site.
•	All static assets (images, CSS) are in the static/ directory for easy serving.
Project Structure
text
/project-root
  /static
    /images
      humm_logo.png
      humm_icon.png
      apple_podcast.png
      spotify.png
    /css
      styles.css
  /templates
    index.html
    video.html
    404.html
  app.py
  database.py (optional, if separated)
  init_db.py
  schema.sql
  sample_data.yaml
  README.md
  DESIGN.md
Known Issues / To-Do
•	Add more sample data for broader testing.
•	Finalize deployment and update documentation with public URLs.
•	Optional: Add user authentication or search/filter features.
Demo Video
[Insert YouTube link here after recording screencast]
