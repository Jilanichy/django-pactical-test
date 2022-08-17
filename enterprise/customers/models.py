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
  
  	# To get the price per plan based on customer plan selection, there's three plan in PLAN_CHOICES
    def save(self, *args, **kwargs):
        if self.plan_type == 'Bronze':
            self.subscription_price = 500
        elif self.plan_type == 'Silver':
            self.subscription_price = 750
        elif self.plan_type == 'Gold':
            self.subscription_price = 1500
        super(SubscriptionInfo, self).save(*args, **kwargs)

    # if a subscriber subscribed to a paid plan, subscriber will own the phone number otherwise the company
    def save(self, *args, **kwargs):
        if self.plan_type:
            self.phone_number_owner = self.subscriber
        else:
            self.phone_number_owner = self.subscribed_company

        super(SubscriptionInfo, self).save(*args, **kwargs)


    # To get a customer's contract remaining days
    def get_contract_remaining_day(self):
        if PLAN_CHOICES[2][0]:
            return "No termination period, you can cancel any time"
        else:
            today = date.today()
            remaining_day = self.contract_initiated.date() - today
            remaining_day_stripped = str(remaining_day).split(",", 1)[0]
            return f"Contact will end after {remaining_day_stripped} days"


    # ordering models data based on contract initiated date of a customer
    class Meta:
        ordering = ['contract_initiated']
