from django.conf import settings
from datetime import timedelta, datetime
from django import template
from urllib import parse
import pytz
from django.utils import timezone


from django.core.serializers import serialize

from collections import Counter
# from utils.pandas_location import LocationData, AirlineData


# location_data = LocationData.get_instance()
# airline_data = AirlineData.get_instance()


register = template.Library()


@register.filter(name="convert_time_str")
def convert_time_str(timestamp, format):
    try:
        time = datetime.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
        time = time
        return time.strftime(format)
    except BaseException:
        return "NULL"


@register.filter(name="get_flight_summary")
def get_flight_summary(flight_details):
    start_time = convert_time_str(flight_details.get("departureTime"), " %a %d %b %Y")
    stops = (
        "Non-stop"
        if len(flight_details.get("segments")) == 1
        else f"{len(flight_details.get('segments'))} Stops"
    )
    return f"{start_time} • {stops} • 1h 35m duration"


# @register.filter(name="get_location_name")
# def get_location_name(location_code):
#     return location_data.get_location_name_by_iata(location_code)