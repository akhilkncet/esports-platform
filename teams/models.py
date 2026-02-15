from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tag = models.CharField(max_length=10, unique=True, blank=True, help_text="Short team tag/abbreviation")
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_teams'
    )
    logo = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'teams'
        ordering = ['name']
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        return f"{self.name} [{self.tag}]"
