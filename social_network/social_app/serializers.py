from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Like


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'email', 'created', 'last_login', 'last_request']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'created', 'liked']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'updated', 'value']


class LikeAnalyticsSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    likes = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['date', 'likes']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
