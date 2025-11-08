import os
import requests
import json

# Get the API key from environment variable
api_key = os.getenv('BREVO_API_KEY')
if not api_key:
    print("ERROR: BREVO_API_KEY environment variable not set")
    exit(1)

# Mask the API key for security
api_key_display = f"{api_key[:8]}...{api_key[-4:] if api_key else ''}" if api_key else "[NOT SET]"
print(f"Using API key: {api_key_display}")

# Test API key by getting account information
try:
    print("\nTesting Brevo API key by fetching account information...")
    headers = {
        'accept': 'application/json',
        'api-key': api_key
    }
    
    # Test 1: Get account information
    response = requests.get('https://api.brevo.com/v3/account', headers=headers)
    print(f"\nAccount Info - Status Code: {response.status_code}")
    print("Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    
    # Test 2: Send a test email
    print("\nSending test email...")
    email_data = {
        "sender": {
            "name": "Test Sender",
            "email": "testcasemail019@gmail.com"
        },
        "to": [{"email": "122311510119@apollouniversity.edu.in"}],
        "subject": "Test Email from Brevo API",
        "htmlContent": "<h1>Test Email</h1><p>This is a test email sent via the Brevo API.</p>"
    }
    
    response = requests.post(
        'https://api.brevo.com/v3/smtp/email',
        headers=headers,
        json=email_data
    )
    
    print(f"\nSend Email - Status Code: {response.status_code}")
    print("Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    
except Exception as e:
    print(f"\nError: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response content: {e.response.text}")
