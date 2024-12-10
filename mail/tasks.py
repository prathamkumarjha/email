from django.core.mail import EmailMessage
from emailservice.common.response import error_response, success_response
from rest_framework import status
from django.template.loader import render_to_string
from emailservice.common.constants import TASK_STATUS_DICT, QUEUED, FAILED, SUCCESS
from pdf.generate_pdf import generate_flight_ticket

class EmailService:
    # message  = 
    @staticmethod
    def send_email(self, from_email, to_email, subject, html, attachments):
        # email = Email
        return True
   
   
   
   
   
   
   
   
   
    
        
    @staticmethod   
    def accountApprovalAndApproved(task):
        try:
            to_email = task.content.get("to")  
            context = task.content.get("context",{}) 
            subject = task.content.get("subject", "No subject provided")
            from_email = task.content.get("from", "defaultsender@example.com")
            
            if task.taskName == "account approval":   
             template_name = task.content.get("template_name", "flight_ticket.html")
            if task.taskName == "account approved":
                template_name = task.content.get("template_name", "account_approved.html")
                 
            name = task.content.get("name")
            company = task.content.get("company", {})
            if isinstance(to_email, str):
                to_email = [to_email]


            context['name'] = name
            context['company'] = company
            
            message = render_to_string(template_name, context)

            email_message = EmailMessage(
                from_email=from_email,
                to=to_email,
                subject=subject,
                body=message,
            )
            email_message.content_subtype = 'html' 
            email_message.send()

            print(f"Email sent for task {task.id}")
            return TASK_STATUS_DICT[SUCCESS]

        except Exception as e:
            print(f"Error sending email for task {task.id}: {e}")
            return TASK_STATUS_DICT[FAILED]           
    
    
    @staticmethod
    def sendFlightTicket(task):
        try:
            to_email = task.content.get("to")
            context = task.content.get("context", {})
            subject = task.content.get("subject", "Your Flight Ticket")
            from_email = task.content.get("from", "defaultsender@example.com")
            template_name = "flight_ticket.html"

            # Ensure `to_email` is a list
            if isinstance(to_email, str):
                to_email = [to_email]

            # Add extra context if needed
            name = task.content.get("name")
            company = task.content.get("company", {})
            ticket = task.content.get("ticket",{})
            context['name'] = name
            context['company'] = company
            context['ticket'] = ticket
            
            # Render HTML to string
            html_content = render_to_string(template_name, context)

            # Generate PDF
            pdf_path = generate_flight_ticket(ticket)
            with open(pdf_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # Create email
            email_message = EmailMessage(
                from_email=from_email,
                to=to_email,
                subject=subject,
                body=html_content,
            )
            email_message.content_subtype = 'html'
            email_message.attach('flight_ticket.pdf', pdf_data, 'application/pdf')

            # Send email
            email_message.send()

            print(f"Flight ticket email sent for task {task.id}")
            return TASK_STATUS_DICT[SUCCESS]

        except Exception as e:
            print(f"Error sending flight ticket email for task {task.id}: {e}")
            return TASK_STATUS_DICT[FAILED]
        
        
        
        
        
        
        
        
    #     "ticket": {
    #   "booking_order_id": "BO12345678",
    #   "booking_status": "Confirmed",
    #   "company_logo_url": "http://services.kandharitravels.com:8020/media/uploads/Logo%20(1).png",
    #   "created_at": "2023-12-01T14:30:00Z",
    #   "booking_flights": [
    #     {
    #       "flight_pnr": "PNR12345",
    #       "flight_details": {
    #         "from": "DEL",
    #         "to": "DXB",
    #         "boardingFrom": "New Delhi",
    #         "boardingTo": "Dubai",
    #         "segments": [
    #           {
    #             "LayoverTime": null,
    #             "From": "DEL",
    #             "To": "DXB",
    #             "DepartureTime": "2023-12-05T10:30:00Z",
    #             "ArrivalTime": "2023-12-05T13:00:00Z",
    #             "AirlineCode": "EK",
    #             "AirlineName": "Emirates",
    #             "FlightNo": "EK513",
    #             "FromAirport": "Indira Gandhi International Airport",
    #             "ToAirport": "Dubai International Airport",
    #             "DepartureTerminal": "T3",
    #             "ArrivalTerminal": "T1",
    #             "Passengers": [
    #               {
    #                 "title": "Mr",
    #                 "first_name": "John",
    #                 "last_name": "Doe",
    #                 "pnr_number": "ETK1234567890"
    #               },
    #               {
    #                 "title": "Mrs",
    #                 "first_name": "Jane",
    #                 "last_name": "Doe",
    #                 "pnr_number": "ETK1234567891"
    #               }
    #             ]
    #           }
    #         ]
    #       }
    #     }
    #   ],
    #   "total_price": "85000",
    #   "flight_id": "12345"
    # },