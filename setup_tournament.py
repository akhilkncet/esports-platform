import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esports_platform.settings')
django.setup()

from teams.models import Team
from tournaments.models import Tournament, Group, Match
from django.contrib.auth import get_user_model

User = get_user_model()

def setup_full_tournament():
    """
    Set up a complete tournament with:
    - 50 teams
    - 5 groups (A, B, C, D, E)
    - 10 teams per group
    - Sample matches for each group
    """
    
    print("🏆 Setting up complete 50-team tournament...")
    print("=" * 60)
    
    # Get or create organizer
    organizer = User.objects.first()
    if not organizer:
        print("❌ No user found. Please create a superuser first:")
        print("   python create_superuser.py")
        return
    
    print(f"✓ Organizer: {organizer.username}")
    
    # Step 1: Create Tournament
    print("\n📋 Step 1: Creating Tournament...")
    tournament = Tournament.objects.create(
        name="World Championship 2026",
        description="50-team tournament with 5 groups competing for $1M prize pool. Group winners advance to finals based on kill points.",
        organizer=organizer,
        status="group_stage",
        start_date=datetime.now() + timedelta(days=15),
        end_date=datetime.now() + timedelta(days=30),
        prize_pool=1000000.00,
        max_teams=50
    )
    print(f"✓ Tournament created: {tournament.name} (ID: {tournament.id})")
    
    # Step 2: Create 50 Teams
    print("\n👥 Step 2: Creating 50 Teams...")
    
    team_names = {
        'A': ['Alpha', 'Apex', 'Arrow', 'Atlas', 'Aurora', 'Aether', 'Azure', 'Aegis', 'Armor', 'Astro'],
        'B': ['Bolt', 'Blaze', 'Blade', 'Boost', 'Brick', 'Breeze', 'Bronze', 'Burst', 'Blast', 'Brave'],
        'C': ['Comet', 'Crown', 'Cyber', 'Cosmos', 'Crest', 'Clash', 'Cruise', 'Charge', 'Chaos', 'Chill'],
        'D': ['Delta', 'Dragon', 'Drift', 'Dynamo', 'Dawn', 'Dusk', 'Demon', 'Duos', 'Dash', 'Divine'],
        'E': ['Echo', 'Elite', 'Epic', 'Eagle', 'Edge', 'Energy', 'Ember', 'Eternal', 'Empire', 'Extreme']
    }
    
    countries = ['USA', 'UK', 'Germany', 'France', 'South Korea', 'Japan', 'Brazil', 'Canada', 'Sweden', 'China']
    
    all_teams = []
    team_counter = 1
    
    for group_letter, names in team_names.items():
        for name in names:
            team = Team.objects.create(
                name=f"Team {name}",
                tag=f"{name[:3].upper()}",
                country=random.choice(countries),
                is_active=True
            )
            all_teams.append(team)
            print(f"  ✓ Created: {team.name} [{team.tag}] - Team #{team_counter}")
            team_counter += 1
    
    print(f"\n✓ Total teams created: {len(all_teams)}")
    
    # Step 3: Create 5 Groups
    print("\n🏆 Step 3: Creating 5 Groups...")
    
    groups = []
    group_letters = ['A', 'B', 'C', 'D', 'E']
    
    for i, letter in enumerate(group_letters):
        group = Group.objects.create(
            tournament=tournament,
            name=letter
        )
        
        # Assign 10 teams to this group
        start_idx = i * 10
        end_idx = start_idx + 10
        group_teams = all_teams[start_idx:end_idx]
        group.teams.set(group_teams)
        
        groups.append(group)
        team_list = ", ".join([t.name for t in group_teams])
        print(f"  ✓ Group {letter} created with 10 teams:")
        print(f"    {team_list}")
    
    print(f"\n✓ Total groups created: {len(groups)}")
    
    # Step 4: Create Sample Matches for Each Group
    print("\n🎮 Step 4: Creating Sample Matches...")
    
    total_matches = 0
    for group in groups:
        # Create 8 matches per group
        for match_num in range(1, 9):
            match_date = tournament.start_date + timedelta(days=(match_num - 1))
            
            match = Match.objects.create(
                group=group,
                match_number=match_num,
                status='scheduled',
                scheduled_time=match_date
            )
            total_matches += 1
        
        print(f"  ✓ Group {group.name}: Created 8 matches")
    
    print(f"\n✓ Total matches created: {total_matches}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ TOURNAMENT SETUP COMPLETE!")
    print("=" * 60)
    print(f"📊 Tournament: {tournament.name}")
    print(f"   ID: {tournament.id}")
    print(f"   Status: {tournament.status}")
    print(f"   Start: {tournament.start_date.strftime('%Y-%m-%d')}")
    print(f"   End: {tournament.end_date.strftime('%Y-%m-%d')}")
    print(f"   Prize Pool: ${tournament.prize_pool:,.2f}")
    print(f"\n👥 Teams: {len(all_teams)}")
    print(f"🏆 Groups: {len(groups)}")
    print(f"🎮 Matches: {total_matches}")
    print("\n" + "=" * 60)
    print("🌐 Access your tournament at:")
    print("   http://localhost:8000/")
    print("=" * 60)
    
    return tournament

if __name__ == '__main__':
    response = input("⚠️  This will create a new tournament with 50 teams. Continue? (yes/no): ")
    if response.lower() == 'yes':
        setup_full_tournament()
    else:
        print("❌ Operation cancelled")
