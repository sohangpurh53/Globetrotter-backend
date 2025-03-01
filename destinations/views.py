from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Destination, UserProfile
from .serializers import DestinationSerializer, UserProfileSerializer, UserCreateSerializer
import random

class RandomDestinationView(generics.RetrieveAPIView):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()

    def get(self, request, *args, **kwargs):
        # Get random destination and 3 other random cities for multiple choice
        all_destinations = list(self.get_queryset())
        if len(all_destinations) < 4:
            return Response(
                {"error": "Not enough destinations in database"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        correct_destination = random.choice(all_destinations)
        wrong_options = random.sample([d for d in all_destinations if d != correct_destination], 3)
        
        # Get 1-2 random clues
        num_clues = random.randint(1, 2)
        selected_clues = random.sample(correct_destination.clues, num_clues)
        
        # Create and shuffle options
        options = [correct_destination.city] + [d.city for d in wrong_options]
        random.shuffle(options)
        
        return Response({
            'clues': selected_clues,
            'options': options,
            'correct_city': correct_destination.city,  # Include for verification
            'country': correct_destination.country  # Include country for context
        })

class GuessView(generics.CreateAPIView):
    serializer_class = DestinationSerializer

    def post(self, request, *args, **kwargs):
        city = request.data.get('city')
        user_guess = request.data.get('guess')
        username = request.data.get('username')  # Get username from request data
        
        try:
            destination = Destination.objects.get(city__iexact=city)
        except Destination.DoesNotExist:
            return Response(
                {"error": "City not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        is_correct = destination.city.lower() == user_guess.lower()
        
        response_data = {
            'correct': is_correct,
            'city': destination.city,
            'country': destination.country
        }

        # Always include fun facts regardless of correct/incorrect answer
        response_data['fun_fact'] = random.choice(destination.fun_facts)
        
        # Handle user profile updates
        if username:
            try:
                user = User.objects.get(username=username)
                profile = user.userprofile
                
                # Always increment total attempts
                profile.total_attempts += 1
                
                if is_correct:
                    # Add trivia only for correct answers
                    response_data['trivia'] = random.choice(destination.trivia)
                    
                    # Only increment score and add to solved destinations if correct
                    if destination not in profile.destinations_solved.all():
                        profile.score += 1
                        profile.destinations_solved.add(destination)
                
                profile.save()
                response_data['new_score'] = profile.score
                response_data['total_attempts'] = profile.total_attempts
                
            except User.DoesNotExist:
                # If user doesn't exist, don't update score
                pass
        elif is_correct:
            # For users without a username, still provide trivia for correct answers
            response_data['trivia'] = random.choice(destination.trivia)
        
        return Response(response_data)

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return UserProfile.objects.select_related('user').prefetch_related('destinations_solved')
    
# class GetAllDestination(generics.ListAPIView):
#     queryset = Destination.objects.all()
#     serializer_class = DestinationSerializer