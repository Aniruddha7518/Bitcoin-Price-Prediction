from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from mybtcapp.ml_model.train_model import train_and_save
from mybtcapp.ml_model.predict import predict_next_10_days
from mybtcapp.models import BitcoinPrediction, BitcoinPrice
from mybtcapp.api.serializers import BitcoinPredictionSerializer, BitcoinPriceSerializer

@api_view(['GET'])
def train_model_api(request):
    train_and_save()
    return Response({"message": "Model trained and saved."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def predict_api(request):
    predictions = predict_next_10_days()
    return Response({"message": "Prediction saved.", "predictions": predictions}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_predictions(request):
    preds = BitcoinPrediction.objects.all().order_by('date')
    serializer = BitcoinPredictionSerializer(preds, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_prices(request):
    prices = BitcoinPrice.objects.all().order_by('date')
    serializer = BitcoinPriceSerializer(prices, many=True)
    return Response(serializer.data)
