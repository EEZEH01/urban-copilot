#!/usr/bin/env python3
"""
Test Azure Cognitive Services connection for Urban Copilot
This script tests if the application can successfully connect to 
the Azure Cognitive Services resource.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

def test_text_analytics(api_key, endpoint):
    """Test connection to Azure Text Analytics service"""
    print("Testing connection to Azure Text Analytics service...")
    
    # Construct the request URL
    url = f"{endpoint}text/analytics/v3.1/languages"
    
    # Request headers
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Request body
    data = {
        "documents": [
            {
                "id": "1",
                "text": "Smart cities leverage technology to optimize infrastructure and improve quality of life."
            }
        ]
    }
    
    try:
        # Make the request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # Parse the result
        result = response.json()
        
        print("✅ Successfully connected to Azure Cognitive Services!")
        print(f"Detected language: {result['documents'][0]['detectedLanguage']['name']}")
        print(f"Confidence score: {result['documents'][0]['detectedLanguage']['confidenceScore']:.4f}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
        print(f"Response: {response.text}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    # Load environment variables
    load_dotenv()
    
    # Get Azure Cognitive Services credentials
    api_key = os.environ.get("AZURE_API_KEY")
    endpoint = os.environ.get("AZURE_ENDPOINT")
    
    if not api_key or not endpoint:
        print("❌ Azure Cognitive Services credentials not found in environment variables.")
        print("Please set AZURE_API_KEY and AZURE_ENDPOINT in your .env file.")
        return 1
    
    # Test connection
    success = test_text_analytics(api_key, endpoint)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
