from django.template.loader import render_to_string
from weasyprint import HTML
from django.template.loader import get_template

import os

def generate_flight_ticket(data):
    """
    Generate a PDF for the flight ticket.
    :param data: Dictionary containing ticket details
    :return: Path to the generated PDF
    """
    # Render HTML content
    html_content = render_to_string("ticket.html", data)

    # Define the file path
    pdf_file_path = os.path.join("generated_tickets", f"ticket_{data['flight_id']}.pdf")
    os.makedirs("generated_tickets", exist_ok=True)

    # Generate PDF from HTML
    HTML(string=html_content).write_pdf(pdf_file_path)
    print(pdf_file_path)
    return pdf_file_path
