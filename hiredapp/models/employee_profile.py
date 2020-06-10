from django.db import models
from hiredapp.models import Customer, JobType

class EmployeeProfile(models.Model):
    '''
    Employee Profile Class

    Arguments Required:
    job_type_id
    customer_id
    title
    description

    '''

    job_type = models.ForeignKey(JobType, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=300)
    ratings = 0

