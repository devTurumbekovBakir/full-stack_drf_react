from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('server/select', views.ServerListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
