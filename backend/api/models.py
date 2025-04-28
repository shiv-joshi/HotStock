from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    predicted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Today's ticker that users will vote on
class DailyTicker(models.Model):
    date = models.DateField(unique=False)
    symbol = models.CharField(max_length=10)
    prev_symbol = models.CharField(max_length=10, default='') # yesterday's ticker

# Stores all the predictions made
class DailyPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, default='')
    prediction = models.CharField(max_length=4)
    submitted_at = models.DateTimeField(auto_now_add=True)

# Previous prediction user made to help them understand the update in their score
class PreviousPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10, default='')
    correct = models.BooleanField(default=False)

    def __str__(self):
        if self.ticker == "": return "You have yet to make a prediction!"
        guess = "CORRECTLY" if self.correct else "INCORRECTLY"
        return f"You guessed {guess} on {self.ticker}"