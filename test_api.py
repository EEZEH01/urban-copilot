#!/usr/bin/env python3
import requests
import json
import time
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

BASE_URL = "http://localhost:5000"  # Update this if using a different port

def print_colored(message, color=Fore.GREEN, symbol="✓"):
    """Print a colored message with a symbol prefix."""
    if color == Fore.RED:
        symbol = "✗"
    elif color == Fore.YELLOW:
        symbol = "!"
    print(f"{color}{symbol} {message}{Style.RESET_ALL}")

def test_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Test an API endpoint and return whether the test passed."""
    url = f"{BASE_URL}{endpoint}"
    print_colored(f"Testing {method} {url}", Fore.BLUE, "→")
    
    try:
        if method == "GET":
            start_time = time.time()
            response = requests.get(url, timeout=5)
            elapsed_time = time.time() - start_time
        elif method == "POST":
            start_time = time.time()
            response = requests.post(url, json=data, timeout=5)
            elapsed_time = time.time() - start_time
        else:
            print_colored(f"Unsupported method: {method}", Fore.RED)
            return False

        # Check if status code matches expected
        if response.status_code == expected_status:
            print_colored(f"Status: {response.status_code}, Time: {elapsed_time:.3f}s", Fore.GREEN)
            
            # Print response content
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                # If not JSON, print as text
                print(response.text[:200] + ("..." if len(response.text) > 200 else ""))
                
            return True
        else:
            print_colored(f"Status: {response.status_code} (expected {expected_status}), Time: {elapsed_time:.3f}s", Fore.RED)
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text[:200] + ("..." if len(response.text) > 200 else ""))
            return False
            
    except requests.exceptions.RequestException as e:
        print_colored(f"Error: {e}", Fore.RED)
        return False

def main():
    """Run API tests."""
    print_colored("Urban Copilot API Test", Fore.BLUE, "•")
    print_colored("=" * 60, Fore.BLUE, "")
    
    # Test the main UI endpoint
    print_colored("\nTesting UI:", Fore.BLUE, "•")
    success = test_endpoint("/")
    
    # Test API endpoints
    print_colored("\nTesting API endpoints:", Fore.BLUE, "•")
    
    # Test ask endpoint with valid question
    success = test_endpoint(
        "/api/ask", 
        method="POST", 
        data={"question": "What are smart cities?"}
    ) and success
    
    # Test ask endpoint with empty question (should return 400)
    success = test_endpoint(
        "/api/ask", 
        method="POST", 
        data={"question": ""}, 
        expected_status=400
    ) and success
    
    # Test ask endpoint with malformed request (missing question field)
    success = test_endpoint(
        "/api/ask", 
        method="POST", 
        data={}, 
        expected_status=400
    ) and success
    
    # Summary
    print_colored("\nTest Results:", Fore.BLUE, "•")
    if success:
        print_colored("All tests passed successfully!", Fore.GREEN)
        return 0
    else:
        print_colored("Some tests failed. See above for details.", Fore.RED)
        return 1

if __name__ == "__main__":
    sys.exit(main())
