import requests
from typing import Dict, Any, Optional
from config.config import PIPEDRIVE_API_TOKEN, PIPEDRIVE_API_URL, FIELD_MAPPINGS, EMPLOYEE_NUMBER_MAPPING
from config.valid_insurers import VALID_INSURERS  # Add this import

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
            current_insurer = data.get('Current Commercial Insurer', '')
            # Map the form data to Pipedrive fields
            payload = {
                'name': data.get('company_name', ''),  # Changed from 'name' to 'company_name'
                str(FIELD_MAPPINGS['organization']['industry']): data.get('industry', ''),
                str(FIELD_MAPPINGS['organization']['current_products']): data.get('Which insurance products do you currently have?', ''),  # Updated field name
                str(FIELD_MAPPINGS['organization']['interests']): data.get('interests', '')
            }

            # Handle employee number mapping
            emp_number = data.get('number_of_employees', '')
            if emp_number in EMPLOYEE_NUMBER_MAPPING:
                payload[str(FIELD_MAPPINGS['organization']['number_of_employees'])] = EMPLOYEE_NUMBER_MAPPING[emp_number]

             # Handle current insurer field
            insurer_field = str(FIELD_MAPPINGS['organization']['current_insurer'])
            if current_insurer in VALID_INSURERS:
                payload[insurer_field] = current_insurer
            else:
                payload[insurer_field] = "Other"
            
            # Create organization
            response = self.session.post(
                f"{self.base_url}organizations",
                json=payload
            )
            response.raise_for_status()
            org_data = response.json().get('data')
            
            # If we used "Other" for insurer, add a note
            if org_data and current_insurer not in VALID_INSURERS:
                note_content = f"Other was selected for Current Insurer because the user input '{current_insurer}', which isn't currently in the list"
                self.create_note(org_data['id'], note_content)
            
            return org_data
                
        except requests.exceptions.RequestException as e:
            print(f"Error creating organization: {e}")
            return None

    def create_note(self, org_id: int, content: str) -> Optional[Dict[str, Any]]:
        """
        Create a note attached to an organization in Pipedrive.
        
        Args:
            org_id: The ID of the organization to attach the note to
            content: The content of the note
            
        Returns:
            Dictionary containing the created note data or None if creation failed
        """
        try:
            payload = {
                'content': content,
                'org_id': org_id,
                'pinned_to_organization_flag': 1
            }
            
            response = self.session.post(
                f"{self.base_url}notes",
                json=payload
            )
            print(f"Note creation response: {response.text}")  # Debug line
            response.raise_for_status()
            
            return response.json().get('data')
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating note: {e}")
            return None

    def create_contact(self, data: Dict[str, Any], org_id: int = None) -> Optional[Dict[str, Any]]:
        """
        Create a contact in Pipedrive and optionally associate with an organization.
        
        Args:
            data: Dictionary containing contact data from the form
            org_id: Optional organization ID to associate the contact with
            
        Returns:
            Dictionary containing the created contact data or None if creation failed
        """
        try:
            # Map the form data to Pipedrive fields
            payload = {
                'name': data.get('name', ''),
                'email': [{'value': data.get('email', ''), 'primary': True}]
            }

            # Associate with organization if org_id is provided
            if org_id:
                payload['org_id'] = org_id

            # Make the API request
            response = self.session.post(
                f"{self.base_url}persons",
                json=payload
            )
            response.raise_for_status()
            
            return response.json().get('data')
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating contact: {e}")
            return None

    def process_form_submission(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a form submission by creating both organization and contact.
        
        Args:
            form_data: Dictionary containing all form data
            
        Returns:
            Dictionary containing results of both creation operations
        """
        result = {
            'success': False,
            'organization': None,
            'contact': None,
            'error': None
        }

        try:
            # First create the organization
            org = self.create_organization(form_data)
            if not org:
                raise Exception("Failed to create organization")
            result['organization'] = org

            # Then create the contact and associate with the organization
            contact = self.create_contact(form_data, org.get('id'))
            if not contact:
                raise Exception("Failed to create contact")
            result['contact'] = contact

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)

        return result