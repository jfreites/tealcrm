import datetime
from django.contrib.auth.models import User
from django.db import models

from team.models import Team


class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
    
    def soft_delete(self):
        self.deleted_at = datetime.datetime.today()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
