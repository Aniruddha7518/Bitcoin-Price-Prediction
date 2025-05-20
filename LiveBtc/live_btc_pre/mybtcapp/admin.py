from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BitcoinPrice, BitcoinPrediction

admin.site.register(BitcoinPrice)
admin.site.register(BitcoinPrediction)
