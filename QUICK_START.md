# 🏆 Quick Start - Complete Tournament Setup

## Option 1: Automated Setup (Fastest) ⚡

Run the automated setup script to create everything at once:

```bash
python setup_tournament.py
```

This will create:
- ✅ 1 Tournament (World Championship 2026)
- ✅ 50 Teams (10 per group, A-E themed names)
- ✅ 5 Groups (A, B, C, D, E with 10 teams each)
- ✅ 40 Matches (8 per group)

**Time:** ~30 seconds

---

## Option 2: Manual Setup via API 🔧

Follow the step-by-step guide in:
📄 [`api_test_samples/tournament_full_50teams/README.md`](api_test_samples/tournament_full_50teams/README.md)

**Time:** ~15-30 minutes

---

## Option 3: Use Sample Data 📦

Load pre-made data:

```bash
python manage.py loaddata sample_50_teams.json
```

Then create tournament and groups manually via frontend or API.

**Time:** ~10 minutes

---

## 📚 Documentation Files

### Main Documentation
- 📖 [`TOURNAMENT_FORMAT.md`](TOURNAMENT_FORMAT.md) - Complete tournament rules and structure
  - Explains the 5-group system
  - Kill points ranking
  - Top 6 → Top 4 → Winner progression
  - Final stage format

### API Testing
- 📁 [`api_test_samples/`](api_test_samples/) - JSON files for testing individual endpoints
- 📁 [`api_test_samples/tournament_full_50teams/`](api_test_samples/tournament_full_50teams/) - Complete tournament setup files
- 📄 [`api_test_samples/tournament_full_50teams/MATCH_RESULTS_EXAMPLE.md`](api_test_samples/tournament_full_50teams/MATCH_RESULTS_EXAMPLE.md) - Sample match results with kill points

### Scripts
- 🐍 [`setup_tournament.py`](setup_tournament.py) - Automated tournament creation
- 🐍 [`clear_data.py`](clear_data.py) - Clear all data to start fresh
- 🐍 [`create_superuser.py`](create_superuser.py) - Create admin account

---

## 🚀 Recommended Workflow

### First Time Setup

1. **Create superuser** (if not done):
   ```bash
   python create_superuser.py
   ```

2. **Run automated setup**:
   ```bash
   python setup_tournament.py
   ```

3. **Start servers**:
   ```bash
   python manage.py runserver
   ```

4. **Access frontend**:
   - Open browser: http://localhost:8000
   - Login with your superuser credentials
   - View tournament, teams, and groups

5. **Test in Swagger UI**:
   - Open: http://localhost:8000/api/docs/
   - Try API endpoints interactively

---

## 🎮 Tournament Structure Summary

```
50 TEAMS
    ↓
5 GROUPS (A, B, C, D, E)
├─ 10 teams per group
├─ Multiple matches per group
├─ Teams ranked by TOTAL KILLS
└─ Top 6 → Top 4 → 1 Winner per group
    ↓
5 GROUP WINNERS
    ↓
FINAL STAGE
├─ All 5 winners compete
├─ Multiple final matches
└─ Highest kills = CHAMPION 🏆
```

---

## 📊 Key Concepts

### Kill Points System
- **Primary Metric**: Total kills across all matches
- **1 Kill = 1 Point**
- **Cumulative**: Points add up across matches
- **Ranking**: Higher kills = better rank

### Group Stage Progression
1. **All teams** play in group stage matches
2. **Top 6** teams qualify based on kills
3. **Top 4** from top 6 advance to semifinals
4. **#1 team** becomes group winner
5. **5 group winners** advance to finals

### Final Stage
- Only group winners compete
- Fresh start (new kill count)
- Multiple final matches
- Highest kills = Champion

---

## 🎯 Quick Commands

```bash
# Setup
python setup_tournament.py          # Create full tournament
python clear_data.py                # Clear all data

# Run
python manage.py runserver          # Start backend + frontend

# URLs
http://localhost:8000/              # Frontend
http://localhost:8000/api/docs/     # API Documentation
http://localhost:8000/admin/        # Django Admin
```

---

## 📁 File Structure

```
esports_platform/
├── TOURNAMENT_FORMAT.md            ← Main rules documentation
├── QUICK_START.md                  ← This file
├── setup_tournament.py             ← Automated setup script
├── clear_data.py                   ← Data cleanup script
├── frontend/                       ← Frontend HTML/CSS/JS
│   ├── index.html
│   ├── teams.html
│   ├── tournaments.html
│   ├── style.css
│   └── app.js
└── api_test_samples/               ← API testing files
    ├── 01_create_team.json
    ├── 04_create_tournament.json
    └── tournament_full_50teams/    ← Complete tournament setup
        ├── README.md
        ├── 01_tournament.json
        ├── 02-06_group_*.json
        └── MATCH_RESULTS_EXAMPLE.md
```

---

## 🆘 Troubleshooting

### "Error loading data"
- Make sure backend is running: `python manage.py runserver`
- Check you're logged in at http://localhost:8000/login/

### "Cannot import name..."
- Activate virtual environment: `.venv/scripts/activate`
- Ensure all packages installed: `pip install -r requirements.txt`

### "No user found"
- Create superuser: `python create_superuser.py`
- Or use Django command: `python manage.py createsuperuser`

### Want to start fresh?
```bash
python clear_data.py
python setup_tournament.py
```

---

## 🎊 You're Ready!

Everything you need is set up. Choose your path:

1. **Quick Demo**: Run `setup_tournament.py` → Open http://localhost:8000
2. **Learn API**: Check `TOURNAMENT_FORMAT.md` → Test in Swagger UI
3. **Build Custom**: Use JSON samples in `api_test_samples/`

Good luck with your esports tournament platform! 🏆🎮
