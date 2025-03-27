# PsychManager

PsychManager is a web application designed to help psychologists efficiently manage their schedules and patient information. This project was developed for my girlfriend, a psychologist, to streamline her workflow by providing an intuitive and organized platform for handling appointments and patient records.

## Features

- **Patient Management**: Add, edit, and delete patient records with essential information.
- **Appointment Scheduling**: Book and manage patient appointments.
- **Agenda Overview**: View upcoming sessions in an organized calendar.
- **Detailed Patient Profiles**: Store session notes and relevant patient details.

## Technologies Used

- **Backend**: Django
- **Frontend**: Django-Bootstrap 5
- **Database**: SQLite (default) or PostgreSQL (Looking for a new)
- **Styling**: Bootstrap 5

## Installation

### Prerequisites
- Python 3.x installed
- Virtual environment (recommended)
- Django installed

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/PsychManager.git
   cd PsychManager
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the development server:
   ```sh
   python manage.py runserver
   ```
6. Access the application at `http://127.0.0.1:8000/`

## Usage
- Register and log in to manage patient records and appointments.
- Navigate through the interface to add, update, or delete patients and schedule sessions.
- Use the agenda to track appointments easily.

## Contributing
Feel free to fork this repository and contribute improvements or new features.

## License
This project is open-source under the MIT License.

---

If you have any suggestions or feedback, feel free to reach out!

