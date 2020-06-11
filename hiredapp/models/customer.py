from django.db import models
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.models import User

class Customer(models.Model):
    '''
    Customer Model

    Arguments Required:
    user_id
    address
    zipcode
    phone number


    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=55)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = (F('user__date_joined').asc(nulls_last=True),)


