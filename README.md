# Weather Blog Platform

A platform where users can view, like, and comment on weather-related blogs, with features like secure login, role-based access (RBA), and content management for bloggers.

## Features

- **User Authentication & Authorization**: 
  - Secure login and registration system.
  - Role-based access, ensuring proper access levels for users and bloggers.
  
- **Blog Management for Bloggers**:
  - Bloggers can create, edit, and delete their own blogs.
  - User-friendly content management system for easy blog updates.

- **Interactive Features**:
  - Users can like and comment on blogs, fostering community interaction and engagement.

## Technologies Used

- Python
- Django
- SQLite (Database)
- HTML/CSS for frontend
- JavaScript (for interactive features)
  
## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/weather-blog-platform.git

2. Navigate to the project directory:

    cd weather-blog-platform

3. Create a virtual environment and activate it:

    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install dependencies:

    pip install -r requirements.txt

5. Run migrations:
    python manage.py migrate

6. Run the development server:
    python manage.py runserver