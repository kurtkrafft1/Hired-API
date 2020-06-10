from django.db import models
from django.db.models import F
from hiredapp.models import Customer, EmployeeProfile

class Job(models.Model):
    '''
        Job Model

        Arguments Required:
        Employee_profile id 
        customer id 
    
    '''
    employee_profile = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    review = models.CharField(max_length= 300, null=True, blank=True)

    class Meta:
        ordering = (F('end_date').desc(nulls_last=True),)