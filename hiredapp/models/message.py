from django.db import models
from django.db.models import F
from hiredapp.models import Customer, Job

class Message(models.Model):

    '''
        messages model

        Arguments Required:

        customer_id ----- option 1 employee messages (filter based off of this to see all the messages to potential and hired employees)
        job_id
        receiver_customer_id------ option 2 employer messages (filter based of this to see messages between employers and the user)
        content 
        created_at 
        # seen boolean
    '''
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    receiver_customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='receivers')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    seen = models.BooleanField(default=True) 

    class Meta:
        ordering = (F('created_at').desc(nulls_last=True),)
