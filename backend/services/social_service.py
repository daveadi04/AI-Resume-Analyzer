import openai
from config import Config
import json
from datetime import datetime, timedelta
import pytz

openai.api_key = Config.OPENAI_API_KEY

class SocialService:
    def __init__(self):
        self.model = Config.OPENAI_MODEL
        self.temperature = Config.OPENAI_TEMPERATURE

    def generate_post(self, topic, platform='linkedin', tone='professional', length='medium'):
        """Generate a social media post based on topic and parameters"""
        prompt = f"""
        Create an engaging social media post for {platform} about:
        Topic: {topic}
        Tone: {tone}
        Length: {length}
        
        The post should:
        1. Be platform-appropriate
        2. Include relevant hashtags
        3. Encourage engagement
        4. Provide value to the reader
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are an expert {platform} content creator."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "post": response.choices[0].message.content,
            "hashtags": self._generate_hashtags(topic, platform),
            "best_time": self.optimize_posting_time(platform)
        }

    def generate_thread(self, topic, platform='twitter', num_tweets=5):
        """Generate a thread of related posts"""
        prompt = f"""
        Create a thread of {num_tweets} related posts for {platform} about:
        Topic: {topic}
        
        The thread should:
        1. Flow naturally
        2. Build on each point
        3. Include relevant hashtags
        4. End with a call to action
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are an expert {platform} thread creator."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        # Split the response into individual tweets
        tweets = self._split_into_tweets(response.choices[0].message.content)
        
        return {
            "thread": tweets,
            "hashtags": self._generate_hashtags(topic, platform),
            "best_time": self.optimize_posting_time(platform)
        }

    def suggest_hashtags(self, content, platform='linkedin'):
        """Suggest relevant hashtags for content"""
        prompt = f"""
        Suggest relevant hashtags for this {platform} content:
        {content}
        
        Include:
        1. Industry-specific hashtags
        2. Trending hashtags
        3. Engagement hashtags
        4. Platform-specific hashtags
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a social media hashtag expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return {
            "hashtags": response.choices[0].message.content.split(),
            "trending": self._get_trending_hashtags(platform)
        }

    def optimize_posting_time(self, platform, timezone='UTC'):
        """Suggest optimal posting times based on platform and timezone"""
        # In a real implementation, this would use platform-specific analytics
        # For now, we'll return some general best practices
        best_times = {
            'linkedin': [
                {'day': 'Tuesday', 'time': '10:00-12:00'},
                {'day': 'Wednesday', 'time': '09:00-11:00'},
                {'day': 'Thursday', 'time': '10:00-12:00'}
            ],
            'twitter': [
                {'day': 'Monday', 'time': '09:00-11:00'},
                {'day': 'Wednesday', 'time': '10:00-12:00'},
                {'day': 'Friday', 'time': '09:00-11:00'}
            ]
        }
        
        return {
            "platform": platform,
            "timezone": timezone,
            "best_times": best_times.get(platform, []),
            "next_optimal_time": self._calculate_next_optimal_time(platform, timezone)
        }

    def _generate_hashtags(self, topic, platform):
        """Generate relevant hashtags for a topic and platform"""
        prompt = f"""
        Generate relevant hashtags for {platform} about:
        {topic}
        
        Include:
        1. Industry-specific hashtags
        2. Trending hashtags
        3. Engagement hashtags
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a social media hashtag expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.split()

    def _split_into_tweets(self, content):
        """Split content into individual tweets"""
        # In a real implementation, this would handle Twitter's character limit
        # and properly format the thread
        tweets = content.split('\n\n')
        return [tweet.strip() for tweet in tweets if tweet.strip()]

    def _get_trending_hashtags(self, platform):
        """Get trending hashtags for a platform (simulated)"""
        # In a real implementation, this would use platform APIs
        return {
            'linkedin': ['#leadership', '#innovation', '#careeradvice'],
            'twitter': ['#tech', '#coding', '#developer']
        }.get(platform, [])

    def _calculate_next_optimal_time(self, platform, timezone):
        """Calculate the next optimal posting time"""
        # In a real implementation, this would use more sophisticated algorithms
        now = datetime.now(pytz.timezone(timezone))
        if platform == 'linkedin':
            # If it's Monday, suggest Tuesday
            if now.weekday() == 0:
                next_day = now + timedelta(days=1)
                return next_day.replace(hour=10, minute=0).isoformat()
        return now.replace(hour=10, minute=0).isoformat() 