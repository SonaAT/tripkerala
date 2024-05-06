from django.db import models
from django.contrib.auth.models import User

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journal_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class JournalImage(models.Model):
    journal = models.ForeignKey(Journal, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='journal_images/')


class BucketListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_name = models.CharField(max_length=100, blank=True)
    destination_city = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.destination_city

