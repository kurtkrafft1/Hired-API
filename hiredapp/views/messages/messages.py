from django.http import HttpResponseServerError
from django.http import HttpResponse
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from hiredapp.models import Customer, Message
from django.db.models import Count, F, When, Case, IntegerField
from django.utils import timezone
from hiredapp.views.customers.customer import CustomerSerializer
# from hiredapp.views.customers.user import UserSerializer
import json 

class MessagesSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerSerializer('customer')
    receiver_customer = CustomerSerializer('receiver_customer')
    class Meta:
        model = Message
        url = serializers.HyperlinkedIdentityField(
            view_name="messages",
            lookup_field= "id"
        )
        fields = ('id', 'customer', 'receiver_customer', 'content','created_at', 'job_id')

class Messages(ViewSet):

    def list(self, request):
        get_names = self.request.query_params.get('get_names', None)
        by_job = self.request.query_params.get('by_job', None)
        if get_names is not None:
            customer = Customer.objects.get(user=request.auth.user)
            cId = int(customer.id)
            print("ID", cId)
            print("TYPE", type(cId))
            messages = Message.objects.raw('''
                SELECT
                    m.id,
                    m.content,
                    m.customer_id,
                    m.receiver_customer_id,
                    m.created_at,
                    m.job_id
                    from hiredapp_message m 
                    where m.customer_id = %s or m.receiver_customer_id = %s
                    group by m.job_id;	        
            ''',[cId, cId])
            serializer = MessagesSerializer(messages, many=True, context={"request": request})
            
            return  Response(serializer.data)
        if by_job is not None:
            messages = Message.objects.all()
            messages = messages.filter(job_id=by_job)

            serializer = MessagesSerializer(messages, many=True, context={"request":request})
            return Response(serializer.data)
    
    def create(self,request):
        message = Message()
        customer = Customer.objects.get(user=request.auth.user)
        message.customer = customer
        receiver_customer= Customer.objects.get(id=request.data['receiver_customer_id'])
        message.receiver_customer = receiver_customer
        message.content = request.data['content']
        message.created_at = timezone.now()
        message.job_id = request.data['job_id']
        message.save()

        serializer = MessagesSerializer(message, context={"request":request})
        return Response(serializer.data)