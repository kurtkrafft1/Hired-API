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
from hiredapp.views.customers.user import UserSerializer
from django.utils import timezone
import json 

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # nest a serializer for user so we don't get all the information on the user just the stuff we need - first name and last name 
    user = UserSerializer('user')
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field = "id"
        )
        fields = ('id', 'address', 'phone_number','city', 'zipcode','user_id', 'user', 'profile_picture')
        depth = 1
    
class Customers(ViewSet):

    def list(self, request):
        try:
            customer = Customer.objects.all()
            if hasattr(request.auth, "user"):
                many = False
                customer = customer.get(user=request.auth.user)

                serializer = CustomerSerializer(
                customer, many=many, context={'request': request})

                return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def retrieve(self,request, pk=None):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, many=False, context={"request": request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    def update(self, request, pk=None):

        customer = Customer.objects.get(pk=pk)
        customer.address = request.data['address']
        customer.phone_number = request.data['phone_number']
        customer.city = request.data['city']
        if request.FILES:
            customer.profile_picture = request.FILES["profile_picture"]
        customer.save()

        serializer = CustomerSerializer(customer,context = {'request': request})
        return Response({}, status=status.HTTP_204_NO_CONTENT)
        