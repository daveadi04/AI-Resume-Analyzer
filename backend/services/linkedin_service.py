import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class LinkedInService:
    def __init__(self):
        self.linkedin_client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.linkedin_client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.linkedin_redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.is_configured = bool(self.linkedin_client_id and self.linkedin_client_secret)
        self.model = os.getenv('OPENAI_MODEL')
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE'))

    def analyze_profile(self, profile_url: str) -> dict:
        """
        Analyze LinkedIn profile content
        """
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            # In a real implementation, you would use the LinkedIn API
            # For now, we'll simulate profile data
            profile_data = self._fetch_profile_data(profile_url)
            
            prompt = f"""
            Analyze this LinkedIn profile and provide detailed feedback on:
            1. Profile completeness and professionalism
            2. Content quality and impact
            3. Areas for improvement
            4. Strengths and weaknesses
            
            Profile data:
            {json.dumps(profile_data, indent=2)}
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert LinkedIn profile reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "keywords": self._extract_keywords(profile_data)
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def optimize_profile(self, profile_data):
        """Generate optimization suggestions for a LinkedIn profile"""
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            prompt = f"""
            Provide detailed optimization suggestions for this LinkedIn profile:
            {json.dumps(profile_data, indent=2)}
            
            Include suggestions for:
            1. Headline optimization
            2. About section improvement
            3. Experience descriptions
            4. Skills and endorsements
            5. Profile photo and background
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert LinkedIn profile optimizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            return {
                "suggestions": response.choices[0].message.content,
                "optimized_headline": self._generate_headline(profile_data)
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def generate_post(self, topic, tone='professional', length='medium'):
        """Generate a LinkedIn post based on topic and parameters"""
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            prompt = f"""
            Create an engaging LinkedIn post about:
            Topic: {topic}
            Tone: {tone}
            Length: {length}
            
            The post should:
            1. Be engaging and professional
            2. Include relevant hashtags
            3. Encourage interaction
            4. Provide value to the reader
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert LinkedIn content creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            return {
                "post": response.choices[0].message.content,
                "hashtags": self._generate_hashtags(topic)
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def suggest_keywords(self, profile_data):
        """Suggest relevant keywords for profile optimization"""
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            prompt = f"""
            Suggest relevant keywords and skills for this LinkedIn profile:
            {json.dumps(profile_data, indent=2)}
            
            Include:
            1. Industry-specific keywords
            2. Skill-related keywords
            3. Job title variations
            4. Trending terms in the field
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a keyword optimization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return {
                "keywords": response.choices[0].message.content.split('\n'),
                "trending_terms": self._get_trending_terms(profile_data)
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def _fetch_profile_data(self, profile_url):
        """Fetch profile data from LinkedIn (simulated)"""
        # In a real implementation, this would use the LinkedIn API
        return {
            "headline": "Software Engineer | Full Stack Developer",
            "about": "Passionate software engineer with 5+ years of experience...",
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2020 - Present"
                }
            ],
            "skills": ["Python", "JavaScript", "React", "Node.js"]
        }

    def _generate_headline(self, profile_data):
        """Generate an optimized headline"""
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            prompt = f"""
            Create an optimized LinkedIn headline for this profile:
            {json.dumps(profile_data, indent=2)}
            
            The headline should:
            1. Be attention-grabbing
            2. Include key skills
            3. Be optimized for search
            4. Be under 220 characters
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a LinkedIn headline expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def _generate_hashtags(self, topic):
        """Generate relevant hashtags for a post"""
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            prompt = f"""
            Generate relevant hashtags for a LinkedIn post about:
            {topic}
            
            Include:
            1. Industry-specific hashtags
            2. Trending hashtags
            3. Professional development hashtags
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media hashtag expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.split()
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def _get_trending_terms(self, profile_data):
        """Get trending terms in the industry (simulated)"""
        # In a real implementation, this would use LinkedIn's trending data
        return ["AI", "Machine Learning", "Cloud Computing", "DevOps"]

    def _extract_keywords(self, profile_data):
        """Extract important keywords from profile data"""
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            prompt = f"""
            Extract the most important keywords from this LinkedIn profile:
            {json.dumps(profile_data, indent=2)}
            
            Return them as a comma-separated list.
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a keyword extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.split(',')
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }

    def get_auth_url(self) -> str:
        """
        Get LinkedIn OAuth URL
        """
        if not self.is_configured:
            return None

        # Your existing OAuth URL generation code here
        pass

    def handle_callback(self, code: str) -> dict:
        """
        Handle OAuth callback
        """
        if not self.is_configured:
            return {
                "error": "LinkedIn API is not configured. Please set up LinkedIn API credentials to use this feature.",
                "status": "not_configured"
            }

        try:
            # Your existing callback handling code here
            pass
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            } 