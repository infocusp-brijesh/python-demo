from django.db import models
from django.utils import timezone
from user.models import Users
from bank_accounts.models import Bank_Account

# Create your models here.

class Transactions(models.Model):
  TRANSACTION_STATUS = [
    ('p', 'PENDING'),
    ('s', 'SUCCESS'),
    ('r', 'REJECTED'),
  ]

  TRANSACTION_TYPE = [
    ('d', 'DEBIT'),
    ('c', 'CREDIT'),
  ]

  user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
  account = models.ForeignKey(Bank_Account, on_delete=models.CASCADE, null=False)

  amount = models.FloatField(default=0)
  transaction_type = models.CharField(choices=TRANSACTION_TYPE,max_length=1)
  amount_after_transaction = models.FloatField(default=0)
  transaction_status = models.CharField(choices=TRANSACTION_STATUS, default='p', max_length=1)

  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)
  deleted_at = models.DateTimeField(null=True)

  def __str__(self):
    return f'{self.pk}-{self.user}-{self.account}'