from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename="profile")
router.register(r'posts', views.PostViewSet, basename="post")
router.register(r'likes', views.LikeViewSet, basename="like")


urlpatterns = [
    path('', include(router.urls)),
    path('api/analytics/', views.LikeAnalyticsList.as_view()),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
]
