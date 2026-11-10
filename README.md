🚌 College Bus Management System


  **A Smart QR Code-Based College Bus Tracking and Management System**
A web-based application designed to replace manual college bus entry records with a digital system using QR code scanning.

---

💡 1. Project Idea – How It Started

One day, while passing through my college, I noticed a person manually writing down the details of buses arriving at and leaving the college.

I started thinking:

Why should a person do this work manually when a machine can handle it?

That simple observation gave me the idea to develop the College Bus Management System.

Instead of maintaining bus records in a notebook, I wanted to create a system where a camera could scan a bus QR code, identify the bus, and record its arrival or departure automatically.

My main idea was to replace manual record writing with a simple, smart, and digital solution.

🎯 2. Project Objective

The main objective of this project is to reduce manual work in college bus management.

This system helps to:

- Replace manual bus entry records with digital records.
- Identify buses using QR codes.
- Record bus arrival and departure details.
- Maintain complete bus information.
- Store scan history with date and time.
- Make bus records accessible through a shared cloud database.

✨ 3. Key Features

🚌 A. Bus Management

- Add new bus details.
- Edit existing bus information.
- Store bus number and registration number.
- Maintain driver name and phone number.
- Store bus route and starting place.
- Maintain route stops.
- Store bus capacity.
- Manage scheduled arrival and departure timings.

📷 B. QR Code Scanning

- Each bus has a QR code containing its bus number.
- Scan the QR code using a camera.
- Automatically identify the bus using its bus number.
- No need to manually enter bus details during scanning.
- Makes bus identification faster and easier.

🚍 C. Arrival and Departure Tracking

- Record bus arrival at the college.
- Record bus departure from the college.
- Select the event type: Arrival or Departure.
- Automatically record the date and time of each scan.
- Maintain separate records for arrival and departure events.

📋 D. Bus Scan History

- View previously scanned bus records.
- Display complete bus details.
- View arrival and departure events.
- Check the date and time of each scan.
- Maintain a digital history of bus movements.
- Access previously recorded information whenever needed.

☁️ E. Shared Cloud Database

- Uses Supabase as the cloud database.
- Stores bus information and scan records online.
- Allows multiple users to access the same updated records.
- Helps avoid depending on a single computer's local database.
- Keeps bus details and scan history in one shared database.

🎨 F. Simple User Interface

- Easy-to-use web interface.
- Organized bus information.
- Simple navigation.
- Clear display of bus details.
- Easy access to bus scan history.

⚙️ 4. How the System Works

The system follows a simple process:

1. The administrator adds bus details to the application.
2. Each bus is identified using its QR code.
3. The camera scans the bus QR code.
4. The system reads the bus number stored in the QR code.
5. The user selects the event type: Arrival or Departure.
6. The system records the bus event with its date and time.
7. The scan information is saved in the database.
8. Users can view the updated bus details and scan history.

🛠️ 5. Technologies Used

Technology| Purpose
Python| Main programming language
Flask| Backend web framework
HTML| Web page structure
CSS| Website design and styling
JavaScript| Frontend functionality, where used
SQLite| Original local database
Supabase (PostgreSQL)| Cloud database
QR Code| Bus identification
OpenCV| Camera-based QR scanning
Vercel| Web application hosting and deployment

🔄 6. Database Migration & Development Journey

Phase 1: Initial Development – SQLite

During the initial development, I used SQLite to store bus details and scan history locally on my computer.

- Created a local database.
- Stored bus information.
- Recorded bus arrival and departure details.
- Tested the application and QR scanning locally.

Phase 2: Cloud Database – Supabase

Later, I wanted to make the system accessible from different devices and allow multiple users to view the same updated information.

To achieve this, I migrated the database from SQLite to Supabase (PostgreSQL).

- Created a cloud database using Supabase.
- Connected the Flask application to Supabase.
- Moved the application towards shared online data storage.
- Made bus records accessible through the internet.

Phase 3: Website Deployment – Vercel

To make the application accessible online, I chose Vercel for hosting.

- Prepared the Flask application for deployment.
- Connected the project repository.
- Configured environment variables for database connectivity.
- Worked on deploying the application online.

Final Technology Architecture

- Frontend: HTML, CSS and JavaScript (where used)
- Backend: Python and Flask
- Original Database: SQLite
- Current Cloud Database: Supabase PostgreSQL
- Hosting Platform: Vercel
- Scanning: QR code and camera

🚀 7. Project Benefits

- Reduces manual record writing.
- Saves time and human effort.
- Makes bus identification easier.
- Maintains digital records of bus movements.
- Makes bus information easier to access.
- Allows shared access to records through the cloud.
- Reduces paperwork and manual record maintenance.
- Provides a simple and organized way to manage college buses.

🔮 8. Future Improvements

The following features can be added in future versions:

- Automatic identification of arrival and departure events.
- Student bus attendance tracking.
- SMS or notification alerts.
- Daily and monthly bus reports.
- Advanced dashboard with bus statistics.
- User login and role-based access.
- More detailed bus tracking and reporting.

📂 9. Project Structure

The project is organized using a Flask application structure with separate folders for templates and static files.

college-bus-management/
│
├── app.py
├── scanner.py
├── requirements.txt
│
├── templates/
│   └── HTML templates
│
├── static/
│   ├── CSS files
│   └── Other static files
│
└── .env

Note: The ".env" file contains confidential environment variables. It should not be uploaded to GitHub.

💻 10. How to Run the Project Locally

Step 1: Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

Step 2: Open the Project Folder

cd college-bus-management

Step 3: Install Required Packages

py -m pip install -r requirements.txt

Step 4: Configure Environment Variables

Create a ".env" file and add your Supabase connection details:

SUPABASE_URL=YOUR_SUPABASE_PROJECT_URL
SUPABASE_KEY=YOUR_SUPABASE_SECRET_KEY
FLASK_SECRET_KEY=YOUR_RANDOM_SECRET_KEY

Use your own credentials. Never publish secret keys on GitHub.

Step 5: Run the Flask Application

py app.py

Step 6: Run the QR Scanner

For arrival scanning:

py scanner.py Arrival

For departure scanning:

py scanner.py Departure

Note: The camera scanner requires a suitable local camera and a running application/API endpoint configured in the scanner.

👨‍💻 11. Developed By

Nageswara Sarma

This project was developed based on a simple problem I personally observed in my college.

I wanted to turn that everyday observation into a practical technical solution using Python, Flask, QR code scanning, and cloud database technology.

Small Observation. Simple Idea. Smart Solution. 🚌
