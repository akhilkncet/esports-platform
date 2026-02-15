from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from teams.models import Team


class Tournament(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('registration', 'Registration Open'),
        ('group_stage', 'Group Stage'),
        ('final_stage', 'Final Stage'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_tournaments'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    prize_pool = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_teams = models.IntegerField(default=50, validators=[MinValueValidator(50), MaxValueValidator(50)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tournaments'
        ordering = ['-start_date']
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'

    def __str__(self):
        return self.name


class Group(models.Model):
    GROUP_NAMES = [
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
        ('E', 'Group E'),
    ]

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    name = models.CharField(max_length=1, choices=GROUP_NAMES)
    teams = models.ManyToManyField(Team, related_name='tournament_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'groups'
        unique_together = ['tournament', 'name']
        ordering = ['tournament', 'name']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return f"{self.tournament.name} - Group {self.name}"

    def get_team_count(self):
        return self.teams.count()


class Match(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    match_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_time = models.DateTimeField()
    completed_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        ordering = ['group', 'match_number']
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'
        unique_together = ['group', 'match_number']

    def __str__(self):
        return f"{self.group} - Match {self.match_number}"


class MatchResult(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='results'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='match_results'
    )
    kill_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    placement = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'match_results'
        unique_together = ['match', 'team']
        ordering = ['-kill_points']
        verbose_name = 'Match Result'
        verbose_name_plural = 'Match Results'

    def __str__(self):
        return f"{self.team.tag} - {self.kill_points} kills in {self.match}"


class Standings(models.Model):
    QUALIFICATION_STATUS = [
        ('none', 'Not Qualified'),
        ('top_6', 'Top 6 Qualified'),
        ('top_4', 'Top 4 Qualified'),
        ('winner', 'Group Winner'),
    ]

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='standings'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='standings'
    )
    total_kills = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    matches_played = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rank = models.IntegerField(null=True, blank=True)
    qualification_status = models.CharField(
        max_length=20,
        choices=QUALIFICATION_STATUS,
        default='none'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'standings'
        unique_together = ['group', 'team']
        ordering = ['group', '-total_kills', 'team__name']
        verbose_name = 'Standing'
        verbose_name_plural = 'Standings'

    def __str__(self):
        return f"{self.team.tag} in {self.group} - {self.total_kills} kills"


class FinalStage(models.Model):
    tournament = models.OneToOneField(
        Tournament,
        on_delete=models.CASCADE,
        related_name='final_stage'
    )
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tournament_wins'
    )
    participants = models.ManyToManyField(
        Team,
        related_name='final_stage_participations',
        blank=True
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'final_stages'
        verbose_name = 'Final Stage'
        verbose_name_plural = 'Final Stages'

    def __str__(self):
        return f"Final Stage - {self.tournament.name}"


class FinalStageMatch(models.Model):
    final_stage = models.ForeignKey(
        FinalStage,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    match_number = models.IntegerField()
    scheduled_time = models.DateTimeField()
    completed_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'final_stage_matches'
        unique_together = ['final_stage', 'match_number']
        ordering = ['match_number']
        verbose_name = 'Final Stage Match'
        verbose_name_plural = 'Final Stage Matches'

    def __str__(self):
        return f"Final Match {self.match_number} - {self.final_stage.tournament.name}"


class FinalStageResult(models.Model):
    match = models.ForeignKey(
        FinalStageMatch,
        on_delete=models.CASCADE,
        related_name='results'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='final_results'
    )
    kill_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    placement = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'final_stage_results'
        unique_together = ['match', 'team']
        ordering = ['-kill_points']
        verbose_name = 'Final Stage Result'
        verbose_name_plural = 'Final Stage Results'

    def __str__(self):
        return f"{self.team.tag} - {self.kill_points} kills in final"
