from django.urls import path
from .views import RandomDestinationView, GuessView, UserCreateView, UserProfileView,GetAllDestination

urlpatterns = [
    path('destinations/random/', RandomDestinationView.as_view(), name='random-destination'),
    path('guess/', GuessView.as_view(), name='guess'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<str:user__username>/', UserProfileView.as_view(), name='user-profile'),
    path('all/', GetAllDestination.as_view())
] 