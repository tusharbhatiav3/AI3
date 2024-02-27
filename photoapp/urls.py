from photoapp import views
from django.urls import path

urlpatterns = [
    path('',views.process_image, name='image')
]