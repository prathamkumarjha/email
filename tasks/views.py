# Create your views here.
from .models import NotificationTask
from .serializers import TaskSerializer
from emailservice.common.response import error_response, success_response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

class CreateTaskView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request):
        
        
        serializer = TaskSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Task registered successfully", status=status.HTTP_201_CREATED,)
        return error_response(
            message="An error occurred while trying to register the task", 
            status=status.HTTP_400_BAD_REQUEST, 
            error_details=serializer.errors 
        )   
     
     
#get individual task status
  
  
class GetTaskView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        
        task_id = request.query_params.get("task_id")
              
        
        tasks = NotificationTask.objects.filter(retry__lt=10).exclude(status='sent')
        if task_id:
            tasks  = tasks.filter(id=task_id)
        serializer = TaskSerializer(tasks, many=True)
        return success_response(
            data=serializer.data,
            message="All unsent tickets fetched successfully.",
            status=status.HTTP_200_OK
        )

          
        