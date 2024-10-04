# NeoOrrery

**Live Demo:** https://neoorrery-13c972087676.herokuapp.com

Demo Login Information:

- **Username:** user
- **Password:** NasaSPACE2024$

---

**NeoOrrery** is a web-based Django application designed to visualize, monitor, and alert users about Near-Earth Objects (NEOs) such as comets, asteroids, and other celestial bodies. The project leverages NASA's Open APIs to fetch real-time data about celestial bodies and their close approaches to Earth, providing users with both graphical and tabular representations of planetary data and potential hazards.

---

## 🌍 Project Description

**NeoOrrery** is an interactive web application that provides valuable information about various celestial bodies, including planets, comets, asteroids, and Near-Earth Objects (NEOs). By leveraging data from NASA’s open APIs, **NeoOrrery** displays real-time information about the orbits and key characteristics of these objects, offering users a comprehensive view of their behavior in space. One of the primary focuses is on **Potentially Hazardous Asteroids (PHAs)**, which are asteroids that may pass close to Earth and pose a risk of impact.

The platform provides various tools and features for users, including:

- A **dashboard** that offers detailed statistics on celestial objects like size, speed, and distance.
- **Real-time alerts** to notify users when objects approach close to Earth.
- An immersive **3D visualization tool** that allows users to visualize orbits dynamically.

Additionally, users can create personal profiles, manage settings for alerts, and export celestial data for further research.

---

## 🎯 Features

- **Dashboard:** Displays detailed stats on planets, comets, asteroids, and PHAs, including size, speed, and distance.
- **Real-Time Alerts:** Subscribe to email alerts for objects coming close to Earth, with personalized settings.
- **3D Visualization:** Explore celestial objects and their orbits in an interactive 3D view.
- **User Profiles:** Create accounts, upload profile pictures, and manage settings, including alert subscriptions.
- **Email Notifications:** Get real-time email notifications when objects come near Earth.
- **CSV Export:** Export celestial body data as CSV for further analysis.
- **Search, Filter, and Sort:** Easily search for celestial bodies and filter or sort them.
- **Admin Panel:** Manage users and data using Django's admin interface.
- **Automatic Data Updates:** NeoOrrery automatically fetches data from NASA to keep information up to date.
- **Secure Login/Logout:** Use Django's authentication system for login, logout, and profile management.
- **Responsive Design:** Works seamlessly across all devices, including phones, tablets, and desktops.

---

## 🌟 Ranking System and Points

**NeoOrrery** has a ranking system that rewards users based on their contributions. Each time a user submits a blog post or contribution, they earn points, which contribute to their rank.

- **Non-Verified Contributions:** 25 points per submission
- **Verified Contributions:** 50 points per submission

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

In **NeoOrrery**, you can subscribe to alerts for close approaches based on the distance from Earth. The distances are set as follows:

- **Real-Time Close Approaches Distance:** 100,000 KM
- **Critical Close Approaches Distance:** 10,000 KM

These thresholds allow users to stay informed about potentially dangerous objects and other celestial bodies that come near Earth.

---

## 🛠️ Tools, Languages, and Frameworks Used

### 🖥️ Languages:
- **Python**
- **JavaScript**
- **HTML**
- **CSS**

### 🧰 Frameworks:
- **Django** (Backend Framework)
- **Celery** (Task Queue)
- **Redis** (Message Broker and Task Results Backend)
- **Three.js** (3D Visualization Library)

### ⚙️ Tools:
- **PostgreSQL / SQLite** (Database)
- **NGINX** (Web Server)
- **Gunicorn** (WSGI HTTP Server for Django)
- **Git** (Version Control)
- **Celery Beat** (Scheduler for Periodic Tasks)
- **Docker** (Containerization)

---

## 🌌 API & Resources Used

- **[NASA Open APIs](https://api.nasa.gov):** General NASA API platform.
- **[Near-Earth Comets - Orbital Elements API](https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements-API/ysqn-vd8v/about_data):** Provides data on Near-Earth comets' orbital elements.
- **[NASA Near-Earth Object Web Service (NeoWs)](https://api.nasa.gov/neo):** A service for querying near-Earth objects tracked by NASA's JPL.
- **[Eyes on Asteroids - Home](https://eyes.nasa.gov/apps/asteroids/#/home):** Provides visualizations for asteroids and other small bodies tracked by NASA.

---

## 👥 About Team Radiant

**NeoOrrery** is developed by **Team Radiant**, a group of passionate creators and developers:

- **[Prayangshu Biswas Hritwick](https://github.com/prayangshuu)** (Leader & Lead Developer)
- **[Kamolesh Gachi](https://github.com/kamoleshgachi)** (Concept Designer & Developer, Video Editor)
- **[Biplob Hasan Khan](https://github.com/biplobhasankhan)** (Front-End Developer)
- **[Jannatul Bushra Snigdha](https://github.com/)** (Researcher, Designer)
- **[Sharmin Sultana Lincoln](https://github.com/sharminlincoln)** (Data Specialist & Analyst)
- **[Abdus Sobhan](https://github.com/sobhanlab)** (Co-Researcher)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute to **NeoOrrery**:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
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
