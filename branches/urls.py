from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GymBranchViewSet


router = DefaultRouter()
router.register(r'branches', GymBranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]