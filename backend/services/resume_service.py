import os
import re
import json
import logging
from PyPDF2 import PdfReader
from docx import Document
from typing import Dict, List, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeService:
    def __init__(self):
        # Common skills and keywords for matching
        self.common_skills = {
            'programming': {'python', 'java', 'javascript', 'c++', 'ruby', 'php', 'swift', 'kotlin', 'golang'},
            'web': {'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'},
            'database': {'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'nosql'},
            'cloud': {'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'},
            'tools': {'git', 'jenkins', 'jira', 'confluence', 'slack', 'postman'},
            'soft_skills': {'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical'}
        }

    def analyze_resume(self, resume_text: str, job_description: str) -> dict:
        try:
            # Clean and normalize text
            resume_text = self._normalize_text(resume_text)
            job_description = self._normalize_text(job_description)

            # Extract skills from both texts
            resume_skills = self._extract_skills(resume_text)
            job_skills = self._extract_skills(job_description)

            # Find matching and missing skills
            matching_skills = resume_skills.intersection(job_skills)
            missing_skills = job_skills - resume_skills

            # Calculate match score
            total_required_skills = len(job_skills) if job_skills else 1
            skill_match_score = (len(matching_skills) / total_required_skills) * 60

            # Analyze experience and education
            experience_score = self._analyze_experience(resume_text, job_description) * 25
            education_score = self._analyze_education(resume_text, job_description) * 15

            # Calculate total score
            match_score = int(skill_match_score + experience_score + education_score)
            match_score = min(max(match_score, 0), 100)  # Ensure score is between 0-100

            # Generate improvement suggestions
            suggestions = self._generate_suggestions(missing_skills, resume_text)

            # Analyze ATS compatibility
            ats_score, ats_suggestions = self._analyze_ats_compatibility(resume_text)

            return {
                "match_score": match_score,
                "analysis": {
                    "content_and_structure": self._analyze_content_structure(resume_text),
                    "ats_optimization": f"ATS Compatibility Score: {ats_score}%. {'; '.join(ats_suggestions)}",
                    "strengths": list(matching_skills),
                    "areas_for_improvement": list(missing_skills),
                    "job_match_analysis": f"Found {len(matching_skills)} matching skills out of {len(job_skills)} required skills",
                    "action_items": [f"Add skill: {skill}" for skill in list(missing_skills)[:3]]
                },
                "keywords": list(matching_skills),
                "suggestions": suggestions
            }
        except Exception as e:
            logger.error(f"Error in analyze_resume: {str(e)}")
            raise Exception(f"Failed to analyze resume: {str(e)}")

    def _normalize_text(self, text: str) -> str:
        """Normalize text for better matching"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return ' '.join(text.split())

    def _extract_skills(self, text: str) -> Set[str]:
        """Extract skills from text"""
        skills = set()
        for category, category_skills in self.common_skills.items():
            for skill in category_skills:
                if skill.lower() in text.lower():
                    skills.add(skill)
        return skills

    def _analyze_experience(self, resume_text: str, job_description: str) -> float:
        """Analyze experience match (returns score 0-1)"""
        # Extract years of experience from job description
        required_years = self._extract_years_of_experience(job_description)
        resume_years = self._extract_years_of_experience(resume_text)
        
        if required_years == 0:
            return 0.8  # Default good score if no specific requirement
        
        return min(resume_years / required_years, 1.0) if required_years > 0 else 0.5

    def _analyze_education(self, resume_text: str, job_description: str) -> float:
        """Analyze education match (returns score 0-1)"""
        education_levels = {
            'phd': 4,
            'master': 3,
            'bachelor': 2,
            'associate': 1
        }
        
        required_level = 0
        actual_level = 0
        
        for level, score in education_levels.items():
            if level in job_description.lower():
                required_level = score
            if level in resume_text.lower():
                actual_level = score
                
        if required_level == 0:
            return 0.8  # Default good score if no specific requirement
            
        return min(actual_level / required_level, 1.0) if required_level > 0 else 0.5

    def _extract_years_of_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)[\+]?\s*(?:years?|yrs?).+?experience',
            r'experience.+?(\d+)[\+]?\s*(?:years?|yrs?)',
            r'(\d+)[\+]?\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])
        return 0

    def _analyze_content_structure(self, resume_text: str) -> str:
        """Analyze resume content and structure"""
        sections = ['summary', 'experience', 'education', 'skills']
        found_sections = []
        
        for section in sections:
            if section in resume_text.lower():
                found_sections.append(section)
                
        if len(found_sections) >= 3:
            return "Well-structured resume with clear sections"
        else:
            return "Consider adding standard resume sections: Summary, Experience, Education, and Skills"

    def _analyze_ats_compatibility(self, resume_text: str) -> tuple:
        """Analyze ATS compatibility"""
        score = 100
        suggestions = []
        
        # Check for common ATS issues
        if len(resume_text.split()) < 100:
            score -= 20
            suggestions.append("Resume seems too short")
            
        if len(resume_text.split()) > 1000:
            score -= 10
            suggestions.append("Resume might be too long")
            
        if not re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', resume_text):
            score -= 15
            suggestions.append("Add contact information")
            
        if len(re.findall(r'[^\x00-\x7F]+', resume_text)) > 0:
            score -= 15
            suggestions.append("Remove special characters for better ATS compatibility")
            
        return score, suggestions

    def _generate_suggestions(self, missing_skills: Set[str], resume_text: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = [
            "Focus on adding these missing skills to your resume:",
            *[f"- Add experience with {skill}" for skill in list(missing_skills)[:5]]
        ]
        
        if len(resume_text.split()) < 100:
            suggestions.append("Add more detail to your experience descriptions")
            
        if not re.search(r'\d+', resume_text):
            suggestions.append("Quantify your achievements with numbers and metrics")
            
        return suggestions

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception("Failed to extract text from PDF file. Please ensure the file is not corrupted.")

    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            raise Exception("Failed to extract text from DOCX file. Please ensure the file is not corrupted.") 