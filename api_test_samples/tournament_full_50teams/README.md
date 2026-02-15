# Complete 50-Team Tournament Setup Guide

Follow these steps to set up a full tournament with the 5-group structure.

## 📋 Step 1: Create Tournament

**Endpoint:** `POST /api/tournaments/tournaments/`  
**File:** `01_tournament.json`

This creates the main tournament with max 50 teams.

---

## 👥 Step 2: Create 50 Teams

You can either:

### Option A: Use sample_50_teams.json
Load the pre-made 50 teams file from the root directory:
```bash
python manage.py loaddata sample_50_teams.json
```

### Option B: Create via API
Create 50 teams using the API (use team creation samples as templates).

**Recommended team names pattern:**
- Group A: Team Alpha, Team Apex, Team Arrow, Team Atlas, Team Aurora, Team Aether, Team Azure, Team Aegis, Team Armor, Team Astro
- Group B: Team Bolt, Team Blaze, Team Blade, Team Boost, Team Brick, Team Breeze, Team Bronze, Team Burst, Team Blast, Team Brave
- Group C: Team Comet, Team Crown, Team Cyber, Team Cosmos, Team Crest, Team Clash, Team Cruise, Team Charge, Team Chaos, Team Chill
- Group D: Team Delta, Team Dragon, Team Drift, Team Dynamo, Team Dawn, Team Dusk, Team Demon, Team Duos, Team Dash, Team Divine
- Group E: Team Echo, Team Elite, Team Epic, Team Eagle, Team Edge, Team Energy, Team Ember, Team Eternal, Team Empire, Team Extreme

---

## 🏆 Step 3: Create 5 Groups

**Endpoint:** `POST /api/tournaments/groups/`

Create all 5 groups:
1. **Group A** - Use `02_group_a.json`
2. **Group B** - Use `03_group_b.json`
3. **Group C** - Use `04_group_c.json`
4. **Group D** - Use `05_group_d.json`
5. **Group E** - Use `06_group_e.json`

---

## 📝 Step 4: Assign Teams to Groups

After creating groups and teams, update each group with 10 team IDs.

### Group A - Update with teams 1-10
**Endpoint:** `PUT /api/tournaments/groups/1/`
```json
{
  "tournament": 1,
  "name": "A",
  "teams": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```

### Group B - Update with teams 11-20
**Endpoint:** `PUT /api/tournaments/groups/2/`
```json
{
  "tournament": 1,
  "name": "B",
  "teams": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
}
```

### Group C - Update with teams 21-30
**Endpoint:** `PUT /api/tournaments/groups/3/`
```json
{
  "tournament": 1,
  "name": "C",
  "teams": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
}
```

### Group D - Update with teams 31-40
**Endpoint:** `PUT /api/tournaments/groups/4/`
```json
{
  "tournament": 1,
  "name": "D",
  "teams": [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
}
```

### Group E - Update with teams 41-50
**Endpoint:** `PUT /api/tournaments/groups/5/`
```json
{
  "tournament": 1,
  "name": "E",
  "teams": [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
}
```

---

## 🎮 Step 5: Create Group Stage Matches

For each group, create multiple matches (typically 6-10 per group).

### Example: Group A - Match 1
**Endpoint:** `POST /api/tournaments/matches/`
```json
{
  "group": 1,
  "match_number": 1,
  "status": "scheduled",
  "scheduled_time": "2026-04-02T14:00:00Z"
}
```

**Repeat for all groups:**
- Group A: Matches 1-10
- Group B: Matches 1-10
- Group C: Matches 1-10
- Group D: Matches 1-10
- Group E: Matches 1-10

---

## 📊 Step 6: Record Match Results & Kills

After each match, record kills for each team. This updates the standings.

**Example:** Recording kills for Match 1 in Group A

For each team in the match, you would typically have a MatchTeam entry with:
```json
{
  "match": 1,
  "team": 1,
  "kills": 15,
  "placement": 1
}
```

(This depends on your MatchTeam model implementation)

---

## 📈 Step 7: View Group Standings

**Endpoint:** `GET /api/tournaments/standings/?group=1`

This shows current standings for Group A based on cumulative kills.

Check standings for each group:
- `/api/tournaments/standings/?group=1` (Group A)
- `/api/tournaments/standings/?group=2` (Group B)
- `/api/tournaments/standings/?group=3` (Group C)
- `/api/tournaments/standings/?group=4` (Group D)
- `/api/tournaments/standings/?group=5` (Group E)

---

## 🏆 Step 8: Identify Group Winners

After all group matches are complete:

1. **Top 6 from each group** - teams ranked 1-6 by kills
2. **Top 4 from Top 6** - teams ranked 1-4
3. **Group Winner** - #1 ranked team in each group

**You should have 5 group winners (one from each group).**

---

## 🎯 Step 9: Create Final Stage

**Endpoint:** `POST /api/tournaments/final-stages/`
```json
{
  "tournament": 1,
  "name": "Grand Finals",
  "format": "single_elimination",
  "teams": [1, 11, 21, 31, 41]
}
```

(Replace team IDs with actual group winner IDs)

---

## 🔥 Step 10: Create Final Matches

**Endpoint:** `POST /api/tournaments/final-matches/`

Create final stage matches for the 5 group winners.

```json
{
  "final_stage": 1,
  "match_number": 1,
  "status": "scheduled",
  "scheduled_time": "2026-04-14T18:00:00Z"
}
```

Create 3-6 final matches.

---

## 🏅 Step 11: Record Final Results

Record kills for each team in final matches.

The team with the highest cumulative kills in final stage wins the tournament!

---

## ✅ Step 12: Complete Tournament

**Endpoint:** `PUT /api/tournaments/tournaments/1/`
```json
{
  "status": "completed"
}
```

---

## 🎊 Tournament Complete!

You now have:
- ✅ 1 Tournament
- ✅ 50 Teams
- ✅ 5 Groups (10 teams each)
- ✅ 50+ Group Stage Matches
- ✅ 5 Group Winners
- ✅ Final Stage with 5 competitors
- ✅ 1 Champion 🏆

---

## 📱 View in Frontend

Access your frontend at `http://localhost:8000/` to see:
- Dashboard with tournament statistics
- Teams page with all 50 teams
- Tournaments page with detailed views
- Group standings
- Final standings

---

## 🔄 Quick Reset

To start over:
```bash
python clear_data.py
```

Then begin again from Step 1!
