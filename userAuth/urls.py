from django.urls import path
from .views import MyTokenObtainPairView, UserProfile, FollowUser, EditProfile

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #User Profile

    path('edit-profile/', EditProfile, name='edit-profile'),
    path('<str:username>/', UserProfile, name='user-posts'),
    path('<str:username>/saved/', UserProfile, name='user-saved'),
    path('<str:username>/follow/<str:option>', FollowUser, name='follow-user'),
]