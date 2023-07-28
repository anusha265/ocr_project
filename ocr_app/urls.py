from django.urls import path
from .import views
app_name='ocr_app'
urlpatterns=[
    path('', views.home, name='home'),
    path('download_text_file/', views.download_text_file, name='download_text_file'),
]