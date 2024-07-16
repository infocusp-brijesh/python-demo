from django.db import models
from django.utils import timezone

from user.models import Users

# Create your models here.
class Bank_Account(models.Model):
  ACCOUNT_STATUS = [
    ('a', 'ACTIVE'),
    ('i', 'IN_ACTIVE'),
    ('d', 'DELETED'),
  ]
  
  ACCOUNT_TYPE = [
    ('sa', 'SAVINGS'),
    ('cu', 'CURRENT'),
  ]

  user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users')
  current_balance = models.FloatField(default=0, null=False)
  account_type = models.CharField(choices=ACCOUNT_TYPE, default='sa', max_length=2)
  status = models.CharField(choices=ACCOUNT_STATUS, default='a', max_length=1)
  
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)
  deleted_at = models.DateTimeField(null=True)

  def __str__(self):
    return f'{self.pk}-{self.user}-{self.account_type}'