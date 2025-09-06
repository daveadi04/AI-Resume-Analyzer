import os
import json
import requests # type: ignore
import logging
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class InterviewService:
    API_URL = "https://api.perplexity.ai/chat/completions"

    def __init__(self, api_key: str):
        """Initialize the service with API key and default parameters."""
        if not api_key:
            raise ValueError("API key is required.")
        
        self.api_key = api_key
        self.model = "sonar-pro"
        self.temperature = 0.3

    def _send_request(self, prompt: str, max_tokens: int = 500):
        """Helper function to send API requests and handle responses."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": self.temperature
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.API_URL, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP failures

            response_json = response.json()
            logging.info("API Response: %s", json.dumps(response_json, indent=2))

            if "choices" not in response_json or not response_json["choices"]:
                raise ValueError("Invalid API response: Missing 'choices' key or empty response.")

            content = response_json["choices"][0].get("message", {}).get("content", "").strip()

            if not content:
                raise ValueError("API returned an empty response.")

            return content

        except requests.RequestException as e:
            logging.error("API request failed: %s", str(e))
            raise Exception(f"API request error: {str(e)}")
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response from API.")
            raise ValueError("Invalid JSON response from API.")

    def generate_questions(self, job_description: str, difficulty: str = 'medium', num_questions: int = 5):
        """Generate interview questions based on job description."""
        if not job_description:
            raise ValueError("Job description is required.")

        prompt = f"""
        Given this job description:
        {job_description}

        Generate {num_questions} interview questions at {difficulty} difficulty level.
        Format response as JSON:
        {{
            "questions": ["Question 1", "Question 2", ...]
        }}
        """

        response_text = self._send_request(prompt)

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format in API response.")
            raise ValueError("API returned an invalid JSON response.")

        if not isinstance(result, dict) or "questions" not in result:
            logging.error("Unexpected response format: %s", result)
            raise ValueError("Unexpected API response format.")

        return result["questions"]

    def generate_answers(self, question: str, job_context: str):
        """Generate sample answers for a given interview question."""
        if not question:
            raise ValueError("Question is required.")
        if not job_context:
            raise ValueError("Job context is required.")

        prompt = f"""
        Given this interview question:
        {question}

        Job Context:
        {job_context}

        Generate a strong sample answer.
        Format response as JSON:
        {{
            "strong_answer": "Your detailed answer"
        }}
        """

        response_text = self._send_request(prompt)

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format in API response.")
            raise ValueError("API returned an invalid JSON response.")

        if not isinstance(result, dict) or "strong_answer" not in result:
            logging.error("Unexpected response format: %s", result)
            raise ValueError("Unexpected API response format.")

        return result["strong_answer"]

    def analyze_response(self, response: str, question: str, job_context: str):
        """Analyze an interview response and provide feedback."""
        if not response:
            raise ValueError("Response is required.")
        if not question:
            raise ValueError("Question is required.")
        if not job_context:
            raise ValueError("Job context is required.")

        prompt = f"""
        Analyze this interview response:
        Question: {question}
        Response: {response}
        Job Context: {job_context}

        Provide a detailed analysis and score.
        Format response as JSON:
        {{
            "analysis": "Detailed feedback",
            "score": 85
        }}
        """

        response_text = self._send_request(prompt)

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format in API response.")
            raise ValueError("API returned an invalid JSON response.")

        if not isinstance(result, dict) or "analysis" not in result or "score" not in result:
            logging.error("Unexpected response format: %s", result)
            raise ValueError("Unexpected API response format.")

        return {
            "analysis": result["analysis"],
            "score": result["score"]
        }

# Example Usage:
if __name__ == "__main__":
    API_KEY = os.getenv("PERPLEXITY_API_KEY")  # Load from environment API removed for security
    interview_service = InterviewService(API_KEY)

    job_description = """
    We are looking for a Senior Python Developer with expertise in Django, REST APIs, and cloud services.
    The candidate should have experience in microservices architecture and database management.
    """

    try:
        questions = interview_service.generate_questions(job_description, difficulty="hard", num_questions=3)
        print("Generated Questions:", questions)

        # Generate an answer for the first question
        sample_answer = interview_service.generate_answers(questions[0], job_description)
        print("Sample Answer:", sample_answer)

        # Analyze a response
        analysis = interview_service.analyze_response(sample_answer, questions[0], job_description)
        print("Response Analysis:", analysis)

    except Exception as e:
        print("Error:", str(e))
