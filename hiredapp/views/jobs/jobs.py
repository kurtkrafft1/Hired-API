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

        # customer = None
        # if hasattr(request.auth, "user"):
        #     customer = Customer.objects.get(user=request.auth.user)
        jobs = Job.objects.all()
        # if customer is not None :
        #     jobs = jobs.filter(customer = customer)
        user_query = self.request.query_params.get("user_id", None)
        if user_query is not None:
            user = User.objects.get(pk=user_query)
            customer = Customer.objects.get(user = user)
            jobs = jobs.filter(customer=customer)
        
        Twoser_query = self.request.query_params.get('by_user', None)
        if Twoser_query is not None:
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
            ''', [Twoser_query])
        

        serializer = JobSerializer(jobs, many=True, context={"request": request})

        return Response(serializer.data)
    
    def create(self, request):
        # Grab the user using the token
        customer = Customer.objects.get(user=request.auth.user)
        new_job = Job()
        new_job.start_date = None
        new_job.end_date = None
        ep = EmployeeProfile.objects.get(pk=request.data['employee_profile_id'])
        new_job.employee_profile = ep
        new_job.customer = customer 
        new_job.save()

        serializer = JobSerializer(new_job, context= {'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
 
        add_start = self.request.query_params.get('start', None)
        add_end = self.request.query_params.get('end', None)
        add_review = self.request.query_params.get('review', None)
        # https://stackoverflow.com/a/37607525/798303
        # This resolved an issue with naive datetimes
        date = timezone.now()
        job = Job.objects.get(pk=pk)
        if add_start is not None:   
            job.start_date = date
        if add_end is not None:
            job.end_date = date
        if add_review is not None:
            job.review = request.data['review']

        job.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try :
            job = Job.objects.get(pk=pk)
            # print("JOB", job)
            serializer = JobSerializer(job, many=False, context={'request':request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")
                                 




