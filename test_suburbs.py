"""
Test which suburbs work with the sandbox API
"""
import requests

API_BASE_URL = "https://www.microburbs.com.au/report_generator/api"
API_TOKEN = "test"

# Test suburbs
test_suburbs = [
    "Belmont North",
    "Adamstown",
    "Charlestown",
    "Kotara",
    "New Lambton",
    "Newcastle",
    "Mayfield",
    "Hamilton",
    "Merewether",
    "The Junction"
]

print("Testing suburbs with sandbox API...\n")
print("-" * 60)

working_suburbs = []

for suburb in test_suburbs:
    try:
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{API_BASE_URL}/suburb/properties',
            params={'suburb': suburb},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else 0
            print(f"✓ {suburb:<20} - Working! ({count} properties)")
            working_suburbs.append(suburb)
        else:
            print(f"✗ {suburb:<20} - Failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"✗ {suburb:<20} - Error: {str(e)[:40]}")

print("-" * 60)
print(f"\nWorking suburbs: {len(working_suburbs)}/{len(test_suburbs)}")
if working_suburbs:
    print("\nList of working suburbs:")
    for suburb in working_suburbs:
        print(f"  - {suburb}")
