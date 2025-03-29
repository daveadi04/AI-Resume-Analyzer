import openai
from config import Config
import json

openai.api_key = Config.OPENAI_API_KEY

class InterviewService:
    def __init__(self):
        self.model = Config.OPENAI_MODEL
        self.temperature = Config.OPENAI_TEMPERATURE

    def generate_questions(self, job_description, difficulty='medium', num_questions=10):
        """Generate interview questions based on job description"""
        prompt = f"""
        Generate {num_questions} interview questions for this job:
        {job_description}
        
        Difficulty level: {difficulty}
        
        Include:
        1. Technical questions
        2. Behavioral questions
        3. Problem-solving questions
        4. Role-specific questions
        
        Format each question with:
        - Question text
        - Difficulty level
        - Category
        - Key points to address
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "questions": self._parse_questions(response.choices[0].message.content),
            "categories": self._extract_categories(job_description)
        }

    def generate_answers(self, question, job_context, difficulty='medium'):
        """Generate sample answers for an interview question"""
        prompt = f"""
        Generate sample answers for this interview question:
        Question: {question}
        
        Job Context: {json.dumps(job_context, indent=2)}
        Difficulty: {difficulty}
        
        Provide:
        1. A strong answer
        2. A weak answer
        3. Key points to include
        4. Common pitfalls to avoid
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "answers": self._parse_answers(response.choices[0].message.content),
            "tips": self._generate_tips(question, difficulty)
        }

    def analyze_response(self, response, question, job_context):
        """Analyze an interview response"""
        prompt = f"""
        Analyze this interview response:
        Question: {question}
        Response: {response}
        Job Context: {json.dumps(job_context, indent=2)}
        
        Provide:
        1. Strengths
        2. Areas for improvement
        3. Missing key points
        4. Overall effectiveness score
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview response analyzer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "analysis": response.choices[0].message.content,
            "score": self._calculate_score(response.choices[0].message.content),
            "suggestions": self._generate_suggestions(response.choices[0].message.content)
        }

    def generate_feedback(self, interview_data, job_context):
        """Generate comprehensive interview feedback"""
        prompt = f"""
        Generate comprehensive feedback for this interview:
        Interview Data: {json.dumps(interview_data, indent=2)}
        Job Context: {json.dumps(job_context, indent=2)}
        
        Include:
        1. Overall performance assessment
        2. Strengths and weaknesses
        3. Specific improvement areas
        4. Action items for preparation
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview feedback provider."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "feedback": response.choices[0].message.content,
            "action_items": self._extract_action_items(response.choices[0].message.content),
            "preparation_plan": self._generate_preparation_plan(response.choices[0].message.content)
        }

    def _parse_questions(self, content):
        """Parse generated questions into structured format"""
        # In a real implementation, this would properly parse the content
        questions = content.split('\n\n')
        return [q.strip() for q in questions if q.strip()]

    def _parse_answers(self, content):
        """Parse generated answers into structured format"""
        # In a real implementation, this would properly parse the content
        answers = content.split('\n\n')
        return [a.strip() for a in answers if a.strip()]

    def _extract_categories(self, job_description):
        """Extract question categories from job description"""
        prompt = f"""
        Extract relevant interview question categories for this job:
        {job_description}
        
        Return as a comma-separated list.
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert job analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.split(',')

    def _generate_tips(self, question, difficulty):
        """Generate tips for answering a question"""
        prompt = f"""
        Generate tips for answering this interview question:
        Question: {question}
        Difficulty: {difficulty}
        
        Include:
        1. Key points to remember
        2. Common mistakes to avoid
        3. Structure suggestions
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.split('\n')

    def _calculate_score(self, analysis):
        """Calculate an effectiveness score from analysis"""
        # In a real implementation, this would use more sophisticated scoring
        return 85  # Simulated score

    def _generate_suggestions(self, analysis):
        """Generate improvement suggestions from analysis"""
        prompt = f"""
        Generate specific improvement suggestions based on this analysis:
        {analysis}
        
        Focus on actionable items.
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.split('\n')

    def _extract_action_items(self, feedback):
        """Extract action items from feedback"""
        prompt = f"""
        Extract specific action items from this feedback:
        {feedback}
        
        Return as a numbered list.
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert action planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.split('\n')

    def _generate_preparation_plan(self, feedback):
        """Generate a preparation plan based on feedback"""
        prompt = f"""
        Create a detailed preparation plan based on this feedback:
        {feedback}
        
        Include:
        1. Daily tasks
        2. Resources to study
        3. Practice exercises
        4. Timeline
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview preparation planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content 