from .models import NotificationTask
from mail.tasks import EmailService
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def notification_factory(task):
    """
    Factory function to return the appropriate notification callable or service object.
    """
    if task.type == "email":
        email_service = EmailService()
        email_task_mapping = {
            "account approval": email_service.accountApprovalAndApproved,
            "account approved": email_service.accountApprovalAndApproved,
            "create ticket": email_service.sendFlightTicket,
        }
        if task.taskName not in email_task_mapping:
            raise ValueError(f"Unknown email task type: {task.taskName}")
        return email_task_mapping[task.taskName]  # Returns a callable function
    elif task.type == "whatsapp":
        # Placeholder for WhatsApp notification service
        def whatsapp_notification(task):
            logger.warning("WhatsApp notification service is not yet implemented.")
            return "not_implemented"
        return whatsapp_notification  # Return a callable function
    else:
        raise ValueError(f"Unknown task type: {task.type}")

def process_task():
    tasks = NotificationTask.objects.filter(retry__lt=10).exclude(status='sent')
    print("coming here")
    for task in tasks:
        try:
            # Get the notification callable
            notification_callable = notification_factory(task)
            print("line 20", task)
            
            # Call the notification function with the task
            status = notification_callable(task)  # Pass the task as an argument

            # Check if the status is valid and within the allowed length
            if len(status) > 10:
                raise ValueError(f"Status '{status}' is too long for task {task.id}.")

            with transaction.atomic():
                print("this is status", status)
                # task.status = status
                # task.retry += 1
                task.save()
        except Exception as e:
            print(f"Error processing task {task.id}: {e}")




      