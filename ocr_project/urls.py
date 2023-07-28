from django.urls import path, include
from ocr_app import views

urlpatterns = [
    path('', include('ocr_app.urls', namespace='ocr_app')),
]
