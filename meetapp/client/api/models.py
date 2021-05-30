from django.db import models
from client.models import Member


class Match(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='match_owner')
    partners = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='match_partners')
    like = models.BooleanField(default=None)
