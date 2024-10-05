# NeoOrrery

Live Demo: https://neoorrery-13c972087676.herokuapp.com

Demo Login Information:

- Username: user
- Password: NasaSPACE2024$

---
## 🌍 Project Description


NeoOrrery is a dynamic web-based platform designed to provide real-time tracking, analysis, and 3D visualization of celestial bodies. By integrating NASA's Open APIs, the platform keeps users continuously informed about close approaches of asteroids and other space objects. It features an intuitive and comprehensive dashboard that displays detailed information on registered celestial bodies, key statistics, critical close approaches, and custom 3D models, making space data accessible and visually engaging.

NeoOrrery directly addresses the challenge of providing public access to real-time space data by offering personalized alerts and email notifications tailored to individual user preferences. We've integrated Celery for automating real-time data fetching and alerting, ensuring users always have the most up-to-date information on space events.

This project is crucial because it connects the public with real-time cosmic events, raising awareness about cosmic occurrences and promoting interest in space exploration. By offering an immersive, user-friendly experience, NeoOrrery has the potential to empower researchers, space enthusiasts, and the general public to explore and engage with space data. Its scalable infrastructure lays the foundation for broader educational opportunities, future innovations, and a collaborative approach to real-time space tracking, setting the stage for the next generation of space science engagement.


---

### 🚀 Features Overview

- Dashboard: A detailed dashboard shows real-time statistics on celestial bodies, including planets, comets, asteroids, and potentially hazardous asteroids (PHAs). Data includes the size, distance, and velocity of these bodies.
  
- Real-Time Close Approach Alerts: Users are alerted when a celestial object passes within a certain distance of Earth. By default:
  - Real-Time Close Approaches Distance: 100,000 km
  - Critical Close Approaches Distance: 10,000 km
  Users can also set personalized distances for these alerts based on their preferences.

- Automated Data Updates: NeoOrrery automatically fetches the latest data from NASA's APIs:
  - Data is updated every 6 hours to ensure the latest information about celestial bodies is available.
  - Email alerts are sent to users every 24 hours if a significant close approach occurs within their chosen parameters.

- 3D Visualization: Users can explore the orbits and movement of celestial bodies in a 3D environment, providing an interactive and engaging way to understand their behavior and trajectories.

- User Profiles: Users can create personalized accounts where they can:
  - Set custom distances for close approach alerts.
  - Upload profile pictures.
  - Manage and update personal information.
  - View contributions and points.

- Contribution System & Ranking: Users can contribute blog posts or articles, and earn points based on their contributions.
  - Non-Verified Contributions: Earn 25 points each.
  - Verified Contributions: Earn 50 points each.
  - Points are accumulated, leading to a ranking system where users earn ranks such as "Rookie Explorer" and "Universe Architect."

- CSV Export: Users can download data about celestial bodies, including planets, asteroids, comets, and PHAs, for further analysis. Data can be exported in CSV format.

- Search, Filter, and Sort: The dashboard includes advanced search, filter, and sort functionality to help users find specific celestial bodies based on their size, distance, or name.

- Admin Panel: The app provides an admin panel where administrators can manage user accounts, contributions, and review submitted content.

- Secure Authentication: NeoOrrery offers secure login and logout options, password management, and user authentication using Django's built-in security mechanisms.

Bushra, [10/5/2024 4:51 AM]
- Custom Error Pages: The app includes custom error pages for smooth handling of issues like 404 (page not found) or 500 (server error).

- Responsive Design: The application is fully responsive, providing an optimal experience on mobile, tablet, and desktop devices.

---

## 🌟 Ranking System and Points

NeoOrrery has a ranking system that rewards users based on their contributions. Each time a user submits a blog post or contribution, they earn points, which contribute to their rank.

- Non-Verified Contributions: 25 points per submission
- Verified Contributions: 50 points per submission

As users accumulate points, their rank increases. The ranking system is as follows:

| Points Range       | Rank                   |
|--------------------|------------------------|
| 10,000+            | Universe Architect      |
| 9,500 - 9,999      | Space Voyager           |
| 9,000 - 9,499      | Quantum Pioneer         |
| 8,000 - 8,999      | Nebula Master           |
| 7,000 - 7,999      | Celestial Analyst       |
| 6,000 - 6,999      | Orbital Specialist      |
| 5,000 - 5,999      | Galactic Researcher     |
| 4,000 - 4,999      | Orbit Navigator         |
| 3,000 - 3,999      | Interstellar Scout      |
| 2,000 - 2,999      | Cosmic Observer         |
| 1,000 - 1,999      | Astro Apprentice        |
| 500 - 999          | Stellar Novice          |
| 0 - 499            | Rookie Explorer         |

---

## 📡 Real-Time and Critical Close Approaches

In NeoOrrery, you can subscribe to alerts for close approaches based on the distance from Earth. The distances are set as follows:

- Real-Time Close Approaches Distance: 100,000 KM
- Critical Close Approaches Distance: 10,000 KM

These thresholds allow users to stay informed about potentially dangerous objects and other celestial bodies that come near Earth.

---

## 🛠️ Tools, Languages, and Frameworks Used

### 🖥️ Languages:
- Python
- JavaScript
- HTML
- CSS

### 🧰 Frameworks:
- Django (Backend Framework)
- Celery (Task Queue)
- Redis (Message Broker and Task Results Backend)
- Three.js (3D Visualization Library)

### ⚙️ Tools:
- PostgreSQL / SQLite (Database)
- NGINX (Web Server)
- Gunicorn (WSGI HTTP Server for Django)
- Git (Version Control)
- Celery Beat (Scheduler for Periodic Tasks)
- Docker (Containerization)

---

### ⚙️ Installation Instructions
Follow these steps to set up *NeoOrrery* on your local machine.
#### 1. 📂 Clone the Repository
Clone the project from the GitHub repository:
⁠ git clone https://github.com/prayangshu/neoorrery.git ⁠
Move into the project directory:
⁠ cd neoorrery ⁠
#### 2. 🛠️ Set Up a Virtual Environment (Recommended)
It's recommended to create a virtual environment to manage dependencies.
For Windows:
⁠ python -m venv neoenv ⁠
⁠ neoenv\Scripts\activate ⁠
For macOS/Linux:
⁠ python3 -m venv neoenv ⁠
⁠ source neoenv/bin/activate ⁠
Once activated, you'll see (venv) in your terminal prompt.
#### 3. 📦 Install Dependencies
Install the required Python packages:
⁠ pip install -r requirements.txt ⁠
### 4. 🗄️ Run Migrations
Apply the database migrations to set up the schema:
python manage.py migrate
### 5. 🚀 Start the Development Server
Start the Django development server:
python manage.py runserver
The server will run at `http://127.0.0.1:8000/``` by default.
### 6. 📡 Running Celery Worker
To handle background tasks like sending email notifications, start the Celery worker:
`celery -A NeoOrreryProject worker -l info`
### 7. ⏲️ Running Celery Beat Scheduler
To run periodic tasks (e.g., fetching NASA data every 6 hours), start the Celery beat scheduler:
`celery -A NeoOrreryProject beat -l info`
### 8. 🐳 Docker

NeoOrrery also includes a Docker setup for easier deployment. To run the app using Docker, follow these steps:

Make sure Docker is installed on your machine.
Build the Docker image:
`docker-compose build`
Start the services:
`docker-compose up`

Bushra, [10/5/2024 4:51 AM]
This will start the web server, Redis, and Celery in containers. The app will be accessible at http://localhost:8000/.

### 9. 🌐 Access the Application
Once the server is running, open your browser and visit:
http://127.0.0.1:8000/
Now you can explore NeoOrrery and start monitoring celestial bodies in real-time!


## 🌌 API & Resources Used

- [NASA Open APIs](https://api.nasa.gov): General NASA API platform.
- [Near-Earth Comets - Orbital Elements API](https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements-API/ysqn-vd8v/about_data): Provides data on Near-Earth comets' orbital elements.
- [NASA Near-Earth Object Web Service (NeoWs)](https://api.nasa.gov/neo): A service for querying near-Earth objects tracked by NASA's JPL.
- [Eyes on Asteroids - Home](https://eyes.nasa.gov/apps/asteroids/#/home): Provides visualizations for asteroids and other small bodies tracked by NASA.

---

## 👥 About Team Radiant

NeoOrrery is developed by Team Radiant, a group of passionate creators and developers:

- [Prayangshu Biswas Hritwick](https://github.com/prayangshuu) (Leader & Lead Developer)
- [Kamolesh Gachi](https://github.com/kamoleshgachi) (Concept Designer & Developer, Video Editor)
- [Biplob Hasan Khan](https://github.com/biplobhasankhan) (Front-End Developer)
- [Jannatul Bushra Snigdha](https://github.com/jannat-b) (Researcher, Designer)
- [Sharmin Sultana Lincoln](https://github.com/sharminlincoln) (Data Specialist & Analyst)
- [Abdus Sobhan](https://github.com/sobhanlab) (Co-Researcher)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute to NeoOrrery:

1. Fork the repository.
2. Create a new branch: git checkout -b feature/YourFeature.
3. Commit your changes: git commit -m 'Add your feature'.
4. Push to the branch: git push origin feature/YourFeature.
5. Open a Pull Request.

Please ensure your code follows the existing style and passes all tests before submitting.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🌟 Acknowledgements

Thanks to NASA for providing open APIs that enable real-time space data access.

- [NASA Open APIs](https://api.nasa.gov)
- [Near-Earth Comets - Orbital Elements API](https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements-API/ysqn-vd8v/about_data)
- [NASA Near-Earth Object Web Service (NeoWs)](https://api.nasa.gov/neo)
- [Eyes on Asteroids - Home](https://eyes.nasa.gov/apps/asteroids/#/home)
