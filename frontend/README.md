# Esports Platform Frontend

A simple, modern frontend for the Esports Tournament Platform built with vanilla HTML, CSS, and JavaScript.

## 🚀 Features

- **Dashboard**: Overview of teams, tournaments, and statistics
- **Teams Management**: Create, view, edit, and delete teams
- **Tournaments Management**: Create and manage tournaments with detailed views
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time API Integration**: Connects to Django REST API backend

## 📋 Prerequisites

Before running the frontend, ensure you have:

1. **Backend Running**: The Django backend must be running on `http://localhost:8000`
2. **Web Server**: Use a local web server (Live Server, Python HTTP server, etc.)

## 🛠️ Setup Instructions

### 1. Install Backend Dependencies

First, install the required Python packages including the new CORS package:

```bash
cd esports_platform
pip install -r requirements.txt
```

### 2. Run Database Migrations

```bash
python manage.py migrate
```

### 3. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start the Django Backend

```bash
python manage.py runserver
```

The backend should now be running at `http://localhost:8000`

### 5. Serve the Frontend

You have several options to serve the frontend:

#### Option A: VS Code Live Server (Recommended)
1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html` in the `frontend` folder
3. Select "Open with Live Server"
4. The frontend will open at `http://localhost:5500` or similar

#### Option B: Python HTTP Server
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500` in your browser

#### Option C: Node.js HTTP Server
```bash
cd frontend
npx http-server -p 5500
```

## 📁 Project Structure

```
frontend/
├── index.html          # Dashboard/Home page
├── teams.html          # Teams management page
├── tournaments.html    # Tournaments management page
├── style.css          # All styling (dark theme)
├── app.js             # API client and utilities
└── README.md          # This file
```

## 🎨 Pages

### 1. Dashboard (index.html)
- Statistics cards showing total teams, tournaments, active, and completed tournaments
- Recent tournaments list
- Quick navigation

### 2. Teams (teams.html)
- View all teams in a grid layout
- Search and filter teams by status
- Create new teams
- Edit and delete existing teams

### 3. Tournaments (tournaments.html)
- View all tournaments
- Filter by status (Draft, Registration, Group Stage, Final Stage, Completed, Cancelled)
- Create new tournaments
- View detailed tournament information including groups and matches
- Edit and delete tournaments

## 🔧 Configuration

The API base URL is configured in `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

If your backend runs on a different port, update this variable.

### CORS Configuration

The backend has been configured to allow requests from:
- `http://localhost:5500`
- `http://127.0.0.1:5500`
- `http://localhost:3000`
- `http://127.0.0.1:3000`

If you use a different port, add it to the `CORS_ALLOWED_ORIGINS` list in `esports_platform/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://localhost:YOUR_PORT",
    # Add more as needed
]
```

## 🎯 API Endpoints Used

The frontend interacts with the following API endpoints:

- **Teams**: `/api/teams/teams/`
- **Tournaments**: `/api/tournaments/tournaments/`
- **Groups**: `/api/tournaments/groups/`
- **Matches**: `/api/tournaments/matches/`
- **Standings**: `/api/tournaments/standings/`
- **Final Stages**: `/api/tournaments/final-stages/`
- **Final Matches**: `/api/tournaments/final-matches/`
- **Users**: `/api/accounts/users/`

## 🐛 Troubleshooting

### "Cannot connect to the server" error

**Solution**: Make sure the Django backend is running on `http://localhost:8000`

```bash
python manage.py runserver
```

### CORS errors in browser console

**Solutions**:
1. Verify `django-cors-headers` is installed: `pip install django-cors-headers`
2. Check that your frontend URL is in `CORS_ALLOWED_ORIGINS` in `settings.py`
3. Restart the Django server after making changes

### Frontend not loading properly

**Solutions**:
1. Make sure you're serving the frontend through a web server (not opening the HTML file directly)
2. Check the browser console for JavaScript errors
3. Verify all files (index.html, teams.html, tournaments.html, style.css, app.js) are in the same directory

### "Module not found" errors when creating tournaments

**Note**: When creating tournaments, the frontend currently uses `organizer: 1` as a placeholder. Make sure you have at least one user in the database:

```bash
python manage.py createsuperuser
```

## 🎨 Customization

### Changing Colors

The color scheme is defined using CSS variables in `style.css`. You can customize the theme by modifying these values:

```css
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... and more */
}
```

### Adding New Pages

1. Create a new HTML file (e.g., `matches.html`)
2. Include the same navigation structure
3. Link `style.css` and `app.js`
4. Add your page-specific JavaScript
5. Update the navigation links in all pages

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

The frontend uses modern JavaScript features (async/await, fetch API) which are supported in all modern browsers.

## 🔒 Security Notes

**This is a development setup. For production:**

1. Enable authentication (currently using `IsAuthenticatedOrReadOnly`)
2. Use HTTPS instead of HTTP
3. Restrict CORS to specific production domains
4. Add proper error handling and validation
5. Implement rate limiting
6. Add CSRF token handling for authenticated requests

## 📄 License

This project is part of the Esports Tournament Platform.

## 🤝 Contributing

Feel free to enhance the frontend by:
- Adding more features (player management, match results, etc.)
- Improving the UI/UX
- Adding animations and transitions
- Implementing authentication
- Adding real-time updates with WebSockets

Happy coding! 🎮
