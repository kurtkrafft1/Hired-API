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
from hiredapp.views.customers.customer import CustomerSerializer
# from hiredapp.views.customers.user import UserSerializer
import json 


class EmployeeProfileSerializer(serializers.HyperlinkedModelSerializer):

    customer = CustomerSerializer('customer')
    class Meta:
        model = EmployeeProfile 
        url = serializers.HyperlinkedIdentityField(
            view_name="employee_profiles",
            lookup_field = "id"
        )
        fields = ('id', 'customer', 'title', 'description', 'job_type_id')
        depth =2

class EmployeeProfiles(ViewSet):

    def list(self, request):

        eps = EmployeeProfile.objects.all()

        user_query = self.request.query_params.get('user_id', None)
        if user_query is not None:
            user = User.objects.get(pk=user_query)
            customer = Customer.objects.get(user_id=user)
            eps = eps.filter(customer = customer)
        serializer = EmployeeProfileSerializer(eps, many=True, context = {'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):

        try: 
            ep = EmployeeProfile.objects.get(pk=pk)

            serializer = EmployeeProfileSerializer(ep, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self,request):

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
        ep.customer_id = request.data['customer_id']
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
