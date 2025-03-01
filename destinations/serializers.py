from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Destination, UserProfile

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'city', 'country', 'clues', 'fun_facts', 'trivia']

class DestinationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['city', 'country']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    destinations_solved = DestinationBasicSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'score', 'total_attempts', 'destinations_solved']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['username', 'password']
        fields = ['username']
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user