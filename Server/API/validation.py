from werkzeug.exceptions import HTTPException
from flask import make_response
import json

class UserError(HTTPException):
    def __init__(self, status_code, error_code, error_description):
        message = {"error_code": error_code, "error_description": error_description}
        self.response = make_response(json.dumps(message), status_code)
        
class PropertyExistError(HTTPException):
    def __init__(self,message, status_code):
        self.response = make_response(message, status_code)       


class TheatreError(HTTPException):
    def __init__(self, status_code, error_code, error_description):
        message = {"error_code": error_code, "error_description": error_description}
        self.response = make_response(json.dumps(message), status_code)         