# app/agents/urban_agent.py
from app.core.agent_base import AgentBase
from app.core.cognitive_services import CognitiveServicesClient
import logging
from typing import List

class UrbanAgent(AgentBase):
    """
    A specific agent for urban-related questions. Inherits from AgentBase and implements
    the 'run' method to provide specific responses related to urban topics.
    """
    def __init__(self):
        """
        Initialize the agent. You can load data, models, or any setup here if needed.
        """
        super().__init__()  # Call the parent constructor to ensure proper initialization
        self.logger = logging.getLogger(__name__)  # Set up logging for debugging and tracking
        self.cognitive_client = CognitiveServicesClient()  # Initialize the Azure Cognitive Services client

    def run(self, question: str) -> str:
        """
        Implement the logic for handling a question related to urban topics.

        Parameters:
        - question (str): The question to be answered by the agent.

        Returns:
        - str: The response to the question.
        """
        try:
            # Example logic: UrbanAgent returns a dynamic response based on the question
            if not question:
                raise ValueError("Question cannot be empty")

            # Placeholder for potential complex logic (e.g., API calls, database queries)
            response = self.process_urban_question(question)

            # Log the response for debugging purposes
            self.logger.info(f"Answering question: {question} with response: {response}")
            return response

        except ValueError as e:
            # Log and handle known exceptions
            self.logger.error(f"Error: {str(e)}")
            return f"Error: {str(e)}"

        except Exception as e:
            # Log and handle unexpected exceptions
            self.logger.error(f"Unexpected error: {str(e)}")
            return "Sorry, there was an issue processing your request."

    def process_urban_question(self, question: str) -> str:
        """
        Process urban-related questions using Azure Cognitive Services for enhanced responses.

        Parameters:
        - question (str): The urban-related question to process.

        Returns:
        - str: A dynamic response based on the question and AI analysis.
        """
        # Use Azure Cognitive Services to analyze the question
        try:
            # Detect language of the question
            language, language_confidence = self.cognitive_client.detect_language(question)
            if language != "English" and language_confidence > 0.8:
                self.logger.info(f"Detected non-English question in {language}")
                # We could add translation here in the future
            
            # Extract key phrases to better understand the question's focus
            key_phrases = self.cognitive_client.extract_key_phrases(question)
            self.logger.info(f"Extracted key phrases: {key_phrases}")
            
            # Analyze sentiment to gauge user's emotional context
            sentiment, sentiment_score = self.cognitive_client.analyze_sentiment(question)
            self.logger.info(f"Detected sentiment: {sentiment} with score {sentiment_score}")
            
            # Enhanced response logic using AI insights
            response = self.generate_enhanced_response(question, key_phrases, sentiment)
            return response
            
        except Exception as e:
            self.logger.error(f"Error using Cognitive Services: {str(e)}")
            
            # Fall back to basic response logic if AI analysis fails
            if "traffic" in question.lower():
                return "Traffic is heavy in downtown today."
            elif "weather" in question.lower():
                return "The weather today is sunny with a high of 25°C."
            else:
                return f"Urban Copilot Response to: {question}"
                
    def generate_enhanced_response(self, question: str, key_phrases: List[str], sentiment: str) -> str:
        """
        Generate an enhanced response using AI insights from cognitive services
        
        Parameters:
        - question (str): The original question
        - key_phrases (List[str]): Extracted key phrases from the question
        - sentiment (str): Detected sentiment of the question
        
        Returns:
        - str: An enhanced response tailored to the question context
        """
        # Example implementation - in production, this could use more advanced NLP or LLM
        topic_responses = {
            "traffic": "The current traffic conditions show moderate congestion in the city center. Consider using public transit or alternative routes.",
            "parking": "There are several parking spots available in the downtown area. You can use the city's parking app to find and reserve a spot.",
            "weather": "The current weather is mild with a chance of light showers in the evening. It's a good day for outdoor activities with proper preparation.",
            "event": "There are several city events happening this weekend including a farmers market, art exhibition, and community cleanup.",
            "public transit": "The public transit system is operating normally with minor delays on the blue line due to scheduled maintenance.",
        }
        
        # Check if any key phrases match our topics
        for phrase in key_phrases:
            phrase_lower = phrase.lower()
            for topic, response in topic_responses.items():
                if topic in phrase_lower:
                    return response
        
        # If no specific topic is matched, provide a general response
        if sentiment == "negative":
            return "I understand you may be concerned about this issue. The city has resources available to address urban problems. How can I help you specifically?"
        elif sentiment == "positive":
            return "I'm glad you're interested in our city's services! How can I provide more specific information to help you?"
        else:
            return "Thank you for your question about urban services. Could you provide more specifics about what you're looking for in our city?"

