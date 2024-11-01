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

    def create_organization(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create an organization in Pipedrive with the given data.
        
        Args:
            data: Dictionary containing organization data from the form
            
        Returns:
            Dictionary containing the created organization data or None if creation failed
        """
        try:
            # Map the form data to Pipedrive fields
            payload = {
                'name': data.get('name', ''),
                str(FIELD_MAPPINGS['organization']['industry']): data.get('industry', ''),
                str(FIELD_MAPPINGS['organization']['current_insurer']): data.get('current_insurer', ''),
                str(FIELD_MAPPINGS['organization']['current_products']): data.get('current_products', ''),
                str(FIELD_MAPPINGS['organization']['interests']): data.get('interests', '')
            }

            # Handle employee number mapping
            emp_number = data.get('number_of_employees', '')
            if emp_number in EMPLOYEE_NUMBER_MAPPING:
                payload[str(FIELD_MAPPINGS['organization']['number_of_employees'])] = EMPLOYEE_NUMBER_MAPPING[emp_number]

            # Make the API request
            response = self.session.post(
                f"{self.base_url}organizations",
                json=payload
            )
            response.raise_for_status()
            
            return response.json().get('data')
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating organization: {e}")
            return None