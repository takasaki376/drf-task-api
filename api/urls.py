from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import TaskViewSet

routers = routers.DefaultRouter()
routers.register('task' , TaskViewSet)

urlpatterns = [
    path('',include(routers.urls))
]