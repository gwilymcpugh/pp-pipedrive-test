import requests
from typing import Dict, Any, Optional
from config.config import PIPEDRIVE_API_TOKEN, PIPEDRIVE_API_URL, FIELD_MAPPINGS, EMPLOYEE_NUMBER_MAPPING

class PipedriveClient:
    """
    Client for interacting with the Pipedrive API.
    Handles creation of organizations and contacts, with appropriate field mapping.
    """
    def __init__(self):
        self.api_token = PIPEDRIVE_API_TOKEN
        self.base_url = PIPEDRIVE_API_URL
        self.session = requests.Session()
        self.session.params = {'api_token': self.api_token}