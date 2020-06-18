from django.http import HttpResponseServerError
from django.http import HttpResponse
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from hiredapp.models import Customer, EmployeeProfile, Rating
from django.db.models import Count, F, When, Case, IntegerField
from hiredapp.views.employee_profiles.employee_profiles import EmployeeProfileSerializer

class RatingsSerializer(serializers.HyperlinkedModelSerializer):
    employee_profile = EmployeeProfileSerializer('employee_profile')
    
    class Meta:
        model = Rating
        url = serializers.HyperlinkedIdentityField(
            view_name="ratings",
            lookup_field = "id"
        )
        fields = ("id", "customer", "employee_profile", "number")


class Ratings(ViewSet):
    def create(self, request):
        rating = Rating()
        rating.number = int(request.data["number"])
        ep = EmployeeProfile.objects.get(pk = request.data["employee_profile_id"])
        rating.employee_profile = ep
        customer = Customer.objects.get(user= request.auth.user)
        rating.customer = customer
        rating.save()
        serializer = RatingsSerializer(rating, many=False, context={"request": request})
        return Response(serializer.data)
