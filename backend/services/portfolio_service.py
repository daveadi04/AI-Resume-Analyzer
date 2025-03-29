import openai
from config import Config
from github import Github
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = Config.OPENAI_API_KEY
github = Github(Config.GITHUB_API_KEY)

class PortfolioService:
    def __init__(self):
        self.model = Config.OPENAI_MODEL
        self.temperature = Config.OPENAI_TEMPERATURE
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_client = Github(self.github_token) if self.github_token else None

    def generate_portfolio(self, user_data):
        """Generate a portfolio website based on user data"""
        prompt = f"""
        Create a complete portfolio website structure for this user:
        {json.dumps(user_data, indent=2)}
        
        Generate:
        1. HTML structure
        2. CSS styling
        3. JavaScript functionality
        4. Responsive design
        5. SEO optimization
        
        Include sections for:
        - Hero/Introduction
        - About Me
        - Skills
        - Projects
        - Experience
        - Contact
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert web developer and portfolio designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "html": self._extract_html(response.choices[0].message.content),
            "css": self._extract_css(response.choices[0].message.content),
            "js": self._extract_js(response.choices[0].message.content),
            "meta": self._generate_meta_tags(user_data)
        }

    def analyze_github(self, username):
        """
        Analyzes a GitHub profile and returns relevant information
        """
        try:
            if not self.github_client:
                raise Exception("GitHub token not configured")

            user = self.github_client.get_user(username)
            
            # Get user's repositories
            repos = []
            for repo in user.get_repos():
                if not repo.fork:  # Only include non-forked repositories
                    repos.append({
                        'name': repo.name,
                        'description': repo.description,
                        'language': repo.language,
                        'stars': repo.stargazers_count,
                        'url': repo.html_url
                    })

            # Get user's contributions
            contributions = {
                'public_repos': user.public_repos,
                'public_gists': user.public_gists,
                'followers': user.followers,
                'following': user.following
            }

            return {
                'user': {
                    'name': user.name,
                    'bio': user.bio,
                    'location': user.location,
                    'company': user.company,
                    'blog': user.blog,
                    'email': user.email,
                    'hireable': user.hireable
                },
                'repositories': repos,
                'contributions': contributions
            }
        except Exception as e:
            raise Exception(f"Failed to analyze GitHub profile: {str(e)}")

    def customize_portfolio(self, portfolio_data, customization):
        """Customize the portfolio website based on user preferences"""
        prompt = f"""
        Customize this portfolio website:
        Portfolio Data: {json.dumps(portfolio_data, indent=2)}
        Customization Options: {json.dumps(customization, indent=2)}
        
        Apply the following customizations:
        1. Color scheme
        2. Layout
        3. Typography
        4. Animations
        5. Additional sections
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert web designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return {
            "html": self._extract_html(response.choices[0].message.content),
            "css": self._extract_css(response.choices[0].message.content),
            "js": self._extract_js(response.choices[0].message.content)
        }

    def deploy_portfolio(self, portfolio_id):
        """
        Deploys the generated portfolio to a hosting service
        """
        try:
            # Here you would implement the deployment logic
            # This could involve:
            # 1. Setting up hosting (e.g., GitHub Pages, Netlify, Vercel)
            # 2. Uploading files
            # 3. Configuring domain settings
            
            return {
                'status': 'success',
                'message': 'Portfolio deployed successfully',
                'deployed_url': 'https://your-portfolio-url.com'
            }
        except Exception as e:
            raise Exception(f"Failed to deploy portfolio: {str(e)}")

    def _extract_html(self, content):
        """Extract HTML code from the response"""
        # In a real implementation, this would parse the content properly
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio</title>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

    def _extract_css(self, content):
        """Extract CSS code from the response"""
        # In a real implementation, this would parse the content properly
        return """
        /* Portfolio Styles */
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        """

    def _extract_js(self, content):
        """Extract JavaScript code from the response"""
        # In a real implementation, this would parse the content properly
        return """
        // Portfolio JavaScript
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize portfolio functionality
        });
        """

    def _generate_meta_tags(self, user_data):
        """Generate SEO meta tags for the portfolio"""
        prompt = f"""
        Generate SEO meta tags for this portfolio:
        {json.dumps(user_data, indent=2)}
        
        Include:
        1. Title
        2. Description
        3. Keywords
        4. Open Graph tags
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an SEO expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content

    def _extract_languages(self, repo_data):
        """Extract programming languages from repository data"""
        languages = {}
        for repo in repo_data:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        return languages 