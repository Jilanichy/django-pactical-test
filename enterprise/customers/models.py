from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# app contains three distinct plans
PLAN_CHOICES = (
    ('Bronze', 'Globalnet Bronze'),
    ('Silver', 'Globalnet Silver'),
    ('Gold', 'Globalnet Gold')
)

# making a few bangladeshi company for customer to choose from
COMPANY_CHOICES = (
    ('Robi', 'Robi'),
    ('Airtel', 'Airtel'),
    ('Grameenphone', 'Grameenphone'),
    ('Teletalk', 'Teletalk')
)

class SubscriptionInfo(models.Model):
    plan_type = models.CharField(choices=PLAN_CHOICES, max_length=6, blank=True)
    subscriber = models.ForeignKey('auth.User', related_name='SubscriptionInfo', on_delete=models.CASCADE)
    primary_phone_number = models.CharField(max_length=14, unique=True)
    other_phone_number = models.CharField(max_length=14, blank=True)
    subscription_price = models.FloatField(blank=True, default=0)
    subscribed_company = models.CharField(choices=COMPANY_CHOICES, max_length=14)
    contract_initiated = models.DateTimeField(auto_now_add=True)
    phone_number_owner = models.CharField(max_length=100, blank=True)


    # ordering models data based on contract initiated date of a customer
    class Meta:
        ordering = ['contract_initiated']
