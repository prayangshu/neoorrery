**NeoOrrery** is a web-based Django application designed to visualize, monitor, and alert users about Near-Earth Objects (NEOs) such as comets, asteroids, and other celestial bodies. The project leverages NASA's Open APIs to fetch real-time data about celestial bodies and their close approaches to Earth, providing users with both graphical and tabular representations of planetary data and potential hazards.

---

### 🌍 Project Description

**NeoOrrery** is an interactive web application designed to provide users with valuable information about various celestial bodies, including planets, comets, asteroids, and Near-Earth Objects (NEOs) that might come close to Earth. By leveraging data from NASA’s open APIs, **NeoOrrery** displays real-time information about the orbits and key characteristics of these objects, offering a comprehensive view of their behavior in space. The central goal of **NeoOrrery** is to create an easy-to-use platform where users can explore and track objects in space that could pose potential threats to Earth or be of scientific interest. For example, one of the key categories of objects tracked by the application is Potentially Hazardous Asteroids (PHAs), which are asteroids that could pass very close to Earth, raising the possibility of future impacts.

The application provides users with a range of tools to interact with this data. At the heart of **NeoOrrery** is a dashboard that presents detailed statistics on planets, comets, asteroids, and PHAs. Users can easily access information such as the size, distance, and speed of these celestial objects, as well as more advanced details regarding their orbits and recent activity. To make this data even more engaging, the app offers a **real-time close approach alert system**, which notifies users when any object comes within a critical distance of Earth. Users who choose to subscribe to these alerts can receive real-time notifications via email, ensuring they stay informed about space objects that might pose risks or warrant attention.

One of the most exciting features of **NeoOrrery** is the **3D visualization tool**. This tool provides users with an immersive way to visualize the orbits of planets, comets, and asteroids in space, allowing them to see the dynamic movement of these bodies and how they interact with one another over time. This visual representation helps users gain a better understanding of the structure and behavior of our solar system, making it both educational and engaging.

In addition to real-time data and visualizations, **NeoOrrery** allows users to create personal accounts. This enables them to manage their profiles, control whether or not they receive email alerts, and even export data about celestial bodies to CSV format for further analysis. The export feature is particularly useful for researchers, students, and space enthusiasts who want to dive deeper into the data for personal study or external projects.

**NeoOrrery** is built using Django, a robust web framework known for its scalability and flexibility. To handle the app's background tasks, such as checking for new close approaches and sending alert notifications, **NeoOrrery** uses Celery, which works alongside Redis as the message broker. This setup ensures that tasks are processed efficiently, without any delay in delivering critical updates. The data itself is sourced directly from NASA’s official APIs, which guarantees that the information presented is both accurate and up-to-date, making **NeoOrrery** a reliable resource for anyone interested in celestial events and near-Earth space activity.

---

### 🎯 Features

- **Dashboard:** The dashboard shows details about planets, comets, asteroids, and potentially hazardous asteroids (PHAs). You can see their size, speed, and distance from Earth.
- **Real-Time Alerts:** NeoOrrery sends you email alerts when a space object comes close to Earth. You can choose to opt-in for these alerts.
- **3D Visualization:** See planets, comets, and asteroids in a 3D view. You can explore their orbits and how they move in space.
- **User Profiles:** Create an account, upload a profile picture, and manage your settings, including alerts.
- **Email Notifications:** Get email notifications when objects come near Earth. You’ll receive detailed information like the distance and speed of the object.
- **CSV Export:** Download celestial body data as a CSV file. This is useful for further analysis or research.
- **Search, Filter, and Sort:** Find celestial bodies easily using search, filters, and sorting options on the dashboard.
- **Admin Panel:** Manage users and data with the built-in admin panel.
- **Error Handling:** Custom error pages for smooth handling of issues like 404 (page not found) or 500 (server error).
- **Automatic Updates:** NeoOrrery automatically fetches the latest data from NASA’s APIs to keep information up-to-date.
- **Secure Login and Logout:** Log in and out safely, update your account details, and manage your password.
- **Responsive Design:** NeoOrrery works smoothly on all devices, including phones, tablets, and desktops.

---

### 🛠️ Tools, Languages, and Frameworks Used

#### 🖥️ Languages:
- 🐍 Python
- 🟨 JavaScript
- 🌐 HTML
- 🎨 CSS

#### 🧰 Frameworks:
- 🌐 Django (Backend Framework)
- 📨 Celery (Task Queue)
- 🌀 Redis (Message Broker and Task Results Backend)
- 🌍 Three.js (3D Visualization Library)

#### ⚙️ Tools:
- 🛢️ PostgreSQL / SQLite (Database)
- 🖥️ NGINX (Web Server)
- 🚀 Gunicorn (WSGI HTTP Server for Django)
- 🔀 Git (Version Control)
- ⏰ Celery Beat (Scheduler for Periodic Tasks)

---

### 🌌 API & Resources Used

- 🚀 **[NASA Open APIs](https://api.nasa.gov):** General NASA API platform.
- ☄️ **[Near-Earth Comets - Orbital Elements API | NASA Open Data Portal](https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements-API/ysqn-vd8v/about_data):** Provides data on Near-Earth comets' orbital elements.
- 🌠 **[NASA Near-Earth Object Web Service (NeoWs)](https://api.nasa.gov/neo):** A service for querying near-Earth objects tracked by NASA's JPL.
- 🛰️ **[Eyes on Asteroids - Home](https://eyes.nasa.gov/apps/asteroids/#/home):** Provides visualizations for asteroids and other small bodies tracked by NASA.

---

### ⚙️ Installation Instructions

Follow these steps to set up **NeoOrrery** on your local machine.

#### 1. 📂 Clone the Repository

Clone the project from the GitHub repository:

`git clone https://github.com/prayangshu/neoorrery.git`

Move into the project directory:

`cd neoorrery`

#### 2. 🛠️ Set Up a Virtual Environment (Recommended)

It's recommended to create a virtual environment to manage dependencies.

For Windows:

`python -m venv neoenv`
`neoenv\Scripts\activate`

For macOS/Linux:


`python3 -m venv neoenv`
`source neoenv/bin/activate`

Once activated, you'll see (venv) in your terminal prompt.

#### 3. 📦 Install Dependencies

Install the required Python packages:

`pip install -r requirements.txt`

### 4. 🗄️ Run Migrations

Apply the database migrations to set up the schema:

`python manage.py migrate`

### 5. 🚀 Start the Development Server

Start the Django development server:

`python manage.py runserver`

The server will run at ```http://127.0.0.1:8000/``` by default.

### 6. 📡 Running Celery Worker

To handle background tasks like sending email notifications, start the Celery worker:

`celery -A NeoOrreryProject worker -l info`

### 7. ⏲️ Running Celery Beat Scheduler

To run periodic tasks (e.g., fetching NASA data every 6 hours), start the Celery beat scheduler:

`celery -A NeoOrreryProject beat -l info`

### 8. 🐳 Docker (Not Set Up Yet)

Docker is not currently configured. If you plan to use Docker in the future, set it up and update this section accordingly.

### 9. 🌐 Access the Application

Once the server is running, open your browser and visit:

`http://127.0.0.1:8000/`

Now you can explore **NeoOrrery** and start monitoring celestial bodies in real-time!

---

## 👥 About Team Radiant

**NeoOrrery** is developed by a passionate team of creators and developers known as **Team Radiant**. Each member brings unique skills and expertise to the project:

- **[Prayangshu Biswas Hritwick](https://github.com/prayangshuu)** **(Leader & Lead Developer)**
- **[Kamolesh Gachi](https://github.com/kamoleshgachi)** **(Concept Designer & Developer, Video Editor)** 
- [Biplob Hasan Khan](https://github.com/biplobhasankhan) **(Front-End Developer)**
- **[Jannatul Bushra Snigdha](https://github.com/)** **(Researcher, Designer)**
- **[Sharmin Sultana Lincoln](https://github.com/sharminlincoln)** **(Data Specialist & Analyst)**
- **[Abdus Sobhan](https://github.com/sobhanlab)** **(Co-Researcher)**

---

## 🤝 Contributing

We welcome contributions from the community! If you're interested in contributing to **NeoOrrery**, feel free to open an issue or submit a pull request. Whether it’s fixing bugs, improving documentation, or adding new features, all contributions are appreciated.

To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Please ensure your code adheres to the existing style and passes all tests before submitting.

---

## 📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software under the terms of the license. See the [LICENSE](LICENSE) file for more details.

---

## 🌟 Acknowledgements

Special thanks to NASA for providing open APIs that allow access to real-time space data and make projects like **NeoOrrery** possible.

Resources used in this project include:
- [NASA Open APIs](https://api.nasa.gov)
- [Near-Earth Comets - Orbital Elements API](https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements-API/ysqn-vd8v/about_data)
- [NASA Near-Earth Object Web Service (NeoWs)](https://api.nasa.gov/neo)
- [Eyes on Asteroids - Home](https://eyes.nasa.gov/apps/asteroids/#/home)
