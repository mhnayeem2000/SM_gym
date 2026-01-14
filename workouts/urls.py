from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WorkoutPlanViewSet, WorkoutTaskViewSet

router = DefaultRouter()
router.register(r'plans', WorkoutPlanViewSet, basename='workout-plan')
router.register(r'tasks', WorkoutTaskViewSet, basename='workout-task')

urlpatterns = [
    path('', include(router.urls)),
]