from rest_framework import serializers
from mybtcapp.models import BitcoinPrice, BitcoinPrediction

class BitcoinPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinPrice
        fields = ['date', 'close']

class BitcoinPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinPrediction
        fields = ['date', 'predicted_close']
