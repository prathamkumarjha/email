# Commonly used constants
BASE_URL = "http://example.com"
API_VERSION = "v1"
DEFAULT_TIMEOUT = 30  # in seconds

# Commonly used status codes
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_ACCEPTED = 202
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_METHOD_NOT_ALLOWED = 405
HTTP_STATUS_CONFLICT = 409
HTTP_SESSION_EXPIRED = 419
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
HTTP_STATUS_NOT_IMPLEMENTED = 501
HTTP_STATUS_BAD_GATEWAY = 502
HTTP_STATUS_SERVICE_UNAVAILABLE = 503
HTTP_STATUS_GATEWAY_TIMEOUT = 504

# Common error messages
ERROR_BAD_REQUEST = "Bad request."
ERROR_UNAUTHORIZED = "Unauthorized access."
ERROR_FORBIDDEN = "Access forbidden."
ERROR_NOT_FOUND = "Resource not found."
ERROR_METHOD_NOT_ALLOWED = "Method not allowed."
ERROR_CONFLICT = "Resource conflict."
ERROR_INTERNAL_SERVER_ERROR = "Internal server error."
ERROR_NOT_IMPLEMENTED = "Feature not implemented."
ERROR_BAD_GATEWAY = "Bad gateway."
ERROR_SERVICE_UNAVAILABLE = "Service unavailable."
ERROR_GATEWAY_TIMEOUT = "Gateway timeout."


AIR_ARABIA_PROVIDER = "AA"
LOCAL_PROVIDER = "LOCAL"

COMPLETED = "COMPLETED"
PENDING = "PENDING"
ERROR = "ERROR"
IN_PROGRESS = "IN_PROGRESS"
CANCELLED = "CANCELLED"
FAILED = "FAILED"
SUCCESS = "SUCCESS"

# Create a dictionary to map status types to their values
STATUS_DICT = {
    COMPLETED: "The task has been completed successfully.",
    PENDING: "The task is pending and yet to start.",
    ERROR: "An error occurred while processing the task.",
    IN_PROGRESS: "The task is currently in progress.",
    CANCELLED: "The task has been cancelled.",
    FAILED: "The task has failed.",
   SUCCESS: "The task was successful.",
}


#task status
QUEUED = "QUEUED"
SUCCESS = "SUCCESS"
FAILED = "FAILED"


TASK_STATUS_DICT = {
    QUEUED: "queued",
    SUCCESS: "success",
    FAILED: "failed"
}



 

#task type 
EMAIL ="EMAIL"
WHATSAPP = "WHATSAPP"

TASK_TYPE_DICT = {
    EMAIL: "email",
    WHATSAPP:"whatsapp"
}


 


#task source
FLIGHTS = "FLIGHTS"
HELPDESK = "HELPDESK"
ACCOUNTS = "ACCOUNTS"

TASK_SOURCE_DICT = {
    FLIGHTS: "flights",
    HELPDESK:"helpdesk",
    ACCOUNTS:"accounts"
}


# task name
CREATE_TICKET = "CREATE_TICKET"
REGISTER_COMPLAINT = "REGISTER_COMPLAINT"
SEND_OTP = "SEND_OTP"
ACCOUNT_APPROVAL="ACCOUNT_APPROVAL"
ACCOUNT_APPROVED="ACCOUNT_APPROVED"

TASK_NAME_DICT = {
    CREATE_TICKET:"create ticket",
    REGISTER_COMPLAINT:"register complaint",
    SEND_OTP:"send otp",
    ACCOUNT_APPROVAL:"account approval",
    ACCOUNT_APPROVED:"account approved"
}