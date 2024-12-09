from rest_framework.response import Response


def success_response(data=None, message="", status=200):
    """
    Utility function to generate a success response.
    """
    return Response(
        {"payload": data, "message": message, "statusCode": status}, status=status
    )


def error_response(error_details, message, status=400):
    """
    Utility function to generate an error response.
    """
    return Response(
        {"errorMessage": error_details, "message": message, "statusCode": status},
        status=status,
    )
