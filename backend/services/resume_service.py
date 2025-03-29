import os
from dotenv import load_dotenv
from openai import OpenAI
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class ResumeService:
    def __init__(self):
        self.model = "gpt-4"
        self.temperature = 0.7

    def analyze_resume(self, filepath):
        """Analyze a resume and provide feedback"""
        # Extract text from PDF
        text = self._extract_text_from_pdf(filepath)
        
        # Generate analysis using OpenAI
        prompt = f"""
        Analyze this resume and provide detailed feedback on:
        1. Content and structure
        2. Keywords and ATS optimization
        3. Areas for improvement
        4. Strengths and weaknesses
        
        Resume text:
        {text}
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "analysis": response.choices[0].message.content,
            "keywords": self._extract_keywords(text)
        }

    def generate_resume(self, job_description, user_profile):
        """Generate a tailored resume based on job description and user profile"""
        prompt = f"""
        Create a professional resume tailored for this job description:
        {job_description}
        
        User profile information:
        {user_profile}
        
        Generate a complete resume with:
        1. Professional summary
        2. Work experience
        3. Skills
        4. Education
        5. Projects
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert resume writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "resume": response.choices[0].message.content,
            "keywords": self._extract_keywords(job_description)
        }

    def generate_cover_letter(self, job_description, resume):
        """Generate a cover letter based on job description and resume"""
        prompt = f"""
        Create a compelling cover letter for this job:
        {job_description}
        
        Using this resume information:
        {resume}
        
        The cover letter should:
        1. Be personalized to the job
        2. Highlight relevant experience
        3. Show enthusiasm for the role
        4. Be concise and professional
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "cover_letter": response.choices[0].message.content
        }

    def _extract_text_from_pdf(self, filepath):
        """Extract text from PDF file"""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def _extract_keywords(self, text):
        """Extract important keywords from text"""
        prompt = f"""
        Extract the most important keywords and skills from this text:
        {text}
        
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

    def extract_keywords(self, text: str) -> list:
        """
        Extract keywords from text
        """
        try:
            prompt = f"""Extract the most important keywords from this text:
            {text}
            
            Return only a comma-separated list of keywords."""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a keyword extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )

            keywords = response.choices[0].message.content.split(',')
            return [k.strip() for k in keywords]

        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []

    def calculate_match_score(self, analysis: str) -> int:
        """
        Calculate match score from analysis
        """
        try:
            prompt = f"""Based on this analysis, calculate a match percentage (0-100):
            {analysis}
            
            Return only the number."""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a job matching expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )

            score = int(response.choices[0].message.content.strip())
            return min(max(score, 0), 100)  # Ensure score is between 0 and 100

        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            return 0 