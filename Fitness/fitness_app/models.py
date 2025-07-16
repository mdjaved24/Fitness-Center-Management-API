from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class FitnessCenter(models.Model):

    CATEGORY_CHOICES = [
        ('GYM','gym'),
        ('YOGA','yoga'),
        ('CROSSFIT','crossfit'),
        ('PILATES','pilates'),
        ('SWIMMING','swimming')
    ]

    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    monthly_fee = models.PositiveIntegerField()
    total_sessions = models.PositiveIntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES, default='GYM', max_length=50)
    facilities = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    established_date = models.DateField()
    created_add = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    