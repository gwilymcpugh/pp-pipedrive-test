
# Pipedrive API configuration
PIPEDRIVE_API_TOKEN = '5e74823582b2b2a0a7ca1f6ec5d278a5cc320823'
PIPEDRIVE_API_URL = 'https://api.pipedrive.com/v1/'

# Field mappings from form to Pipedrive
FIELD_MAPPINGS = {
    'organization': {
        'name': 'name',
        'industry': '720380dd0ab1f274fff94d3dfc6ce321e147aeeb',
        'number_of_employees': 'f812c78bcabb652b2345ccbef5bba1e8692a9d5d',
        'current_insurer': '5ad7b7abc8fc49c19e1d8944d95a2f3203555b7c',
        'current_products': '3c61382178e930ca247b7446ef2afecd7a588999',
        'interests': '2152db888ef0c548b6365671b649068ee286ed00'
    },
    'contact': {
        'name': 'name',
        'email': 'email',
        'org_id': 'org_id'
    }
}

# Employee number mapping from dropdown to actual values
EMPLOYEE_NUMBER_MAPPING = {
    '1-10': 10,
    '11-50': 50,
    '51-100': 100,
    '101-250': 250,
    '251-500': 500,
    '501+': 1000
}
