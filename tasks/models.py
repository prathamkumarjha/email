from django.db import models
from emailservice.common.base_model import BaseModel
from emailservice.common.constants import TASK_TYPE_DICT, TASK_STATUS_DICT, QUEUED, SUCCESS, FAILED, EMAIL, WHATSAPP, TASK_SOURCE_DICT, FLIGHTS, HELPDESK, ACCOUNTS, TASK_NAME_DICT, CREATE_TICKET, SEND_OTP, REGISTER_COMPLAINT, ACCOUNT_APPROVAL, ACCOUNT_APPROVED

# Create your models here.
# add these to constants.py in common folder
class NotificationTask(BaseModel):
    
    STATUS_CHOICES = [
        (TASK_STATUS_DICT[QUEUED], "Queued"),
        (TASK_STATUS_DICT[SUCCESS], "Sent"),
        (TASK_STATUS_DICT[FAILED],"Failed"),
    ]
    
    TYPE_CHOICES = [
    (TASK_TYPE_DICT[EMAIL], "Email"),
    (TASK_TYPE_DICT[WHATSAPP], "Whatsapp")
    ]  
    
    SOURCE_CHOICES =[
    (TASK_SOURCE_DICT[FLIGHTS], "Flights"),
    (TASK_SOURCE_DICT[HELPDESK], "HelpDesk"),
    (TASK_SOURCE_DICT[ACCOUNTS],"Accounts")
    ]
    
    TASK_NAME_CHOICES = [
        (TASK_NAME_DICT[CREATE_TICKET], "create ticket"),
        (TASK_NAME_DICT[SEND_OTP], "send otp"),
        (TASK_NAME_DICT[REGISTER_COMPLAINT], "register complaint"),
        (TASK_NAME_DICT[ACCOUNT_APPROVAL], "account approval"),
        (TASK_NAME_DICT[ACCOUNT_APPROVED], "account approved")
        
    ]
    
    
    source = models.CharField(
        max_length = 20,
        choices= SOURCE_CHOICES,
        help_text="From which service this notification request is coming"
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='queued',
        help_text="Current status of the notification task"
    )
    
    content = models.JSONField(
        help_text="JSON containing notification details: 'to', 'subject', message' "
    )
    
    taskName = models.TextField(
       choices=TASK_NAME_CHOICES,
       help_text="Exactly what are we supposed to do" 
    )
    
    retry = models.PositiveIntegerField(
        default=0,
        help_text="Number of retry attempts made for this notification"
    )
    
    type = models.CharField(
        TYPE_CHOICES,
        help_text = "Platform through which we want to send the data "
    )

    
    def __str__(self):
        return f"NotificationTask {self.id} - {self.status}"
    
    
    