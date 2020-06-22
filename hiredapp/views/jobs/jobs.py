from django.http import HttpResponseServerError
from django.http import HttpResponse
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from hiredapp.models import Job, Customer, EmployeeProfile
from django.db.models import Count, F, When, Case, IntegerField
from django.utils import timezone
import json 


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User 
        url = serializers.HyperlinkedIdentityField(
            view_name="user",
            lookup_field = "id"
        )
        fields = ( 'id', "first_name", 'last_name')

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer('user')

    class Meta:
        model=Customer
        url= serializers.HyperlinkedIdentityField(
            view_name="customer",
            lookup_field = 'id'
        )
        fields = ('id', 'user', 'address', 'phone_number', 'zipcode', 'city')

class EmployeeProfileSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerSerializer('customer')
    class Meta:
        model= EmployeeProfile
        url = serializers.HyperlinkedIdentityField(
            view_name='employee_profile',
            lookup_field = "id"
        )
        fields = ('id', 'job_type_id', 'customer', 'title', 'description', 'ratings')

class JobSerializer(serializers.HyperlinkedModelSerializer):
    employee_profile = EmployeeProfileSerializer('employee_profile')
    customer = CustomerSerializer('customer')
    class Meta:
        model = Job 
        url = serializers.HyperlinkedIdentityField(
            view_name = "jobs",
            lookup_field= "id"
        )
        fields = ('id', 'employee_profile', 'customer', 'start_date', 'end_date', 'review')
        depth=2

class Jobs(ViewSet):

    def list(self, request):

        jobs = Job.objects.all()
        #filter by user_id if provided the correct query
        user_query = self.request.query_params.get("user_id", None)
        if user_query is not None:
            #grab the user/associate it with customer/ associate it with that jobs so we can show all the jobs for a user
            # user = User.objects.get(pk=user_query)
            customer = Customer.objects.get(user = request.auth.user)
            jobs = jobs.filter(customer=customer)
        
        #Here we check if we are trying to get jobs by the user
        Twoser_query = self.request.query_params.get('by_user', None)
        if Twoser_query is not None:
            customer = Customer.objects.get(user=request.auth.user)
            #we have to use a raw sqlite query because the customer id is nested within employeeprofile and inside that is the user id 
            # We will have access to the user_id through session storage
            #to make more secure we could use token authentication however my stages were incorrect when I set this page up so it wasn't working
            #will update in future if time allows
            jobs = Job.objects.raw('''
            Select 
                j.id, 
                j.start_date,
                j.end_date, 
                j.review, 
                j.customer_id,
                j.employee_profile_id
                from hiredapp_job j 
                left join hiredapp_employeeprofile ep on j.employee_profile_id = ep.id
                left join hiredapp_customer c on ep.customer_id = c.id
                left join auth_user u on c.user_id = u.id 
                where u.id = %s;
            ''', [customer.user.id])
        
        employee_profile = self.request.query_params.get('employee_profile', None)
        if employee_profile is not None:
            print(employee_profile)
            ep = EmployeeProfile.objects.get(pk=employee_profile)
            jobs = jobs.filter(employee_profile = ep)
        

        serializer = JobSerializer(jobs, many=True, context={"request": request})

        return Response(serializer.data)
    
    def create(self, request):
        # Grab the user using the token
        rehire =  self.request.query_params.get('rehire', None)
        if rehire is not None:
            customer = Customer.objects.get(user=request.auth.user)
            new_job = Job()
            new_job.start_date = request.data['start_date']
            new_job.end_date = request.data['end_date']
            ep = EmployeeProfile.objects.get(pk=request.data['employee_profile_id'])
            new_job.review = request.data["review"]
            new_job.employee_profile = ep
            new_job.customer = customer 
            new_job.save()
            

        else:

            customer = Customer.objects.get(user=request.auth.user)
            new_job = Job()
            new_job.start_date = None
            new_job.end_date = None
            ep = EmployeeProfile.objects.get(pk=request.data['employee_profile_id'])
            new_job.employee_profile = ep
            new_job.customer = customer 
            new_job.review = ""
            new_job.save()

        serializer = JobSerializer(new_job, context= {'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        #this will mostly be interacting when the user is messaging someone
        #once the user hits 'hire' it will add the start date 
        #after that the employee will hit finish job and that will add an end_date
        #the review will ideally appear on the home screen of the customer when it is equal to ""
        add_start = self.request.query_params.get('start', None)
        add_end = self.request.query_params.get('end', None)
        rehire =  self.request.query_params.get('rehire', None)
        add_review = self.request.query_params.get('review', None)
        # https://stackoverflow.com/a/37607525/798303
        # This resolved an issue with naive datetimes
        date = timezone.now()
        job = Job.objects.get(pk=pk)
        if add_start is not None:   
            job.start_date = date
        if add_end is not None:
            job.end_date = date
        if rehire is not None:
            job.start_date = date
            job.end_date = None
            job.review = ""
        if add_review is not None:
            job.review = request.data['review']

        job.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try :
            job = Job.objects.get(pk=pk)
            serializer = JobSerializer(job, many=False, context={'request':request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")
                                 




