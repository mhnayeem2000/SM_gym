from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('api.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/branches/', include('branches.urls')),
    path('api/workouts/', include('workouts.urls')),



    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),

]
