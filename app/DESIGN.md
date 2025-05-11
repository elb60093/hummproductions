Overview
The DocuPod™ app is designed for simplicity, portability, and easy maintenance. The stack is intentionally lightweight (Flask, SQLite, Bootstrap, vanilla JS) to minimize infrastructure and maximize compatibility with platforms like GitHub Pages.
Key Design Decisions
•	Flask for backend: Simple routing, easy templating, and Python ecosystem compatibility.
•	SQLite for storage: No server required, easy to reset and populate for demos or small-scale use.
•	Click CLI for DB management: Makes initialization and sample data loading repeatable and scriptable.
•	Jinja2 templating: Keeps logic out of HTML, supports easy expansion.
•	PLATFORM_CONFIG dictionary: Centralizes podcast platform logic, making it easy to add new platforms.
•	Database class/module: Encapsulates all database logic for maintainability and testability.
•	Custom CSS: Ensures strong branding, accessibility, and responsive design.
•	JavaScript for dynamic video switching: Enhances user experience without extra server requests.
Database Schema
•	videos: id, title, youtube_id, description
•	podcasts: id, video_id (FK), platform, episode_id
Data Flow
•	User visits / → Flask queries videos table → renders index.html
•	User clicks a video → Flask queries videos and podcasts → renders video.html with all data and platform config
•	User can switch videos dynamically on the detail page via JS (no reload)
•	Podcast links/embeds are generated based on PLATFORM_CONFIG and data
Error Handling & Security
•	All SQL queries use parameters to prevent injection.
•	404 errors are handled for missing videos (custom 404 page).
•	No user authentication or input forms (read-only app).
Extensibility
•	New platforms: Add to PLATFORM_CONFIG and update sample data.
•	More videos/podcasts: Add to YAML and re-run init script.
•	New features: Can add search, filtering, or user accounts if needed.
Deployment Considerations
•	Static assets and templates are organized for easy deployment.
•	All paths are relative for compatibility with GitHub Pages/static hosting.
•	Subdomain and iframe integration planned for embedding in main site.
Development & Testing Steps
1.	Planned and designed project structure and features.
2.	Created database schema and sample data.
3.	Developed database initialization script with Click and PyYAML.
4.	Built backend with Flask, separating database logic into a class for maintainability.
5.	Developed and branded frontend templates with Bootstrap and custom CSS.
6.	Added Apple Podcasts and Spotify logos to podcast links.
7.	Created a custom 404 error page.
8.	Tested locally for functionality, accessibility, and responsiveness.
9.	Ready for deployment to GitHub Pages and subdomain integration.
Next Steps
•	Complete deployment to GitHub Pages and custom subdomain.
•	Update documentation with deployment URLs and iframe instructions.
•	Record and upload demo screencast.
