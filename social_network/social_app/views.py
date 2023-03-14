from django.contrib.auth import get_user_model
from django.db.models import F, Count
from rest_framework import generics, permissions, viewsets
from .models import Profile, Post, Like
from .serializers import ProfileSerializer, PostSerializer, \
    LikeSerializer, LikeAnalyticsSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        profile = Profile.objects.get(pk=self.request.user.id)
        serializer.save(user=profile)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeAnalyticsList(generics.ListAPIView):
    serializer_class = LikeAnalyticsSerializer

    def get_queryset(self):
        queryset = Like.objects.all()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from and date_to:
            queryset = queryset\
                .filter(created__gte=date_from, created__lte=date_to, value="like")\
                .values(date=F("created__date"))\
                .annotate(likes=Count("value"))
        return queryset


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
