Freelance Platform
This is a full-stack freelance platform built with a Django REST Framework backend and a React/Vite frontend. The platform allows users to create accounts, log in, browse projects, and interact with orders.
Prerequisites
Before running the project, ensure you have the following installed:

Python (3.8 or higher)
Node.js (16.x or higher)
npm (8.x or higher)
Git (for cloning the repository)
A code editor like VS Code or PyCharm

Project Structure

Backend: Located in the root directory (e.g., Freelance_site/). Uses Django and Django REST Framework.
Frontend: Located in the client/ directory. Uses React with Vite.

Setup Instructions
1. Clone the Repository
Clone the project to your local machine:
git clone https://github.com/your-username/freelance-platform.git
cd freelance-platform

(Replace https://github.com/your-username/freelance-platform.git with the actual repository URL if available.)
2. Backend Setup (Django)

Navigate to the backend directory (if not already in the root):
cd Freelance_site


Create a virtual environment:
python -m venv .venv


Activate the virtual environment:

On Windows:.venv\Scripts\activate


On macOS/Linux:source .venv/bin/activate




Install backend dependencies:
pip install django djangorestframework django-cors-headers


Apply database migrations:
python manage.py makemigrations
python manage.py migrate


Create a superuser (optional, for admin access):
python manage.py createsuperuser


Run the backend server:
python manage.py runserver

The backend will be available at http://localhost:8000.


3. Frontend Setup (React/Vite)

Navigate to the frontend directory:
cd client


Install frontend dependencies:Due to a known dependency conflict with infinite-react-carousel, use the --legacy-peer-deps flag:
npm install --legacy-peer-deps

Note: If you encounter issues with infinite-react-carousel, consider replacing it with react-slick:
npm uninstall infinite-react-carousel
npm install react-slick slick-carousel


Run the frontend development server:
npm run dev

The frontend will be available at http://localhost:5173.


4. Configuration
Backend Configuration
Ensure the following settings are in Freelance_site/settings.py to handle CORS and media files:
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    ...
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

CORS_ALLOW_CREDENTIALS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

Add media URL to urls.py:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Frontend Configuration
Ensure API requests include the correct backend URL. Check client/src/utils/newRequest.js:
import axios from 'axios';

const newRequest = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  withCredentials: true,
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`,
  },
});

export default newRequest;

5. Running the Application

Start the backend:
cd Freelance_site
.venv\Scripts\activate  # On Windows; use `source .venv/bin/activate` on macOS/Linux
python manage.py runserver


Start the frontend:Open a new terminal, navigate to the frontend directory, and run:
cd client
npm run dev


Access the application:

Frontend: Open http://localhost:5173 in your browser.
Backend API: Test endpoints like http://localhost:8000/api/v1/projects/ in a browser or Postman.
Admin panel: Access http://localhost:8000/admin/ with superuser credentials.



6. Common Issues and Fixes

CORS Errors:If you see CORS-related errors, double-check CORS_ALLOWED_ORIGINS and CORS_ALLOW_CREDENTIALS in settings.py. Ensure the backend is running before the frontend.

APPEND_SLASH Error:If you get a Django error about URLs not ending with a slash, ensure API requests include a trailing slash (e.g., /api/v1/projects/). Alternatively, set APPEND_SLASH=False in settings.py (not recommended).

Dependency Conflicts:If npm install fails due to infinite-react-carousel, use:
npm install --legacy-peer-deps

Or replace with react-slick as described above.

TypeError: data.map is not a function:Ensure the backend returns an array for /api/v1/projects/. Check the frontend code in client/src/pages/orders/Orders.jsx for proper data handling:
{Array.isArray(data) && data.length > 0 ? (
  // Map over data
) : (
  <div>No projects available</div>
)}



7. Building for Production

Build the frontend:
cd client
npm run build

This creates a dist/ folder with production-ready files.

Serve the backend in production:Use a WSGI server like gunicorn:
pip install gunicorn
gunicorn Freelance_site.wsgi


Serve static and media files:Configure a web server like Nginx to handle static and media files. Collect static files:
python manage.py collectstatic



8. Additional Notes

Authentication: The app uses JWT for authentication. Ensure the backend endpoints (/api/v1/auth/login/, /api/v1/auth/register/) are working.
Media Files: Upload images via the admin panel or API to test project images.
Testing: Test API endpoints with Postman or curl to verify data format.

For further assistance, refer to the Django Documentation, Vite Documentation, or React Query Documentation.
