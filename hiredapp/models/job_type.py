from django.db import models

class JobType(models.Model):
    '''
        Job Type Model

        Arguments Required
        Title
    '''

    title = models.CharField(max_length=50)

    