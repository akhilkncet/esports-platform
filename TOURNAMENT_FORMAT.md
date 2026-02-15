# Tournament Structure & Rules

## 🏆 Tournament Format

### Overview
This is a **50-team tournament** with a two-stage elimination system based on **kill points**.

---

## 📋 Stage 1: Group Stage

### Group Configuration
- **5 Groups**: A, B, C, D, E
- **10 Teams per Group** (50 total teams)
- Each group plays multiple matches
- Teams earn **kill points** from each match

### Scoring System
- Teams accumulate kill points across all group stage matches
- Kill points are the primary ranking metric
- Higher kills = better ranking

### Group Advancement Rules

**From each group:**

1. **Top 6 Teams** qualify based on total kill points
2. **From Top 6 → Top 4** are selected for semifinals
3. **From Top 4 → Top 1** becomes the **Group Winner**

**Result:** 5 Group Winners advance to Final Stage

---

## 📋 Stage 2: Final Stage

### Final Configuration
- **5 Group Winners** compete
- Multiple final matches played
- Winner determined by highest kill points in finals

### Final Winner
- The team with the **most kill points** in the Final Stage becomes the **Overall Tournament Winner**

---

## 🎯 Tournament Flow

```
50 Teams
    ↓
┌───────────────────────────────────────┐
│        GROUP STAGE (5 Groups)         │
├───────────────────────────────────────┤
│ Group A (10 teams) → Top 6 → Top 4 → Winner │
│ Group B (10 teams) → Top 6 → Top 4 → Winner │
│ Group C (10 teams) → Top 6 → Top 4 → Winner │
│ Group D (10 teams) → Top 6 → Top 4 → Winner │
│ Group E (10 teams) → Top 6 → Top 4 → Winner │
└───────────────────────────────────────┘
                ↓
         5 Group Winners
                ↓
    ┌───────────────────────┐
    │     FINAL STAGE       │
    │    (5 Competitors)    │
    └───────────────────────┘
                ↓
         1 CHAMPION 🏆
```

---

## 📊 Example Group Stage Standings

### Group A - After All Matches

| Rank | Team Name      | Matches | Total Kills | Status          |
|------|----------------|---------|-------------|-----------------|
| 1    | Team Alpha     | 10      | 148         | 🏆 Group Winner |
| 2    | Team Beta      | 10      | 142         | ✅ Top 4        |
| 3    | Team Gamma     | 10      | 135         | ✅ Top 4        |
| 4    | Team Delta     | 10      | 128         | ✅ Top 4        |
| 5    | Team Epsilon   | 10      | 121         | ✅ Top 6        |
| 6    | Team Zeta      | 10      | 115         | ✅ Top 6        |
| 7    | Team Eta       | 10      | 98          | ❌ Eliminated   |
| 8    | Team Theta     | 10      | 87          | ❌ Eliminated   |
| 9    | Team Iota      | 10      | 76          | ❌ Eliminated   |
| 10   | Team Kappa     | 10      | 65          | ❌ Eliminated   |

**Team Alpha wins Group A with 148 kills!**

---

## 📊 Example Final Stage

### Finals - The 5 Group Winners

| Rank | Team Name      | Group | Final Kills | Status              |
|------|----------------|-------|-------------|---------------------|
| 1    | Team Alpha     | A     | 89          | 🎖️ CHAMPION          |
| 2    | Team Phoenix   | B     | 82          | 🥈 2nd Place        |
| 3    | Team Dragon    | C     | 78          | 🥉 3rd Place        |
| 4    | Team Tiger     | D     | 71          | 4th Place           |
| 5    | Team Eagle     | E     | 64          | 5th Place           |

**Team Alpha is the Tournament Champion! 🏆**

---

## 🎮 Match Structure

### Group Stage Matches
- Multiple matches per group (typically 6-10 matches)
- All 10 teams in a group compete in each match
- Kill points are recorded per team per match
- Running total determines rankings

### Final Stage Matches
- All 5 group winners compete together
- Multiple final matches (typically 3-6 matches)
- Cumulative kills determine the champion

---

## 📈 Standings Calculation

### Kill Points System
- Each elimination/kill = 1 point
- Cumulative across all matches
- No placement points (kills only)

### Tiebreakers (if needed)
1. Total kills (primary)
2. Most kills in single match
3. Average kills per match
4. Head-to-head results

---

## 🔄 Tournament Lifecycle

### 1. Registration Phase
- Status: `registration`
- Teams sign up (max 50)
- Groups not yet assigned

### 2. Group Stage
- Status: `group_stage`
- 5 groups created (A, B, C, D, E)
- 10 teams assigned per group
- Multiple matches played
- Standings updated after each match

### 3. Group Stage Completion
- Top 6 from each group identified
- Top 4 from each top 6 selected
- 1 winner per group determined
- 5 group winners advance

### 4. Final Stage
- Status: `final_stage`
- 5 group winners compete
- Final matches played
- Final standings determined

### 5. Tournament Completion
- Status: `completed`
- Champion crowned
- Final standings published

---

## 🏅 Awards & Recognition

### Group Stage
- **Group Winners (5)**: Advance to Finals + Prize
- **Top 4 per Group (20 total)**: Recognition + Participation Prize
- **Top 6 per Group (30 total)**: Qualification Achievement

### Final Stage
- **1st Place**: 🏆 Champion Trophy + 50% Prize Pool
- **2nd Place**: 🥈 Silver + 25% Prize Pool
- **3rd Place**: 🥉 Bronze + 15% Prize Pool
- **4th Place**: 7% Prize Pool
- **5th Place**: 3% Prize Pool

---

## 🎯 Strategic Implications

### For Teams
- **Aggressive Play**: More kills = higher rank
- **Consistency**: Performance across all matches matters
- **Survival**: Can't earn kills if eliminated early
- **Risk/Reward**: High-risk strategies for high kill counts

### Match Importance
- Every match counts toward total
- Early deficits can be overcome
- Momentum shifts possible throughout group stage
- Final stage is fresh start for group winners

---

## 📱 Frontend Display

### Dashboard
- Show all 5 groups
- Current standings per group
- Top 6 highlighted
- Group winners marked

### Group Page
- Detailed standings table
- Match history
- Kill statistics per team
- Progression indicators (Top 6, Top 4, Winner)

### Finals Page
- 5 finalists displayed
- Final match results
- Live standings
- Champion announcement

---

## 🔧 Technical Requirements

### Database Models Required
- **Tournament**: Main tournament info
- **Group**: 5 groups per tournament
- **Team**: 50 teams
- **Match**: Multiple per group + final matches
- **MatchTeam**: Team performance in each match (kills)
- **GroupStanding**: Cumulative standings per group
- **FinalStage**: Finals configuration
- **FinalMatch**: Final stage matches

### Key Calculations
1. Sum kills per team across group matches
2. Rank teams within group by total kills
3. Identify Top 6, Top 4, and Winner per group
4. Track 5 group winners
5. Sum kills in final stage
6. Determine overall champion

---

## ✅ Validation Rules

### Tournament Creation
- `max_teams` must be 50
- Must create exactly 5 groups

### Group Assignment
- Each group must have exactly 10 teams
- Teams cannot be in multiple groups
- All teams must be assigned before group stage starts

### Match Recording
- All teams in group must participate
- Kill counts must be non-negative
- Matches must be in group stage before finals

### Advancement
- Only group winners can enter final stage
- Final stage requires all 5 winners
- Cannot skip group stage

---

## 📊 API Endpoints Usage

### Setup Tournament
1. `POST /api/tournaments/tournaments/` - Create tournament
2. `POST /api/teams/teams/` - Register 50 teams
3. `POST /api/tournaments/groups/` - Create 5 groups
4. Assign 10 teams to each group

### Record Matches
1. `POST /api/tournaments/matches/` - Create match
2. Record kills for each team in match
3. Update standings automatically

### Query Standings
1. `GET /api/tournaments/standings/?group=1` - Group A standings
2. Filter Top 6 teams by kills
3. Identify group winner

### Setup Finals
1. `POST /api/tournaments/final-stages/` - Create final stage
2. Add 5 group winners
3. `POST /api/tournaments/final-matches/` - Create final matches
4. Record final results

---

This tournament structure creates an exciting, competitive format where every elimination matters and teams must perform consistently across multiple matches to succeed! 🎮🏆
