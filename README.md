# Django Chat Application

A real-time chat application built with Django, Django Channels, WebSockets, and Redis. The application supports user authentication, private messaging, and a user-friendly interface.

## Features

- User authentication (Login, Logout, Register)
- Real-time messaging using WebSockets
- WebSocket integration with Django Channels
- Redis as a message broker
- Chat history persistence using a database
- Responsive UI

## Technologies Used

- **Backend**: Django, Django Channels, Redis, WebSockets
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite / PostgreSQL (configurable)

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python (>= 3.8)
- Redis Server
- Virtualenv (optional but recommended)

### Step 1: Clone the Repository
```bash
$ git clone https://github.com/VardhanVelamkanni/django-chat-app.git
$ cd django-chat-app
```

### Step 2: Create a Virtual Environment
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```bash
$ pip install -r requirements.txt
```

### Step 4: Configure Redis Server
Ensure Redis is running on your system. If not installed, you can install it using:
```bash
$ sudo apt install redis  # On Ubuntu/Debian
$ brew install redis      # On macOS
```
Start Redis server:
```bash
$ redis-server
```

### Step 5: Apply Migrations
```bash
$ python manage.py migrate
```

### Step 6: Create a Superuser (Optional)
```bash
$ python manage.py createsuperuser
```

### Step 7: Run the Server
```bash
$ python manage.py runserver
```

### Step 8: Run the WebSocket Worker
```bash
$ daphne -b 0.0.0.0 -p 8001 chat.asgi:application
```

Now, open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser and start chatting!

## Screenshots
![Screenshot 2025-02-03 223419](https://github.com/user-attachments/assets/6b4de65c-1599-453a-a8e5-7cde4937d838)
![Screenshot 2025-02-03 223527](https://github.com/user-attachments/assets/383e9f4c-9b8d-48bd-82a3-766ef6cd22a2)
![Screenshot 2025-02-03 223709](https://github.com/user-attachments/assets/fdb03454-8ede-4eb4-9cb5-050ba400dd8a)
![Screenshot 2025-02-03 223727](https://github.com/user-attachments/assets/8b5f7df2-4b3f-484d-bffd-b727222328d4)



## Folder Structure
```
chat-app/
|-- chat/                     # Django app for chat functionality
|-- users/                    # Django app for user authentication
|-- templates/chat/           # HTML templates
|-- static/                   # CSS and JavaScript files
|-- db.sqlite3                 # Database file
|-- manage.py                 # Django project management script
|-- asgi.py                   # ASGI entry point for WebSockets
|-- settings.py               # Django project settings
```

## Environment Variables
Create a `.env` file and add the following:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, localhost
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Running with Docker (Optional)
```bash
$ docker-compose up --build
```

## License
MIT License

## Author
Your Name - [GitHub Profile](https://github.com/yourusername)

