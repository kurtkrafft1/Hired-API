from django.http import HttpResponseServerError
from django.http import HttpResponse
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from hiredapp.models import Job, Customer, EmployeeProfile, Rating
from django.db.models import Count, F, When, Case, IntegerField
from django.utils import timezone
from hiredapp.views.customers.customer import CustomerSerializer
# from hiredapp.views.customers.user import UserSerializer
import json 
import sqlite3 
from hiredapp.views.connection import Connection
import math



class EmployeeProfileSerializer(serializers.HyperlinkedModelSerializer):

    customer = CustomerSerializer('customer')
    class Meta:
        model = EmployeeProfile 
        url = serializers.HyperlinkedIdentityField(
            view_name="employee_profiles",
            lookup_field = "id"
        )
        fields = ('id', 'customer', 'title', 'description', 'job_type_id', 'ratings')
        depth =2


class EmployeeProfiles(ViewSet):

    def list(self, request):

        eps = EmployeeProfile.objects.all()
        for prof in eps:
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = create_ratings

                db_cursor = conn.cursor()
   
                db_cursor.execute('''
                SELECT 
                    SUM(r.number) total,
                    COUNT(r.employee_profile_id) as number,
                    r.employee_profile_id
                    from hiredapp_rating r
                    where employee_profile_id = ?
                ''',(prof.id,))
         
                data = db_cursor.fetchone()
                if data.total is not None:
                    avg = data.total/data.number
                    prof.ratings = custom_round(avg)
                
            # print(data)
            # avg = ratings['total']/ ratings['number']÷
            # prof.ratings = ratings  

        #Check to see if the duery has a filter by user_id attached to it
        user_query = self.request.query_params.get('user_id', None)
        search = self.request.query_params.get('search', None)
        if user_query is not None:
            #if so we grab the user and the find the customer based of that 
            user = User.objects.get(pk=user_query)
            customer = Customer.objects.get(user_id=user)
            #then we filter the profiles based off of that customer
            eps = eps.filter(customer = customer)
        

        serializer = EmployeeProfileSerializer(eps, many=True, context = {'request': request})
        # Now we check if there is a search requested
        if search is not None:
            # check if city is in requested field 
            city = self.request.query_params.get('city', None)
            #check if job type is in requested field
            job_type_id = self.request.query_params.get('job_type_id', None)
            # check if title is in requested field 
            title = self.request.query_params.get('title', None)
            # create a new list to filter all the data through
            new_list = list()
            if city is not None:
                #filter based off othe customers location (the one whose profile it belongs to)
                new_list = list(filter(lambda d: city  in d['customer']['city'].lower(), serializer.data))
            if job_type_id is not None:
                new_list = list(filter(lambda d: int(job_type_id) == int(d['job_type_id']), new_list))
            if title is not None:
                new_list = list(filter(lambda d: title in d['title'].lower(), new_list))
            #Now we return the a response of the filtered data from the serializer
            for prof in new_list:
                print('profile',prof)
                with sqlite3.connect(Connection.db_path) as conn:
                    conn.row_factory = create_ratings

                    db_cursor = conn.cursor()
    
                    db_cursor.execute('''
                    SELECT 
                        SUM(r.number) total,
                        COUNT(r.employee_profile_id) as number,
                        r.employee_profile_id
                        from hiredapp_rating r
                        where employee_profile_id = ?
                    ''',(prof['id'],))
            
                    data = db_cursor.fetchone()
                    if data.total is not None:
                        avg = data.total/data.number
                        prof.ratings = custom_round(avg)

            return Response(new_list)
        else:
            return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        '''
            A function made to retreive once specific profile 
            in te fetch url you need to have a viable PK
        '''

        try: 
            ep = EmployeeProfile.objects.get(pk=pk)
            
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = create_ratings

                db_cursor = conn.cursor()
   
                db_cursor.execute('''
                SELECT 
                    SUM(r.number) total,
                    COUNT(r.employee_profile_id) as number,
                    r.employee_profile_id
                    from hiredapp_rating r
                    where employee_profile_id = ?
                ''',(ep.id,))
         
                data = db_cursor.fetchone()
                if data.total is not None:
                    avg = data.total/data.number
                    ep.ratings = custom_round(avg)

            serializer = EmployeeProfileSerializer(ep, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self,request):
        '''
            A post function that creates a new profile based off of the data given from the user. Note we do not user employeeprofile.objects.create()
            that saves the data prematurely 
        '''
        ep = EmployeeProfile()
        ep.job_type_id = request.data['job_type_id']
        ep.title = request.data["title"]
        ep.description = request.data['description']
        customer = Customer.objects.get(user=request.auth.user)
        ep.customer = customer
        ep.save()
        serializer = EmployeeProfileSerializer(ep, many=False, context={"request":request})
        return Response(serializer.data)
    
    def update(self,request ,pk=None):

        ep = EmployeeProfile.objects.get(pk=pk)
        ep.job_type_id = request.data['job_type_id']
        ep.title = request.data["title"]
        ep.description = request.data['description']
        customer = Customer.objects.get(user=request.auth.user)
        ep.customer = customer
        ep.save()
        serializer = EmployeeProfileSerializer(ep, many=False, context={'request': request})

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self,request, pk=None):

        try:
            ep = EmployeeProfile.objects.get(pk=pk)
            ep.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except EmployeeProfile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def create_ratings(cursor, row):
    row = sqlite3.Row(cursor, row)
    rating = Rating()
    rating.number = row["number"]
    rating.total = row["total"]
    rating.employee_profile_id = row["employee_profile_id"]

    return rating

def custom_round(num):
    # y =math.modf(num)[1]
    
    if math.modf(num)[0]>.5:
        return( math.ceil(num))
    elif math.modf(num)[0]< .5:
        
        return (math.floor(num))
    else:
        return (math.ceil(num))



