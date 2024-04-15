from photoapp import views
from django.urls import path

urlpatterns = [
    path('',views.process_image, name='image'),
    path('new/', views.yolo_image_process, name = "area and material")
]