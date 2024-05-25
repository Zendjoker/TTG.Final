from django.db import models
from django.core.exceptions import ValidationError
from Users.models import CustomUser

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    return value

class File(models.Model):
    TYPES = [
        ("video", "Video"),
        ("image", "Image"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=255)
    downloads = models.IntegerField(default=0)
    file = models.FileField(
        upload_to="files/",
        validators=[validate_file_size]
    )
    type = models.CharField(max_length=50, choices=TYPES)

class Gallery(models.Model):
    files = models.ManyToManyField(File)

class Section(models.Model):
    index = models.IntegerField(default=0)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='rooms', null=True, blank=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=10000)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    galleries = models.ManyToManyField(Gallery)
    timestamp = models.DateTimeField(auto_now_add=True)