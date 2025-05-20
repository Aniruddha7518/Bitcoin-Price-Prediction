from django.urls import path, include

urlpatterns = [
    path('api/', include('mybtcapp.api.urls')),
]
