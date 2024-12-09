from rest_framework import serializers
from .models import NotificationTask


class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NotificationTask
       
        fields = ['id', 'status', 'content', 'retry', 'type', 'source', 'taskName']
        
class ProcessTaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NotificationTask
        
        fields = ['id', 'status', 'content', 'retry', 'type', 'source', 'taskName']       
        
        