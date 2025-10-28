"""
Test script for MicroBurbs Property Dashboard
Run this to verify all functionality works correctly
"""

import requests
import json
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_SUBURBS = ["Belmont North", "Sydney", "InvalidSuburb123"]

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text.center(60)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

def test_server_running():
    """Test if the Flask server is running"""
    print_header("Testing Server Connection")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print_success("Server is running")
            print_info(f"Status Code: {response.status_code}")
            return True
        else:
            print_error(f"Server returned unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is it running?")
        print_info("Start the server with: python app.py")
        return False
    except Exception as e:
        print_error(f"Error connecting to server: {str(e)}")
        return False

def test_api_endpoint(suburb, should_succeed=True):
    """Test the API endpoint with a given suburb"""
    print(f"\n{Fore.BLUE}Testing suburb: {suburb}{Style.RESET_ALL}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/properties",
            params={"suburb": suburb},
            timeout=30
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print_success("API request successful")
                
                # Check data structure
                if 'data' in data:
                    properties = data['data']
                    print_info(f"Properties found: {len(properties)}")
                    
                    if len(properties) > 0:
                        print_success("Property data retrieved")
                        
                        # Display first property sample
                        first_prop = properties[0]
                        print_info(f"Sample property keys: {list(first_prop.keys())[:5]}")
                    else:
                        print_info("No properties found for this suburb")
                
                # Check statistics
                if 'statistics' in data:
                    stats = data['statistics']
                    print_success("Statistics calculated")
                    print_info(f"Total: {stats.get('total', 0)}")
                    print_info(f"Avg Price: ${stats.get('average_price', 0):,.0f}")
                    print_info(f"Avg Bedrooms: {stats.get('average_bedrooms', 0)}")
                
                return True
            else:
                if should_succeed:
                    print_error("API returned success=False")
                else:
                    print_success("Expected failure occurred")
                return not should_succeed
        else:
            if should_succeed:
                print_error(f"Unexpected status code: {response.status_code}")
            else:
                print_success("Expected error status code")
            return not should_succeed
            
    except requests.exceptions.Timeout:
        print_error("Request timed out")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_api_without_suburb():
    """Test API endpoint without required suburb parameter"""
    print(f"\n{Fore.BLUE}Testing API without suburb parameter{Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/properties", timeout=5)
        
        if response.status_code == 400:
            print_success("Correctly returned 400 for missing parameter")
            return True
        else:
            print_error(f"Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_static_files():
    """Test if static files are accessible"""
    print_header("Testing Static Files")
    
    files = [
        "/static/app.js",
        "/static/styles.css"
    ]
    
    all_passed = True
    
    for file_path in files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}", timeout=5)
            if response.status_code == 200:
                print_success(f"{file_path} is accessible")
                print_info(f"Size: {len(response.content)} bytes")
            else:
                print_error(f"{file_path} returned {response.status_code}")
                all_passed = False
        except Exception as e:
            print_error(f"Error accessing {file_path}: {str(e)}")
            all_passed = False
    
    return all_passed

def run_all_tests():
    """Run all tests"""
    print_header("MicroBurbs Property Dashboard - Test Suite")
    print_info("This will test all functionality of the application")
    
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Test 1: Server running
    if test_server_running():
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("\nServer not running. Stopping tests.")
        return
    
    # Test 2: Static files
    if test_static_files():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 3: Valid suburbs
    print_header("Testing Valid Suburbs")
    for suburb in TEST_SUBURBS[:2]:  # First two are valid
        if test_api_endpoint(suburb, should_succeed=True):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Test 4: Invalid suburb (should still work, just no results)
    print_header("Testing Invalid Suburb")
    if test_api_endpoint(TEST_SUBURBS[2], should_succeed=True):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 5: Missing parameter
    if test_api_without_suburb():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Print summary
    print_header("Test Summary")
    print(f"{Fore.GREEN}Passed: {results['passed']}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {results['failed']}{Style.RESET_ALL}")
    
    total = results['passed'] + results['failed']
    percentage = (results['passed'] / total * 100) if total > 0 else 0
    print(f"\n{Fore.CYAN}Success Rate: {percentage:.1f}%{Style.RESET_ALL}")
    
    if results['failed'] == 0:
        print(f"\n{Fore.GREEN}{'🎉 All tests passed! 🎉'.center(60)}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}{'⚠ Some tests failed. Check output above.'.center(60)}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Tests interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n\n{Fore.RED}Unexpected error: {str(e)}{Style.RESET_ALL}")
