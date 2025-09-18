from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    folder_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username}_{self.key}"
    

class UserFile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
