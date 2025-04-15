# app/agents/urban_agent.py
from app.core.agent_base import AgentBase
from app.core.cognitive_services import CognitiveServicesClient
import logging

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
                
    def generate_enhanced_response(self, question: str, key_phrases: list, sentiment: str) -> str:
        """
        Generate enhanced responses using AI-derived insights from the question.
        
        Parameters:
        - question (str): The original question
        - key_phrases (list): Key phrases extracted from the question
        - sentiment (str): Sentiment of the question (positive, neutral, negative)
        
        Returns:
        - str: An enhanced response
        """
        # Extract urban-specific keywords from the key phrases
        urban_keywords = {
            "traffic": ["Traffic congestion is currently moderate in the downtown area. Peak hours are 7-9 AM and 4-6 PM.",
                       "The city has implemented smart traffic lights that adapt to traffic flow."],
            "housing": ["Housing prices have increased by 5% in urban centers over the past year.",
                       "New affordable housing initiatives include mixed-use developments near transit hubs."],
            "transportation": ["Public transportation ridership has increased by 12% this quarter.",
                             "The city is expanding bike lanes and pedestrian-friendly infrastructure."],
            "parks": ["The urban parks system covers 15% of the city's area.",
                    "Green spaces have been shown to reduce urban heat and improve mental health."],
            "development": ["Smart urban development focuses on sustainability and community needs.",
                          "Recent projects include revitalizing the waterfront district."],
            "pollution": ["Air quality monitoring stations show improved metrics compared to last year.",
                        "The city has implemented a comprehensive waste management program."]
        }
        
        # Check if any key phrases match our urban topics
        for phrase in key_phrases:
            phrase_lower = phrase.lower()
            for keyword, responses in urban_keywords.items():
                if keyword in phrase_lower:
                    return responses[0]  # Return the first relevant response
        
        # If we have traffic in the question
        if "traffic" in question.lower():
            return urban_keywords["traffic"][0]
        # If we have weather in the question
        elif "weather" in question.lower():
            return "The weather today is sunny with a high of 25°C. Urban areas may experience temperatures 2-3°C higher due to the heat island effect."
        # Sentiment-based generic responses
        elif sentiment == "negative":
            return "I understand your concerns about urban issues. The city's strategic plan addresses challenges through data-driven solutions and community engagement."
        elif sentiment == "positive":
            return "I'm glad you're enthusiastic about urban development! Our city continues to implement smart technologies and sustainable practices to enhance quality of life."
        else:
            return "Urban areas are complex systems that require integrated planning approaches. Our smart city initiatives focus on sustainability, efficiency, and improved quality of life for residents."

