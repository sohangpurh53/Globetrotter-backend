from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    clues = models.JSONField()  # Store list of clues
    fun_facts = models.JSONField()  # Store list of fun facts (note: JSON key is 'fun_fact')
    trivia = models.JSONField()  # Store list of trivia

    class Meta:
        unique_together = ['city', 'country']

    def __str__(self):
        return f"{self.city}, {self.country}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # Correct answers
    total_attempts = models.IntegerField(default=0)  # Total attempts
    destinations_solved = models.ManyToManyField(Destination, blank=True)

    def __str__(self):
        return self.user.username 