from flask import jsonify

def generate_error_response(message, status_code):
    """
    Create a simple error response with a custom message and HTTP status code.

    Args:
        message (str): The error message to send back to the user.
        status_code (int): The HTTP status code to include in the response.

    Returns:
        Flask response: A JSON object with the error message and status code.
    """
    return jsonify({"error": message}), status_code


def validate_required_fields(data, required_fields):
    """
    Check if all the required fields are present in the given data.

    Args:
        data (dict): The input data to check, typically from a request (e.g., request.json).
        required_fields (list): A list of required field names.

    Returns:
        tuple:
            - bool: True if all required fields are present, False otherwise.
            - str: A message listing missing fields if any are not found.
    """
    missing_fields = []  # List to store any missing fields

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # If all fields are present, return True with no message
    return True, None

