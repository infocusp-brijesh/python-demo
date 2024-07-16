from django.db import models
from django.utils import timezone

# Create your models here.
class Users(models.Model):
  USER_STATUS = [
    ('a', 'ACTIVE'),
    ('i', 'IN_ACTIVE'),
    ('d', 'DELETED'),
  ]

  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  user_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=200)
  email_verified = models.BooleanField(default=False)
  phone_number = models.CharField(max_length=11)
  phone_verified = models.BooleanField(default=False)
  password = models.CharField(max_length=20)
  status = models.CharField(choices=USER_STATUS, default='a', max_length=1)
  token = models.TextField(null=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)
  deleted_at = models.DateTimeField(null=True)

  def __str__(self):
    return self.user_name