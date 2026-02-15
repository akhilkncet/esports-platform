# Esports Tournament Platform - Complete API Testing Guide

**DETAILED STEP-BY-STEP GUIDE FOR SWAGGER UI**

This guide provides exact copy-paste content for every API call. Follow each step sequentially.

---

## Initial Setup

### A. Start the Development Server

1. Open terminal in project directory
2. Run:
```bash
python manage.py runserver
```
3. Wait for message: "Starting development server at http://127.0.0.1:8000/"

### B. Access Swagger UI

1. Open your web browser
2. Navigate to: `http://localhost:8000/api/docs/`
3. You should see the Swagger UI interface with all API endpoints listed

### C. Understanding Swagger UI Navigation

- **Sections:** APIs are grouped (accounts, teams, tournaments)
- **Blue GET:** Read/retrieve data
- **Green POST:** Create/submit data
- **Orange PUT/PATCH:** Update data
- **Red DELETE:** Delete data

**How to use an endpoint:**
1. Click on the endpoint to expand it
2. Click "Try it out" button (top right)
3. Fill in parameters and request body
4. Click "Execute" button
5. View response below (status code + response body)

---

## Complete Tournament Workflow - 15 Steps

---

## Complete Tournament Workflow - 15 Steps

---

## STEP 1: Create Organizer Account

### Navigation in Swagger:
1. Scroll to **"accounts"** section
2. Find **`POST /api/accounts/users/`**
3. Click on it to expand
4. Click **"Try it out"** button

### Request Body:
**Copy this entire JSON and paste into the Request body field:**

```json
{
  "username": "organizer1",
  "email": "organizer1@esports.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "is_organizer": true
}
```

### Execute:
1. Click the blue **"Execute"** button
2. Scroll down to see the response

### Expected Response:
- **Status Code:** `201 Created`
- **Response Body:** Will contain user details including `"id": 1`

**IMPORTANT:** Write down or copy the `id` value (e.g., `1`) - you'll need this as `organizer_id` in Step 3.

### Authentication:
After creating the organizer, you need to log in to make authenticated requests:

**Option 1 - Django Admin Login:**
1. Open new tab: `http://localhost:8000/admin/`
2. Login with: `organizer1` / `password123`
3. Return to Swagger tab (you're now authenticated)

**Option 2 - Swagger Authorize:**
1. Click **"Authorize"** button at top of Swagger page
2. Enter credentials if prompted
3. Click "Authorize"

---

## STEP 2: Create 50 Teams (Bulk Upload)

### Navigation in Swagger:
1. Scroll to **"teams"** section
2. Find **`POST /api/teams/teams/bulk_create/`**
3. Click on it to expand
4. Click **"Try it out"** button

### Request Body:
**Copy this entire JSON and paste into the Request body field:**

```json
{
  "teams": [
    {"name": "Team Alpha", "country": "USA", "is_active": true},
    {"name": "Team Beta", "country": "USA", "is_active": true},
    {"name": "Team Gamma", "country": "USA", "is_active": true},
    {"name": "Team Delta", "country": "USA", "is_active": true},
    {"name": "Team Epsilon", "country": "USA", "is_active": true},
    {"name": "Team Zeta", "country": "USA", "is_active": true},
    {"name": "Team Eta", "country": "USA", "is_active": true},
    {"name": "Team Theta", "country": "USA", "is_active": true},
    {"name": "Team Iota", "country": "USA", "is_active": true},
    {"name": "Team Kappa", "country": "USA", "is_active": true},
    {"name": "Team Lambda", "country": "USA", "is_active": true},
    {"name": "Team Mu", "country": "USA", "is_active": true},
    {"name": "Team Nu", "country": "USA", "is_active": true},
    {"name": "Team Xi", "country": "USA", "is_active": true},
    {"name": "Team Omicron", "country": "USA", "is_active": true},
    {"name": "Team Pi", "country": "USA", "is_active": true},
    {"name": "Team Rho", "country": "USA", "is_active": true},
    {"name": "Team Sigma", "country": "USA", "is_active": true},
    {"name": "Team Tau", "country": "USA", "is_active": true},
    {"name": "Team Upsilon", "country": "USA", "is_active": true},
    {"name": "Team Phi", "country": "USA", "is_active": true},
    {"name": "Team Chi", "country": "USA", "is_active": true},
    {"name": "Team Psi", "country": "USA", "is_active": true},
    {"name": "Team Omega", "country": "USA", "is_active": true},
    {"name": "Team Phoenix", "country": "USA", "is_active": true},
    {"name": "Team Dragon", "country": "USA", "is_active": true},
    {"name": "Team Tiger", "country": "USA", "is_active": true},
    {"name": "Team Lion", "country": "USA", "is_active": true},
    {"name": "Team Eagle", "country": "USA", "is_active": true},
    {"name": "Team Falcon", "country": "USA", "is_active": true},
    {"name": "Team Shark", "country": "USA", "is_active": true},
    {"name": "Team Wolf", "country": "USA", "is_active": true},
    {"name": "Team Bear", "country": "USA", "is_active": true},
    {"name": "Team Panther", "country": "USA", "is_active": true},
    {"name": "Team Viper", "country": "USA", "is_active": true},
    {"name": "Team Thunder", "country": "USA", "is_active": true},
    {"name": "Team Lightning", "country": "USA", "is_active": true},
    {"name": "Team Storm", "country": "USA", "is_active": true},
    {"name": "Team Blaze", "country": "USA", "is_active": true},
    {"name": "Team Frost", "country": "USA", "is_active": true},
    {"name": "Team Shadow", "country": "USA", "is_active": true},
    {"name": "Team Phantom", "country": "USA", "is_active": true},
    {"name": "Team Spirit", "country": "USA", "is_active": true},
    {"name": "Team Legend", "country": "USA", "is_active": true},
    {"name": "Team Titan", "country": "USA", "is_active": true},
    {"name": "Team Warrior", "country": "USA", "is_active": true},
    {"name": "Team Knight", "country": "USA", "is_active": true},
    {"name": "Team Champion", "country": "USA", "is_active": true},
    {"name": "Team Victory", "country": "USA", "is_active": true},
    {"name": "Team Glory", "country": "USA", "is_active": true}
  ]
}
```

### Execute:
1. Click the blue **"Execute"** button
2. Wait a few seconds for all teams to be created

### Expected Response:
- **Status Code:** `201 Created`
- **Response Body:** 
```json
{
  "message": "50 teams created successfully",
  "teams": [
    {"id": 1, "name": "Team Alpha", "tag": "TEAMAL", ...},
    {"id": 2, "name": "Team Beta", "tag": "TEAMBE", ...},
    ...
    {"id": 50, "name": "Team Glory", "tag": "TEAMGL", ...}
  ]
}
```

**IMPORTANT:** Note that teams have IDs from 1 to 50. You'll use these in Step 4.

---

## STEP 3: Create Tournament with 5 Groups

### Navigation in Swagger:
1. Scroll to **"tournaments"** section
2. Find **`POST /api/tournaments/tournaments/`**
3. Click on it to expand
4. Click **"Try it out"** button

### Request Body:
**Copy this entire JSON and paste into the Request body field:**

```json
{
  "name": "Championship 2026",
  "description": "Annual esports championship with 50 teams competing in 5 groups",
  "organizer_id": 1,
  "status": "draft",
  "start_date": "2026-03-01T10:00:00Z",
  "end_date": "2026-03-31T20:00:00Z",
  "prize_pool": "500000.00",
  "max_teams": 50
}
```

**NOTE:** If your organizer has a different ID, change `"organizer_id": 1` to match.

### Execute:
1. Click the blue **"Execute"** button

### Expected Response:
- **Status Code:** `201 Created`
- **Response Body:** Tournament details with `"id": 1` and `"groups_count": 5`

**IMPORTANT:** Write down the tournament `id` (e.g., `1`) - you'll use this as `{tournament_id}` in Steps 4, 5, 11.

**AUTOMATICALLY CREATED:** The system automatically creates 5 groups (A, B, C, D, E) when the tournament is created.

---

## STEP 4: Assign Teams to Groups

### ⚠️ IMPORTANT: Get Your Actual Team IDs First!

**Before proceeding, you MUST find your actual team IDs:**

1. In Swagger, find **`GET /api/teams/teams/`**
2. Click "Try it out" → "Execute"
3. Copy the team IDs from the response
4. The IDs might NOT be 1-50 if you created teams manually!

**Example Response:**
```json
[
  {"id": 1, "name": "Team Alpha", "is_active": true},
  {"id": 2, "name": "Team Beta", "is_active": true},
  ...
]
```

### Navigation in Swagger:
1. Scroll to **"tournaments"** section
2. Find **`POST /api/tournaments/tournaments/{id}/assign_teams/`**
3. Click on it to expand
4. Click **"Try it out"** button

### Parameters:
- **id (Path Parameter):** Enter your tournament ID from Step 3 (e.g., `1`)

### Request Body:
**⚠️ Replace the IDs below with YOUR actual team IDs from the GET request above!**

**Example (if your team IDs are 1-50):**

```json
{
  "team_assignments": {
    "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "B": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "C": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
    "D": [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
    "E": [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
  }
}
```

**EXPLANATION:**
- Each group (A, B, C, D, E) needs exactly 10 team IDs
- Use only IDs that exist in your database
- Make sure teams are active (`"is_active": true`)
- Total: 50 teams across 5 groups

### Execute:
1. Click the blue **"Execute"** button

### Expected Response:
- **Status Code:** `200 OK`
- **Response Body:**
```json
{
  "message": "Teams assigned successfully",
  "tournament": {...}
}
```

---

## STEP 5: Create Matches for All Groups

### Navigation in Swagger:
1. Scroll to **"tournaments"** section
2. Find **`POST /api/tournaments/tournaments/{id}/create_matches/`**
3. Click on it to expand
4. Click **"Try it out"** button

### Parameters:
- **id (Path Parameter):** Enter your tournament ID from Step 3 (e.g., `1`)

### Request Body:
**Copy this entire JSON and paste into the Request body field:**

```json
{
  "matches_per_group": 3,
  "start_time": "2026-03-05T14:00:00Z"
}
```

**EXPLANATION:**
- This creates 3 matches for each of the 5 groups = 15 total matches
- Matches are automatically scheduled 1 hour apart
- First match starts at 2026-03-05 14:00 UTC

### Execute:
1. Click the blue **"Execute"** button

### Expected Response:
- **Status Code:** `201 Created`
- **Response Body:**
```json
{
  "message": "15 matches created successfully",
  "matches_per_group": 3,
  "total_matches": 15,
  "matches": [
    {"id": 1, "group": 1, "match_number": 1, "status": "scheduled", ...},
    {"id": 2, "group": 1, "match_number": 2, "status": "scheduled", ...},
    {"id": 3, "group": 1, "match_number": 3, "status": "scheduled", ...},
    {"id": 4, "group": 2, "match_number": 1, "status": "scheduled", ...},
    ...
    {"id": 15, "group": 5, "match_number": 3, "status": "scheduled", ...}
  ]
}
```

**IMPORTANT:** 
- Note the match IDs (1 through 15)
- Group 1 = Group A, Group 2 = Group B, etc.
- You'll submit results for each match in Step 6

---

## STEP 6: Submit Match Results (Repeat 15 Times)

**YOU MUST DO THIS FOR ALL 15 MATCHES CREATED IN STEP 5**

### Navigation in Swagger:
1. Scroll to **"tournaments"** section
2. Find **`POST /api/tournaments/matches/{id}/submit_results/`**
3. Click on it to expand
4. Click **"Try it out"** button

---

### 6.1 - Group A, Match 1

**Parameters:**
- **id (Path Parameter):** `1`

**Request Body:**
```json
{
  "results": [
    {"team_id": 1, "kill_points": 25, "placement": 1},
    {"team_id": 2, "kill_points": 20, "placement": 2},
    {"team_id": 3, "kill_points": 18, "placement": 3},
    {"team_id": 4, "kill_points": 15, "placement": 4},
    {"team_id": 5, "kill_points": 12, "placement": 5},
    {"team_id": 6, "kill_points": 10, "placement": 6},
    {"team_id": 7, "kill_points": 8, "placement": 7},
    {"team_id": 8, "kill_points": 6, "placement": 8},
    {"team_id": 9, "kill_points": 4, "placement": 9},
    {"team_id": 10, "kill_points": 2, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.2 - Group A, Match 2

**Parameters:**
- **id (Path Parameter):** `2`

**Request Body:**
```json
{
  "results": [
    {"team_id": 1, "kill_points": 30, "placement": 1},
    {"team_id": 2, "kill_points": 25, "placement": 2},
    {"team_id": 3, "kill_points": 22, "placement": 3},
    {"team_id": 4, "kill_points": 18, "placement": 4},
    {"team_id": 5, "kill_points": 15, "placement": 5},
    {"team_id": 6, "kill_points": 12, "placement": 6},
    {"team_id": 7, "kill_points": 10, "placement": 7},
    {"team_id": 8, "kill_points": 8, "placement": 8},
    {"team_id": 9, "kill_points": 5, "placement": 9},
    {"team_id": 10, "kill_points": 3, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.3 - Group A, Match 3

**Parameters:**
- **id (Path Parameter):** `3`

**Request Body:**
```json
{
  "results": [
    {"team_id": 1, "kill_points": 28, "placement": 1},
    {"team_id": 2, "kill_points": 23, "placement": 2},
    {"team_id": 3, "kill_points": 20, "placement": 3},
    {"team_id": 4, "kill_points": 17, "placement": 4},
    {"team_id": 5, "kill_points": 14, "placement": 5},
    {"team_id": 6, "kill_points": 11, "placement": 6},
    {"team_id": 7, "kill_points": 9, "placement": 7},
    {"team_id": 8, "kill_points": 7, "placement": 8},
    {"team_id": 9, "kill_points": 4, "placement": 9},
    {"team_id": 10, "kill_points": 2, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

**Group A Total Kills After 3 Matches:**
- Team 1 (Alpha): 83 kills
- Team 2 (Beta): 68 kills
- Team 3 (Gamma): 60 kills
- Team 4 (Delta): 50 kills
- Team 5 (Epsilon): 41 kills
- Team 6 (Zeta): 33 kills

---

### 6.4 - Group B, Match 1

**Parameters:**
- **id (Path Parameter):** `4`

**Request Body:**
```json
{
  "results": [
    {"team_id": 11, "kill_points": 27, "placement": 1},
    {"team_id": 12, "kill_points": 22, "placement": 2},
    {"team_id": 13, "kill_points": 19, "placement": 3},
    {"team_id": 14, "kill_points": 16, "placement": 4},
    {"team_id": 15, "kill_points": 13, "placement": 5},
    {"team_id": 16, "kill_points": 11, "placement": 6},
    {"team_id": 17, "kill_points": 9, "placement": 7},
    {"team_id": 18, "kill_points": 7, "placement": 8},
    {"team_id": 19, "kill_points": 5, "placement": 9},
    {"team_id": 20, "kill_points": 3, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.5 - Group B, Match 2

**Parameters:**
- **id (Path Parameter):** `5`

**Request Body:**
```json
{
  "results": [
    {"team_id": 11, "kill_points": 29, "placement": 1},
    {"team_id": 12, "kill_points": 24, "placement": 2},
    {"team_id": 13, "kill_points": 21, "placement": 3},
    {"team_id": 14, "kill_points": 18, "placement": 4},
    {"team_id": 15, "kill_points": 15, "placement": 5},
    {"team_id": 16, "kill_points": 12, "placement": 6},
    {"team_id": 17, "kill_points": 10, "placement": 7},
    {"team_id": 18, "kill_points": 8, "placement": 8},
    {"team_id": 19, "kill_points": 6, "placement": 9},
    {"team_id": 20, "kill_points": 4, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.6 - Group B, Match 3

**Parameters:**
- **id (Path Parameter):** `6`

**Request Body:**
```json
{
  "results": [
    {"team_id": 11, "kill_points": 26, "placement": 1},
    {"team_id": 12, "kill_points": 21, "placement": 2},
    {"team_id": 13, "kill_points": 18, "placement": 3},
    {"team_id": 14, "kill_points": 15, "placement": 4},
    {"team_id": 15, "kill_points": 12, "placement": 5},
    {"team_id": 16, "kill_points": 10, "placement": 6},
    {"team_id": 17, "kill_points": 8, "placement": 7},
    {"team_id": 18, "kill_points": 6, "placement": 8},
    {"team_id": 19, "kill_points": 4, "placement": 9},
    {"team_id": 20, "kill_points": 2, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.7 - Group C, Match 1

**Parameters:**
- **id (Path Parameter):** `7`

**Request Body:**
```json
{
  "results": [
    {"team_id": 21, "kill_points": 26, "placement": 1},
    {"team_id": 22, "kill_points": 21, "placement": 2},
    {"team_id": 23, "kill_points": 18, "placement": 3},
    {"team_id": 24, "kill_points": 15, "placement": 4},
    {"team_id": 25, "kill_points": 12, "placement": 5},
    {"team_id": 26, "kill_points": 10, "placement": 6},
    {"team_id": 27, "kill_points": 8, "placement": 7},
    {"team_id": 28, "kill_points": 6, "placement": 8},
    {"team_id": 29, "kill_points": 4, "placement": 9},
    {"team_id": 30, "kill_points": 2, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.8 - Group C, Match 2

**Parameters:**
- **id (Path Parameter):** `8`

**Request Body:**
```json
{
  "results": [
    {"team_id": 21, "kill_points": 28, "placement": 1},
    {"team_id": 22, "kill_points": 23, "placement": 2},
    {"team_id": 23, "kill_points": 20, "placement": 3},
    {"team_id": 24, "kill_points": 17, "placement": 4},
    {"team_id": 25, "kill_points": 14, "placement": 5},
    {"team_id": 26, "kill_points": 11, "placement": 6},
    {"team_id": 27, "kill_points": 9, "placement": 7},
    {"team_id": 28, "kill_points": 7, "placement": 8},
    {"team_id": 29, "kill_points": 5, "placement": 9},
    {"team_id": 30, "kill_points": 3, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.9 - Group C, Match 3

**Parameters:**
- **id (Path Parameter):** `9`

**Request Body:**
```json
{
  "results": [
    {"team_id": 21, "kill_points": 25, "placement": 1},
    {"team_id": 22, "kill_points": 20, "placement": 2},
    {"team_id": 23, "kill_points": 17, "placement": 3},
    {"team_id": 24, "kill_points": 14, "placement": 4},
    {"team_id": 25, "kill_points": 11, "placement": 5},
    {"team_id": 26, "kill_points": 9, "placement": 6},
    {"team_id": 27, "kill_points": 7, "placement": 7},
    {"team_id": 28, "kill_points": 5, "placement": 8},
    {"team_id": 29, "kill_points": 3, "placement": 9},
    {"team_id": 30, "kill_points": 1, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.10 - Group D, Match 1

**Parameters:**
- **id (Path Parameter):** `10`

**Request Body:**
```json
{
  "results": [
    {"team_id": 31, "kill_points": 24, "placement": 1},
    {"team_id": 32, "kill_points": 19, "placement": 2},
    {"team_id": 33, "kill_points": 16, "placement": 3},
    {"team_id": 34, "kill_points": 13, "placement": 4},
    {"team_id": 35, "kill_points": 10, "placement": 5},
    {"team_id": 36, "kill_points": 8, "placement": 6},
    {"team_id": 37, "kill_points": 6, "placement": 7},
    {"team_id": 38, "kill_points": 4, "placement": 8},
    {"team_id": 39, "kill_points": 2, "placement": 9},
    {"team_id": 40, "kill_points": 1, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.11 - Group D, Match 2

**Parameters:**
- **id (Path Parameter):** `11`

**Request Body:**
```json
{
  "results": [
    {"team_id": 31, "kill_points": 26, "placement": 1},
    {"team_id": 32, "kill_points": 21, "placement": 2},
    {"team_id": 33, "kill_points": 18, "placement": 3},
    {"team_id": 34, "kill_points": 15, "placement": 4},
    {"team_id": 35, "kill_points": 12, "placement": 5},
    {"team_id": 36, "kill_points": 10, "placement": 6},
    {"team_id": 37, "kill_points": 8, "placement": 7},
    {"team_id": 38, "kill_points": 6, "placement": 8},
    {"team_id": 39, "kill_points": 4, "placement": 9},
    {"team_id": 40, "kill_points": 2, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.12 - Group D, Match 3

**Parameters:**
- **id (Path Parameter):** `12`

**Request Body:**
```json
{
  "results": [
    {"team_id": 31, "kill_points": 23, "placement": 1},
    {"team_id": 32, "kill_points": 18, "placement": 2},
    {"team_id": 33, "kill_points": 15, "placement": 3},
    {"team_id": 34, "kill_points": 12, "placement": 4},
    {"team_id": 35, "kill_points": 9, "placement": 5},
    {"team_id": 36, "kill_points": 7, "placement": 6},
    {"team_id": 37, "kill_points": 5, "placement": 7},
    {"team_id": 38, "kill_points": 3, "placement": 8},
    {"team_id": 39, "kill_points": 2, "placement": 9},
    {"team_id": 40, "kill_points": 1, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.13 - Group E, Match 1

**Parameters:**
- **id (Path Parameter):** `13`

**Request Body:**
```json
{
  "results": [
    {"team_id": 41, "kill_points": 22, "placement": 1},
    {"team_id": 42, "kill_points": 17, "placement": 2},
    {"team_id": 43, "kill_points": 14, "placement": 3},
    {"team_id": 44, "kill_points": 11, "placement": 4},
    {"team_id": 45, "kill_points": 8, "placement": 5},
    {"team_id": 46, "kill_points": 6, "placement": 6},
    {"team_id": 47, "kill_points": 4, "placement": 7},
    {"team_id": 48, "kill_points": 3, "placement": 8},
    {"team_id": 49, "kill_points": 2, "placement": 9},
    {"team_id": 50, "kill_points": 1, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.14 - Group E, Match 2

**Parameters:**
- **id (Path Parameter):** `14`

**Request Body:**
```json
{
  "results": [
    {"team_id": 41, "kill_points": 24, "placement": 1},
    {"team_id": 42, "kill_points": 19, "placement": 2},
    {"team_id": 43, "kill_points": 16, "placement": 3},
    {"team_id": 44, "kill_points": 13, "placement": 4},
    {"team_id": 45, "kill_points": 10, "placement": 5},
    {"team_id": 46, "kill_points": 8, "placement": 6},
    {"team_id": 47, "kill_points": 6, "placement": 7},
    {"team_id": 48, "kill_points": 5, "placement": 8},
    {"team_id": 49, "kill_points": 3, "placement": 9},
    {"team_id": 50, "kill_points": 2, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

---

### 6.15 - Group E, Match 3

**Parameters:**
- **id (Path Parameter):** `15`

**Request Body:**
```json
{
  "results": [
    {"team_id": 41, "kill_points": 21, "placement": 1},
    {"team_id": 42, "kill_points": 16, "placement": 2},
    {"team_id": 43, "kill_points": 13, "placement": 3},
    {"team_id": 44, "kill_points": 10, "placement": 4},
    {"team_id": 45, "kill_points": 7, "placement": 5},
    {"team_id": 46, "kill_points": 5, "placement": 6},
    {"team_id": 47, "kill_points": 3, "placement": 7},
    {"team_id": 48, "kill_points": 2, "placement": 8},
    {"team_id": 49, "kill_points": 1, "placement": 9},
    {"team_id": 50, "kill_points": 1, "placement": 10}
  ]
}
```
Click **Execute**. Expected: `200 OK`

**✅ All 15 matches completed!**

---

## STEP 7: View Group Standings

You can check standings for each group to verify kill totals.

### Navigation in Swagger:
1. Find **`GET /api/tournaments/groups/{id}/standings/`**
2. Click on it to expand
3. Click **"Try it out"** button

### For Group A (Group ID = 1):
**Parameters:**
- **id (Path Parameter):** `1`

Click **Execute**.

### Expected Response:
Teams ranked by total kills (highest first):
```json
[
  {"team_name": "Team Alpha", "total_kills": 83, "rank": 1, ...},
  {"team_name": "Team Beta", "total_kills": 68, "rank": 2, ...},
  {"team_name": "Team Gamma", "total_kills": 60, "rank": 3, ...},
  ...
]
```

**Repeat for Groups 2-5 to verify all group standings.**

---

## STEP 8: Qualify Top 6 Teams per Group (Repeat 5 Times)

This step selects the top 6 teams by kills in each group.

### Navigation in Swagger:
1. Find **`POST /api/tournaments/groups/{id}/qualify_top_6/`**
2. Click on it to expand
3. Click **"Try it out"** button

---

### 8.1 - Group A (Group ID = 1)

**Parameters:**
- **id (Path Parameter):** `1`

**Request Body:** Leave empty or use `{}`

Click **Execute**. Expected: `200 OK` with top 6 teams marked as qualified.

---

### 8.2 - Group B (Group ID = 2)

**Parameters:**
- **id (Path Parameter):** `2`

**Request Body:** Leave empty or use `{}`

Click **Execute**. Expected: `200 OK`

---

### 8.3 - Group C (Group ID = 3)

**Parameters:**
- **id (Path Parameter):** `3`

**Request Body:** Leave empty or use `{}`

Click **Execute**. Expected: `200 OK`

---

### 8.4 - Group D (Group ID = 4)

**Parameters:**
- **id (Path Parameter):** `4`

**Request Body:** Leave empty or use `{}`

Click **Execute**. Expected: `200 OK`

---

### 8.5 - Group E (Group ID = 5)

**Parameters:**
- **id (Path Parameter):** `5`

**Request Body:** Leave empty or use `{}`

Click **Execute**. Expected: `200 OK`

**✅ All groups now have top 6 qualified!**

---

## STEP 9: Qualify Top 4 from Top 6 (Repeat 5 Times)

This step selects the top 4 teams from the top 6.

### Navigation in Swagger:
1. Find **`POST /api/tournaments/groups/{id}/qualify_top_4/`**
2. Click on it to expand
3. Click **"Try it out"** button

---

### 9.1 - Group A (Group ID = 1)

**Parameters:**
- **id (Path Parameter):** `1`

**Request Body (Automatic):**
```json
{}
```

Click **Execute**. Expected: `200 OK` with top 4 teams.

---

### 9.2 - Group B (Group ID = 2)

**Parameters:**
- **id (Path Parameter):** `2`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`

---

### 9.3 - Group C (Group ID = 3)

**Parameters:**
- **id (Path Parameter):** `3`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`

---

### 9.4 - Group D (Group ID = 4)

**Parameters:**
- **id (Path Parameter):** `4`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`

---

### 9.5 - Group E (Group ID = 5)

**Parameters:**
- **id (Path Parameter):** `5`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`

**✅ All groups now have top 4 qualified!**

---

## STEP 10: Select Group Winner (Repeat 5 Times)

This step selects 1 winner from the top 4 in each group.

### Navigation in Swagger:
1. Find **`POST /api/tournaments/groups/{id}/select_winner/`**
2. Click on it to expand
3. Click **"Try it out"** button

---

### 10.1 - Group A Winner (Group ID = 1)

**Parameters:**
- **id (Path Parameter):** `1`

**Request Body (Automatic - highest kills):**
```json
{}
```

Click **Execute**. Expected: `200 OK`. Winner: Team Alpha (ID 1)

---

### 10.2 - Group B Winner (Group ID = 2)

**Parameters:**
- **id (Path Parameter):** `2`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`. Winner: Team Lambda (ID 11)

---

### 10.3 - Group C Winner (Group ID = 3)

**Parameters:**
- **id (Path Parameter):** `3`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`. Winner: Team Phi (ID 21)

---

### 10.4 - Group D Winner (Group ID = 4)

**Parameters:**
- **id (Path Parameter):** `4`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`. Winner: Team Shark (ID 31)

---

### 10.5 - Group E Winner (Group ID = 5)

**Parameters:**
- **id (Path Parameter):** `5`

**Request Body:**
```json
{}
```

Click **Execute**. Expected: `200 OK`. Winner: Team Shadow (ID 41)

**✅ All 5 group winners selected! Ready for finals!**

**Group Winners:**
- Group A: Team Alpha (ID 1)
- Group B: Team Lambda (ID 11)
- Group C: Team Phi (ID 21)
- Group D: Team Shark (ID 31)
- Group E: Team Shadow (ID 41)

---

## STEP 11: Create Final Stage

### Navigation in Swagger:
1. Find **`POST /api/tournaments/tournaments/{id}/create_final_stage/`**
2. Click on it to expand
3. Click **"Try it out"** button

### Parameters:
- **id (Path Parameter):** Enter your tournament ID from Step 3 (e.g., `1`)

### Request Body:
Leave empty or use `{}`

### Execute:
Click **Execute**

### Expected Response:
- **Status Code:** `201 Created`
- **Response Body:**
```json
{
  "id": 1,
  "tournament": 1,
  "participants": [
    {"id": 1, "name": "Team Alpha", ...},
    {"id": 11, "name": "Team Lambda", ...},
    {"id": 21, "name": "Team Phi", ...},
    {"id": 31, "name": "Team Shark", ...},
    {"id": 41, "name": "Team Shadow", ...}
  ],
  "is_completed": false,
  ...
}
```

**IMPORTANT:** Note the final_stage `id` (e.g., `1`) - you'll use this in Steps 14-15.

---

## STEP 12: Create Final Stage Matches (Repeat 3 Times)

**⚠️ IMPORTANT:** Write down the match IDs returned in the response - you'll need them for Step 13!

**If you forget the IDs:** Use `GET /api/tournaments/final-matches/` to list all matches and find their IDs.

### Navigation in Swagger:
1. Find **`POST /api/tournaments/final-matches/`**
2. Click on it to expand
3. Click **"Try it out"** button

---

### 12.1 - Final Match 1

**Request Body:**
```json
{
  "final_stage": 1,
  "match_number": 1,
  "scheduled_time": "2026-03-30T14:00:00Z",
  "is_completed": false
}
```

Click **Execute**. Expected: `201 Created`. 

**COPY THE MATCH ID FROM RESPONSE!** (e.g., `"id": 16`)

---

### 12.2 - Final Match 2

**Request Body:**
```json
{
  "final_stage": 1,
  "match_number": 2,
  "scheduled_time": "2026-03-30T16:00:00Z",
  "is_completed": false
}
```

Click **Execute**. Expected: `201 Created`.

**COPY THE MATCH ID FROM RESPONSE!** (e.g., `"id": 17`)

---

### 12.3 - Final Match 3

**Request Body:**
```json
{
  "final_stage": 1,
  "match_number": 3,
  "scheduled_time": "2026-03-30T18:00:00Z",
  "is_completed": false
}
```

Click **Execute**. Expected: `201 Created`.

**COPY THE MATCH ID FROM RESPONSE!** (e.g., `"id": 18`)

**✅ 3 final matches created!**

---

## STEP 13: Submit Final Stage Results (Repeat 3 Times)

**⚠️ CRITICAL:** Use the actual match IDs from Step 12, NOT the example IDs shown below (16, 17, 18)!

**If you get "No FinalStageMatch matches the given query":**
- You're using the wrong ID
- Check: `GET /api/tournaments/final-matches/` to see your actual match IDs
- Make sure you completed Step 12 first

### Navigation in Swagger:
1. Find **`POST /api/tournaments/final-matches/{id}/submit_results/`**
2. Click on it to expand
3. Click **"Try it out"** button

---

### 13.1 - Final Match 1 Results

**Parameters:**
- **id (Path Parameter):** Use YOUR first final match ID from Step 12 (example shows `16`, but yours might be different!)

**Request Body:**
```json
{
  "results": [
    {"team_id": 1, "kill_points": 35, "placement": 1},
    {"team_id": 11, "kill_points": 30, "placement": 2},
    {"team_id": 21, "kill_points": 25, "placement": 3},
    {"team_id": 31, "kill_points": 20, "placement": 4},
    {"team_id": 41, "kill_points": 15, "placement": 5}
  ]
}
```

Click **Execute**. Expected: `200 OK`

---

### 13.2 - Final Match 2 Results

**Parameters:**
- **id (Path Parameter):** Use YOUR second final match ID from Step 12 (example shows `17`, but yours might be different!)

**Request Body:**
```json
{
  "results": [
    {"team_id": 1, "kill_points": 40, "placement": 1},
    {"team_id": 11, "kill_points": 32, "placement": 2},
    {"team_id": 21, "kill_points": 27, "placement": 3},
    {"team_id": 31, "kill_points": 22, "placement": 4},
    {"team_id": 41, "kill_points": 18, "placement": 5}
  ]
}
```

Click **Execute**. Expected: `200 OK`

---

### 13.3 - Final Match 3 Results

**Parameters:**
- **id (Path Parameter):** Use YOUR third final match ID from Step 12 (example shows `18`, but yours might be different!)

**Request Body:**
```json
{
  "results": [
    {"team_id": 1, "kill_points": 38, "placement": 1},
    {"team_id": 11, "kill_points": 31, "placement": 2},
    {"team_id": 21, "kill_points": 26, "placement": 3},
    {"team_id": 31, "kill_points": 21, "placement": 4},
    {"team_id": 41, "kill_points": 16, "placement": 5}
  ]
}
```

Click **Execute**. Expected: `200 OK`

**✅ All final match results submitted!**

**Final Stage Total Kills:**
- Team Alpha (1): 113 kills (35+40+38)
- Team Lambda (11): 93 kills (30+32+31)
- Team Phi (21): 78 kills (25+27+26)
- Team Shark (31): 63 kills (20+22+21)
- Team Shadow (41): 49 kills (15+18+16)

---

## STEP 14: Determine Overall Winner

### Navigation in Swagger:
1. Find **`POST /api/tournaments/final-stages/{id}/determine_winner/`**
2. Click on it to expand
3. Click **"Try it out"** button

### Parameters:
- **id (Path Parameter):** `1` (your final_stage ID from Step 11)

### Request Body:
Leave empty or use `{}`

### Execute:
Click **Execute**

### Expected Response:
- **Status Code:** `200 OK`
- **Response Body:**
```json
{
  "id": 1,
  "tournament": 1,
  "winner": {
    "id": 1,
    "name": "Team Alpha",
    "tag": "TEAMAL",
    ...
  },
  "is_completed": true,
  ...
}
```

**🏆 WINNER: Team Alpha!**

---

## STEP 15: View Final Leaderboard

### Navigation in Swagger:
1. Find **`GET /api/tournaments/final-stages/{id}/leaderboard/`**
2. Click on it to expand
3. Click **"Try it out"** button

### Parameters:
- **id (Path Parameter):** `1` (your final_stage ID)

### Execute:
Click **Execute**

### Expected Response:
- **Status Code:** `200 OK`
- **Response Body:**
```json
[
  {"team__id": 1, "team__name": "Team Alpha", "team__tag": "TEAMAL", "total_kills": 113},
  {"team__id": 11, "team__name": "Team Lambda", "team__tag": "TEAMLA", "total_kills": 93},
  {"team__id": 21, "team__name": "Team Phi", "team__tag": "TEAMPH", "total_kills": 78},
  {"team__id": 31, "team__name": "Team Shark", "team__tag": "TEAMSH", "total_kills": 63},
  {"team__id": 41, "team__name": "Team Shadow", "team__tag": "TEAMSH", "total_kills": 49}
]
```

**✅ TOURNAMENT COMPLETE!**

---

## Summary of Complete Tournament

### Final Results:
1. **🥇 Champion:** Team Alpha (113 final kills)
2. **🥈 Runner-up:** Team Lambda (93 final kills)
3. **🥉 Third Place:** Team Phi (78 final kills)
4. **4th Place:** Team Shark (63 final kills)
5. **5th Place:** Team Shadow (49 final kills)

### Tournament Statistics:
- **Total Teams:** 50
- **Groups:** 5 (A, B, C, D, E)
- **Group Stage Matches:** 15 (3 per group)
- **Finalists:** 5 (group winners)
- **Final Stage Matches:** 3
- **Total Matches:** 18

---

## Quick Navigation Checklist

Use this checklist to track your progress:

- [ ] Step 1: Create organizer account
- [ ] Step 2: Create 50 teams (bulk)
- [ ] Step 3: Create tournament
- [ ] Step 4: Assign teams to groups
- [ ] Step 5: Create all matches
- [ ] Step 6: Submit results for all 15 matches
- [ ] Step 7: View group standings
- [ ] Step 8: Qualify top 6 (5 groups)
- [ ] Step 9: Qualify top 4 (5 groups)
- [ ] Step 10: Select winner (5 groups)
- [ ] Step 11: Create final stage
- [ ] Step 12: Create 3 final matches
- [ ] Step 13: Submit 3 final results
- [ ] Step 14: Determine overall winner
- [ ] Step 15: View final leaderboard

---

## Troubleshooting

### Authentication Issues
**Problem:** Getting 401 or 403 errors
**Solution:** 
1. Go to `http://localhost:8000/admin/`
2. Login with organizer1/password123
3. Return to Swagger and retry

### Wrong IDs
**Problem:** Can't find tournament/group/match
**Solution:** Use the GET endpoints to list all resources and find correct IDs:
- GET /api/tournaments/tournaments/
- GET /api/tournaments/groups/
- GET /api/tournaments/matches/

### "No FinalStageMatch matches the given query"
**Problem:** Error when trying to submit final match results (Step 13)
**Solution:** 
1. **Check if final matches exist:** Use `GET /api/tournaments/final-matches/` to list all final stage matches
2. **Verify you completed Step 12:** You must create final matches before submitting results
3. **Use correct match IDs:** The response from Step 12 shows the actual match IDs - use those, not the example IDs (16, 17, 18)
4. **Check match details:** Use `GET /api/tournaments/final-matches/{id}/` to verify a specific match exists

**Quick Fix:**
- In Swagger, find `GET /api/tournaments/final-matches/`
- Click "Try it out" → "Execute"
- Check the response for your actual match IDs
- Use those IDs in Step 13

### Validation Errors
**Problem:** "Must have exactly 10 teams per group"
**Solution:** Check your team_assignments in Step 4 - each array must have exactly 10 team IDs

### Can't Create Final Stage
**Problem:** "Need exactly 5 group winners"
**Solution:** Complete Step 10 for all 5 groups before Step 11

---

## Database Reset (Start Fresh)

If you want to reset and test again:

1. Stop the server (Ctrl+C in terminal)
2. Run:
```bash
python manage.py flush --noinput
python manage.py createsuperuser
```
3. Create new admin user when prompted
4. Restart server: `python manage.py runserver`
5. Start from Step 1

---

**🎮 Happy Testing! 🏆**
