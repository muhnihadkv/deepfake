from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('image', views.image , name="image"),
    path('contact', views.contact , name="contact"),
    path('runAnalysis', views.runAnalysis),
    path('getImages', views.getImages),
]