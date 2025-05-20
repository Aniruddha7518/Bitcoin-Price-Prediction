from django.core.management.base import BaseCommand
from mybtcapp.ml_model.train_model import train_and_save
from mybtcapp.ml_model.predict import predict_next_10_days

class Command(BaseCommand):
    help = "Fetch data, train model, and predict next 10 days"

    def handle(self, *args, **kwargs):
        train_and_save()
        predict_next_10_days()
        self.stdout.write(self.style.SUCCESS("Retrained and predicted successfully."))
