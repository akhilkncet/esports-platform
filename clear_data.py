import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esports_platform.settings')
django.setup()

from teams.models import Team
from tournaments.models import (
    Tournament, Group, Match, MatchResult, Standings, 
    FinalStage, FinalStageMatch, FinalStageResult
)

def clear_all_data():
    """Clear all data from the database except users"""
    
    print("🗑️  Clearing all data from database...")
    print("-" * 50)
    
    # Delete in reverse order of dependencies
    
    # Final stage results
    final_stage_results_count = FinalStageResult.objects.all().count()
    FinalStageResult.objects.all().delete()
    print(f"✓ Deleted {final_stage_results_count} final stage results")
    
    # Final stage matches
    final_stage_matches_count = FinalStageMatch.objects.all().count()
    FinalStageMatch.objects.all().delete()
    print(f"✓ Deleted {final_stage_matches_count} final stage matches")
    
    # Final stages
    final_stages_count = FinalStage.objects.all().count()
    FinalStage.objects.all().delete()
    print(f"✓ Deleted {final_stages_count} final stages")
    
    # Standings
    standings_count = Standings.objects.all().count()
    Standings.objects.all().delete()
    print(f"✓ Deleted {standings_count} standings")
    
    # Match results
    match_results_count = MatchResult.objects.all().count()
    MatchResult.objects.all().delete()
    print(f"✓ Deleted {match_results_count} match results")
    
    # Matches
    matches_count = Match.objects.all().count()
    Match.objects.all().delete()
    print(f"✓ Deleted {matches_count} matches")
    
    # Groups
    groups_count = Group.objects.all().count()
    Group.objects.all().delete()
    print(f"✓ Deleted {groups_count} groups")
    
    # Tournaments
    tournaments_count = Tournament.objects.all().count()
    Tournament.objects.all().delete()
    print(f"✓ Deleted {tournaments_count} tournaments")
    
    # Teams
    teams_count = Team.objects.all().count()
    Team.objects.all().delete()
    print(f"✓ Deleted {teams_count} teams")
    
    print("-" * 50)
    print("✅ All data cleared successfully!")
    print("ℹ️  User accounts remain intact")

if __name__ == '__main__':
    response = input("⚠️  This will delete ALL teams, tournaments, and related data. Continue? (yes/no): ")
    if response.lower() == 'yes':
        clear_all_data()
    else:
        print("❌ Operation cancelled")
