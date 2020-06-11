from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from hiredapp.models import JobType

class JobTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = JobType
        url = serializers.HyperlinkedIdentityField(
            view_name="job_types",
            lookup_field = "id"
        )
        fields = ( 'id', 'title')

class JobTypes(ViewSet):

    def list(self,request):

        jts = JobType.objects.all()
        serializer = JobTypeSerializer(jts, many=True, context={'request': request})

        return Response(serializer.data)