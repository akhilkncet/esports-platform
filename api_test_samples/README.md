# API Test Samples

This folder contains JSON samples for testing all API endpoints using tools like Postman, Thunder Client, or curl.

## 📋 Available Endpoints

### Teams API - `http://localhost:8000/api/teams/teams/`

**GET** - List all teams
```bash
curl http://localhost:8000/api/teams/teams/
```

**POST** - Create a team (use: `01_create_team.json`, `02_create_team2.json`, `03_create_team3.json`)
```bash
curl -X POST http://localhost:8000/api/teams/teams/ \
  -H "Content-Type: application/json" \
  -d @01_create_team.json
```

**PUT** - Update a team (use: `10_update_team.json`)
```bash
curl -X PUT http://localhost:8000/api/teams/teams/1/ \
  -H "Content-Type: application/json" \
  -d @10_update_team.json
```

**DELETE** - Delete a team
```bash
curl -X DELETE http://localhost:8000/api/teams/teams/1/
```

---

### Tournaments API - `http://localhost:8000/api/tournaments/tournaments/`

**GET** - List all tournaments
```bash
curl http://localhost:8000/api/tournaments/tournaments/
```

**POST** - Create a tournament (use: `04_create_tournament.json`, `05_create_tournament2.json`)
```bash
curl -X POST http://localhost:8000/api/tournaments/tournaments/ \
  -H "Content-Type: application/json" \
  -d @04_create_tournament.json
```

**PUT** - Update a tournament (use: `11_update_tournament.json`)
```bash
curl -X PUT http://localhost:8000/api/tournaments/tournaments/1/ \
  -H "Content-Type: application/json" \
  -d @11_update_tournament.json
```

**DELETE** - Delete a tournament
```bash
curl -X DELETE http://localhost:8000/api/tournaments/tournaments/1/
```

---

### Groups API - `http://localhost:8000/api/tournaments/groups/`

**GET** - List all groups
```bash
curl http://localhost:8000/api/tournaments/groups/
```

**POST** - Create a group (use: `06_create_group.json`, `07_create_group2.json`)
```bash
curl -X POST http://localhost:8000/api/tournaments/groups/ \
  -H "Content-Type: application/json" \
  -d @06_create_group.json
```

---

### Matches API - `http://localhost:8000/api/tournaments/matches/`

**GET** - List all matches
```bash
curl http://localhost:8000/api/tournaments/matches/
```

**POST** - Create a match (use: `08_create_match.json`, `09_create_match2.json`)
```bash
curl -X POST http://localhost:8000/api/tournaments/matches/ \
  -H "Content-Type: application/json" \
  -d @08_create_match.json
```

---

## 🧪 Testing with VS Code Thunder Client / Postman

### Thunder Client (VS Code Extension)
1. Install "Thunder Client" extension
2. Click the Thunder Client icon in sidebar
3. Create a new request
4. Set method (GET, POST, PUT, DELETE)
5. Enter URL: `http://localhost:8000/api/teams/teams/`
6. For POST/PUT: Go to "Body" tab → Select "JSON" → Paste content from JSON files
7. Click "Send"

### Postman
1. Open Postman
2. Create new request
3. Set method and URL
4. For POST/PUT: Go to "Body" → Select "raw" → Select "JSON" → Paste content
5. Click "Send"

---

## 📝 Quick Test Workflow

### 1. Create Teams First
```bash
POST http://localhost:8000/api/teams/teams/
Body: 01_create_team.json
Body: 02_create_team2.json
Body: 03_create_team3.json
```

### 2. Create Tournament
```bash
POST http://localhost:8000/api/tournaments/tournaments/
Body: 04_create_tournament.json
```

### 3. Create Groups
```bash
POST http://localhost:8000/api/tournaments/groups/
Body: 06_create_group.json
Body: 07_create_group2.json
```

### 4. Create Matches
```bash
POST http://localhost:8000/api/tournaments/matches/
Body: 08_create_match.json
Body: 09_create_match2.json
```

---

## 🔑 Important Notes

- **organizer** field in tournament JSON should match your user ID (check `/api/accounts/users/`)
- **tournament** field in groups should match existing tournament ID
- **group** field in matches should match existing group ID
- **teams** array in groups should contain valid team IDs
- All IDs start from 1 and increment

---

## 🌐 Access API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

These provide interactive API testing directly in your browser!
