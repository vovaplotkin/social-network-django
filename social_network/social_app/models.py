from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    last_request = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    text = models.TextField()
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.text[:20]

    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        ordering = ['-created']


LIKE_CHOICES = (
    ('like', 'like'),
    ('unlike', 'unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User '{self.user}' {self.value.lower()}d post '{self.post}'"
