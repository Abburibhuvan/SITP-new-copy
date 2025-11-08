import requests
import json

# Brevo API configuration
import os
API_KEY = os.getenv('BREVO_API_KEY')
if not API_KEY:
    print("ERROR: BREVO_API_KEY environment variable not set")
    exit(1)
API_URL = 'https://api.brevo.com/v3/smtp/email'

# Email details
email_data = {
    "sender": {
        "name": "Test Sender",
        "email": "testcasemail019@gmail.com"
    },
    "to": [{"email": "122311510119@apollouniversity.edu.in"}],
    "subject": "Test Email from Brevo API - Simple Test",
    "htmlContent": "<h1>Test Email</h1><p>This is a test email sent via the Brevo API.</p>"
}

# Headers
headers = {
    'accept': 'application/json',
    'api-key': API_KEY,
    'content-type': 'application/json'
}

print("Sending test email...")
try:
    response = requests.post(API_URL, headers=headers, json=email_data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    
    # Check if the email was sent successfully
    if response.status_code == 201:
        print("\nEmail sent successfully!")
    else:
        print(f"\nFailed to send email. Status code: {response.status_code}")
        
except Exception as e:
    print(f"\nError occurred: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response content: {e.response.text}")
