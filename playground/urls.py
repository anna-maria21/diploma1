from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.start),
    path("form/", views.sendText)
]
