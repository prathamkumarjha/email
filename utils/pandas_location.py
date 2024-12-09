import threading
from .logger import app_logger
import pandas as pd
import requests
import json
import os
PUBLIC_FOLDER = "public/"
AIRPORT_CODES_FILE = f"{PUBLIC_FOLDER}locations/airport_codes.json"
AIRLINE_CODES_FILE = f"{PUBLIC_FOLDER}airlines/airline_codes.json"

def fetch_and_save_airports_data(output_file=AIRPORT_CODES_FILE):
    try:
        url = "https://raw.githubusercontent.com/mwgg/Airports/master/airports.json"
        # Fetch data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Process data to include only the specified headers
        processed_data = []
        for key, value in data.items():
            processed_entry = {
                "iata": value.get("iata", ""),
                "name": value.get("name", ""),
                "city": value.get("city", ""),
                "country": value.get("country", ""),
                "lat": value.get("lat", ""),
                "lon": value.get("lon", ""),
                "tz": value.get("tz", ""),
            }
            processed_data.append(processed_entry)

        # Save processed data to a local JSON file
        folder_path = os.path.dirname(output_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(output_file, "w") as f:
            json.dump(processed_data, f, indent=4)

        app_logger.info(f"Data successfully saved to {output_file}")

    except requests.RequestException as e:
        app_logger.error(f"Error fetching data: {e}")
    except Exception as e:
        app_logger.error(f"Error processing or saving data: {e}")


def fetch_and_save_airlines_data(output_file=AIRLINE_CODES_FILE):
    try:
        # Fetch data from the URL
        url = (
            "https://raw.githubusercontent.com/npow/airline-codes/master/airlines.json"
        )
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Process data to include only the specified headers
        processed_data = []
        for entry in data:
            processed_entry = {
                "iata": entry.get("iata", ""),
                "name": entry.get("name", ""),
                "country": entry.get("country", ""),
            }
            processed_data.append(processed_entry)

        # Save processed data to a local JSON file
        folder_path = os.path.dirname(output_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(output_file, "w") as f:
            json.dump(processed_data, f, indent=4)

        app_logger.info(f"Data successfully saved to {output_file}")

    except requests.RequestException as e:
        app_logger.error(f"Error fetching data: {e}")
    except Exception as e:
        app_logger.error(f"Error processing or saving data: {e}")


class LocationData:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LocationData, cls).__new__(cls)
                    cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, json_file):
        if not os.path.isfile(json_file):
            fetch_and_save_airports_data(json_file)
        self.df = pd.read_json(json_file)
        self.df = self.df[self.df["iata"].notnull()]  # Filter records with non-null iata values
        self.df.set_index("iata", inplace=True)

    @staticmethod
    def get_instance(json_file=AIRPORT_CODES_FILE):
        if LocationData._instance is None:
            LocationData(json_file)
        return LocationData._instance

    def get_location_by_iata(self, iata):
        try:
            location = self.df.loc[iata].to_dict()
            return location
        except KeyError:
            return None
        
    def get_location_airport_by_iata(self, iata):
        try:
            result = self.df.loc[iata]
            if isinstance(result, pd.Series):
                # Convert Series to dictionary
                location = result.to_dict()
            else:
                # Convert DataFrame to list of dictionaries
                location = result.to_dict(orient='records')[-1]  # Get the last record
            return location["name"]
        except KeyError:
            return None

    def get_location_timezone_by_iata(self, iata):
        try:
            result = self.df.loc[iata]
            if isinstance(result, pd.Series):
                # Convert Series to dictionary
                location = result.to_dict()
            else:
                # Convert DataFrame to list of dictionaries
                location = result.to_dict(orient='records')[-1]  # Get the last record
            return location["tz"]
        except KeyError:
            return None
        
    def get_location_name_by_iata(self, iata):
        try:
            result = self.df.loc[iata]
            if isinstance(result, pd.Series):
                # Convert Series to dictionary
                location = result.to_dict()
            else:
                # Convert DataFrame to list of dictionaries
                location = result.to_dict(orient='records')[-1]  # Get the last record
            return location["city"]
        except KeyError:
            return None

class AirlineData:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AirlineData, cls).__new__(cls)
                    cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, json_file):
        if not os.path.isfile(json_file):
            fetch_and_save_airlines_data(json_file)
        self.df = pd.read_json(json_file)
        self.df.set_index("iata", inplace=True)

    @staticmethod
    def get_instance(json_file=AIRLINE_CODES_FILE):
        if AirlineData._instance is None:
            AirlineData(json_file)
        return AirlineData._instance

    def get_airline_by_iata(self, iata):
        try:
            airline = self.df.loc[iata].to_dict()
            return airline
        except KeyError:
            return None

    def get_airline_name_by_iata(self, iata):
        try:
            result = self.df.loc[iata]
            if isinstance(result, pd.Series):
                # Convert Series to dictionary
                airline = result.to_dict()
            else:
                # Convert DataFrame to list of dictionaries
                airline = result.to_dict(orient='records')[-1]  # Get the last record
            return airline["name"]
        except KeyError:
            return None