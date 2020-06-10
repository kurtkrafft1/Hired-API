from django.db import models
from hiredapp.models import Customer, EmployeeProfile 

class Rating(models.Model):

    '''
        model for Ratings

        Arguments Required:
        number (max is 5)
        customer id
        employee_profile id

    '''
    number = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    employee_profile = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING)