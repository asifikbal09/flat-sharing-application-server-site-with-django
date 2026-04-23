from django.db import models
import uuid
from users.models import User

class Flat(models.Model):
    id = models.CharField(max_length=255, default=uuid.uuid4, primary_key=True, unique=True)
    square_feet = models.IntegerField()
    total_bedrooms = models.IntegerField()
    total_rooms = models.IntegerField()
    utilities_description = models.TextField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    rent = models.IntegerField()
    availability = models.BooleanField(default=True)
    advance_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.location