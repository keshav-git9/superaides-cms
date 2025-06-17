from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)  # active/inactive
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ForumPost(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField(default=True)  # active/inactive
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ForumReply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.name} on {self.post.title}"
