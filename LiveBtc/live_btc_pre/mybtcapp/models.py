from django.db import models

# Create your models here.
from django.db import models

class BitcoinPrice(models.Model):
    date = models.DateField(unique=True)
    close = models.FloatField()

    def __str__(self):
        return f"{self.date} - ${self.close}"


class BitcoinPrediction(models.Model):
    date = models.DateField(unique=True)
    predicted_close = models.FloatField()

    def __str__(self):
        return f"Prediction for {self.date} - ${self.predicted_close}"
