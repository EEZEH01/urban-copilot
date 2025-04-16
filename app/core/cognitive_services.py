"""
Azure Cognitive Services integration for Urban Copilot
This module provides an interface to Azure Cognitive Services
for natural language processing capabilities.
"""

import os
import requests
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class CognitiveServicesClient:
    """Client for interacting with Azure Cognitive Services"""
    
    def __init__(self, api_key=None, endpoint=None):
        """
        Initialize the Azure Cognitive Services client
        
        Args:
            api_key: The Azure Cognitive Services API key
            endpoint: The Azure Cognitive Services endpoint URL
        """
        # Use parameters or fall back to environment variables
        self.api_key = api_key or os.environ.get('AZURE_API_KEY')
        self.endpoint = endpoint or os.environ.get('AZURE_ENDPOINT')
        
        if not self.api_key or not self.endpoint:
            logger.warning("Azure Cognitive Services credentials not configured")
        else:
            logger.info(f"Azure Cognitive Services client initialized with endpoint: {self.endpoint}")
            
    def is_available(self) -> str:
        """
        Check if the Azure Cognitive Services API is available
        
        Returns:
            str: "up" if the service is available, "down" if not
        """
        if not self.api_key or not self.endpoint:
            return "down"
            
        try:
            # Simple ping to the API
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            response = requests.get(
                f"{self.endpoint}/text/analytics/v3.1/languages",
                headers=headers,
                timeout=5
            )
            
            # Check if we got a valid response
            if response.status_code < 400:
                return "up"
            else:
                logger.warning(f"Azure Cognitive Services returned status code: {response.status_code}")
                return "down"
        except Exception as e:
            logger.error(f"Error checking Azure Cognitive Services availability: {e}")
            return "down"

    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of the provided text
        
        Args:
            text: The text to analyze
            
        Returns:
            A tuple containing (language_name, confidence_score)
        """
        if not self.api_key or not self.endpoint:
            logger.warning("Azure Cognitive Services not configured, skipping language detection")
            return ("en", 1.0)  # Default to English
            
        try:
            # Construct the request
            url = f"{self.endpoint}text/analytics/v3.1/languages"
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            data = {
                "documents": [
                    {
                        "id": "1",
                        "text": text
                    }
                ]
            }
            
            # Send the request
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Process the response
            result = response.json()
            detected_language = result['documents'][0]['detectedLanguage']
            
            logger.debug(f"Detected language: {detected_language['name']} with confidence {detected_language['confidenceScore']}")
            return (detected_language['name'], detected_language['confidenceScore'])
            
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            return ("en", 0.0)  # Default to English with zero confidence on error

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze the sentiment of the provided text
        
        Args:
            text: The text to analyze
            
        Returns:
            A tuple containing (sentiment, confidence_score)
            sentiment is one of: positive, neutral, negative
        """
        if not self.api_key or not self.endpoint:
            logger.warning("Azure Cognitive Services not configured, skipping sentiment analysis")
            return ("neutral", 0.5)  # Default to neutral
            
        try:
            # Construct the request
            url = f"{self.endpoint}text/analytics/v3.1/sentiment"
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            data = {
                "documents": [
                    {
                        "id": "1",
                        "text": text
                    }
                ]
            }
            
            # Send the request
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Process the response
            result = response.json()
            document = result['documents'][0]
            sentiment = document['sentiment']
            score = max(document['confidenceScores'][sentiment], 0.5)  # Use the confidence of the detected sentiment
            
            logger.debug(f"Detected sentiment: {sentiment} with confidence {score}")
            return (sentiment, score)
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return ("neutral", 0.5)  # Default to neutral on error
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases from the provided text
        
        Args:
            text: The text to analyze
            
        Returns:
            A list of key phrases
        """
        if not self.api_key or not self.endpoint:
            logger.warning("Azure Cognitive Services not configured, skipping key phrase extraction")
            return [text]  # Return the original text as a single phrase
            
        try:
            # Construct the request
            url = f"{self.endpoint}text/analytics/v3.1/keyPhrases"
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            data = {
                "documents": [
                    {
                        "id": "1",
                        "text": text
                    }
                ]
            }
            
            # Send the request
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Process the response
            result = response.json()
            key_phrases = result['documents'][0]['keyPhrases']
            
            logger.debug(f"Extracted key phrases: {key_phrases}")
            return key_phrases
            
        except Exception as e:
            logger.error(f"Error extracting key phrases: {str(e)}")
            return [text]  # Return the original text on error
