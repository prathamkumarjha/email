import requests
import random
import string
import hashlib


def request_helper(method, payload, headers=None):
    try:
        response = requests.post(method, json=payload, headers=headers)
        if response.status_code == 200:
            raw_response = response.json()
            return raw_response
        else:
            error_message = str(response.text)
            raise Exception(error_message)
    except Exception as e:
        raise Exception(e)


def random_string_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def hash_string(input_string, length=None):
    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes of the string
    sha256.update(input_string.encode("utf-8"))

    # Get the hexadecimal representation of the hash
    full_hash = sha256.hexdigest()
    if length:
        # Truncate the hash to the desired length (50 characters)
        truncated_hash = full_hash[:length]
        return truncated_hash
    else:
        return full_hash
