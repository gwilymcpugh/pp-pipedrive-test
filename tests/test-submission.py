from src.FormHandler import FormHandler

def test_form_submission():
    # Test data
    form_data = {
        'name': 'John Doe',  # Contact name
       'company_name': 'Test Company Ltd',  # Organization name
        'email': 'contact@testcompany.com',
        'industry': 'Technology',
        'number_of_employees': '11-50',
        'Current Commercial Insurer': 'AIG',  # Updated field name
        'Which insurance products do you currently have?': 'Public Liability Insurance',  # Updated field name
        'interests': 'Direct environmental impact through policies'
    }

    # Initialize handler
    handler = FormHandler()

    # Process submission
    result = handler.handle_submission(form_data)

    # Print results
    print("Submission Result:")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Organization ID: {result['organization']['id']}")
        print(f"Contact ID: {result['contact']['id']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_form_submission()