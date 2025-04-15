#!/usr/bin/env python3
import requests
import time
import concurrent.futures
import argparse
import statistics
import json
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

# Default settings
BASE_URL = "http://localhost:5000"
DEFAULT_ENDPOINT = "/api/ask"
DEFAULT_METHOD = "POST"
DEFAULT_NUM_REQUESTS = 50
DEFAULT_CONCURRENCY = 10
DEFAULT_DATA = {"question": "What are smart cities?"}

def print_header(message):
    """Print a header with box drawing characters."""
    width = len(message) + 4
    print(f"╔{'═' * width}╗")
    print(f"║  {message}  ║")
    print(f"╚{'═' * width}╝")
    
def print_colored(message, color=Fore.GREEN, prefix=""):
    """Print a colored message with optional prefix."""
    print(f"{color}{prefix}{message}{Style.RESET_ALL}")

def make_request(endpoint, method="POST", data=None, request_num=0):
    """Make a single request to the API and return performance metrics."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        else:
            return {
                "request_num": request_num,
                "success": False,
                "error": f"Unsupported method: {method}"
            }
        
        elapsed_time = time.time() - start_time
        
        return {
            "request_num": request_num,
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "elapsed_time": elapsed_time,
            "response_size": len(response.content)
        }
    except Exception as e:
        return {
            "request_num": request_num,
            "success": False,
            "error": str(e)
        }

def run_load_test(endpoint, method, data, num_requests, concurrency):
    """Run a load test with specified parameters."""
    print_header("URBAN COPILOT LOAD TEST")
    print_colored(f"Target: {method} {BASE_URL}{endpoint}", Fore.BLUE)
    print_colored(f"Requests: {num_requests}, Concurrency: {concurrency}", Fore.BLUE)
    print_colored(f"Request data: {json.dumps(data)}\n", Fore.BLUE)
    
    results = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit all requests
        futures = [
            executor.submit(make_request, endpoint, method, data, i)
            for i in range(num_requests)
        ]
        
        # Process results as they complete
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            results.append(result)
            
            # Print progress every 10% of requests
            if (i + 1) % max(1, num_requests // 10) == 0:
                print_colored(f"Completed {i + 1}/{num_requests} requests " +
                             f"({(i + 1) / num_requests * 100:.1f}%)", 
                             Fore.YELLOW)
    
    total_time = time.time() - start_time
    
    # Analyze and print results
    print_results(results, total_time)

def print_results(results, total_time):
    """Analyze and print load test results."""
    successful_results = [r for r in results if r.get("success", False)]
    failed_results = [r for r in results if not r.get("success", False)]
    
    print_header("RESULTS")
    print_colored(f"Total requests: {len(results)}", Fore.BLUE)
    print_colored(f"Successful: {len(successful_results)} " +
                 f"({len(successful_results) / len(results) * 100:.1f}%)", 
                 Fore.GREEN if len(successful_results) == len(results) else Fore.YELLOW)
    
    if failed_results:
        print_colored(f"Failed: {len(failed_results)} " +
                     f"({len(failed_results) / len(results) * 100:.1f}%)", 
                     Fore.RED)
        
        # Group failures by error or status code
        failure_types = {}
        for result in failed_results:
            if "error" in result:
                key = str(result["error"])
            else:
                key = f"Status {result['status_code']}"
                
            if key not in failure_types:
                failure_types[key] = 0
            failure_types[key] += 1
        
        print_colored("\nFailure breakdown:", Fore.RED)
        for error, count in failure_types.items():
            print_colored(f"  - {error}: {count} requests", Fore.RED)
    
    # Performance statistics for successful requests
    if successful_results:
        response_times = [r["elapsed_time"] for r in successful_results]
        
        print_colored("\nPerformance metrics:", Fore.BLUE)
        print(f"  Total test duration: {total_time:.2f} seconds")
        print(f"  Requests per second: {len(successful_results) / total_time:.2f}")
        print(f"  Average response time: {statistics.mean(response_times):.3f} seconds")
        print(f"  Median response time: {statistics.median(response_times):.3f} seconds")
        print(f"  Min response time: {min(response_times):.3f} seconds")
        print(f"  Max response time: {max(response_times):.3f} seconds")
        
        # Calculate percentiles
        percentiles = [50, 90, 95, 99]
        sorted_times = sorted(response_times)
        print("\nResponse time percentiles:")
        for p in percentiles:
            index = int(len(sorted_times) * p / 100)
            print(f"  {p}th percentile: {sorted_times[index]:.3f} seconds")

def main():
    """Parse arguments and run load test."""
    parser = argparse.ArgumentParser(description="Load testing tool for Urban Copilot API")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, 
                        help=f"API endpoint to test (default: {DEFAULT_ENDPOINT})")
    parser.add_argument("--method", default=DEFAULT_METHOD, choices=["GET", "POST"],
                        help=f"HTTP method (default: {DEFAULT_METHOD})")
    parser.add_argument("--requests", type=int, default=DEFAULT_NUM_REQUESTS,
                        help=f"Number of requests to send (default: {DEFAULT_NUM_REQUESTS})")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY,
                        help=f"Number of concurrent requests (default: {DEFAULT_CONCURRENCY})")
    parser.add_argument("--data", type=str, default=json.dumps(DEFAULT_DATA),
                        help="JSON data to send with POST requests")
    
    args = parser.parse_args()
    
    # Parse JSON data
    try:
        data = json.loads(args.data)
    except json.JSONDecodeError:
        print_colored(f"Error: Invalid JSON data: {args.data}", Fore.RED)
        return 1
    
    run_load_test(args.endpoint, args.method, data, args.requests, args.concurrency)
    return 0

if __name__ == "__main__":
    main()
