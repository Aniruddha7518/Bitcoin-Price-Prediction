from django.urls import path
from mybtcapp.api import views

urlpatterns = [
    path('train/', views.train_model_api, name='train-model'),
    path('predict/', views.predict_api, name='predict'),
    path('predictions/', views.get_predictions, name='get-predictions'),
    path('prices/', views.get_prices, name='get-prices'),
]
