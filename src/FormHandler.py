from typing import Dict, Any
from .PipedriveClient import PipedriveClient

class FormHandler:
    """Handles form submissions and validation"""
    
    def __init__(self):
        self.pipedrive = PipedriveClient()

    def validate_form_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates required fields in form data
        """
        errors = {}
        required_fields = ['name', 'company_name', 'email', 'industry', 'number_of_employees']  # Added company_name
        
        for field in required_fields:
            if not form_data.get(field):
                errors[field] = f"{field} is required"

        if 'email' in form_data and '@' not in form_data['email']:
            errors['email'] = "Invalid email format"

        return errors

    def handle_submission(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and processes form submission
        """
        # Validate form data
        errors = self.validate_form_data(form_data)
        if errors:
            return {
                'success': False,
                'errors': errors
            }

        # Process submission via PipedriveClient
        result = self.pipedrive.process_form_submission(form_data)
        return result