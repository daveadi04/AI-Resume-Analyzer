# AI Personal Branding Assistant - Technical Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Backend Development](#backend-development)
4. [Frontend Development](#frontend-development)
5. [Features](#features)
6. [API Integration](#api-integration)
7. [Database](#database)
8. [Deployment](#deployment)
9. [Development Setup](#development-setup)

## Project Overview

The AI Personal Branding Assistant is a full-stack web application designed to help users optimize their professional presence through AI-powered tools. The application consists of a Flask backend and a Next.js frontend.

### Tech Stack

- **Backend**: Python, Flask, OpenAI API
- **Frontend**: Next.js, React, TypeScript
- **Database**: PostgreSQL
- **Styling**: Custom CSS, Tailwind CSS
- **Deployment**: Docker, AWS

## Architecture

### Project Structure

```
Personal-Branding-Assistant/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── services/              # Business logic layer
│   │   ├── resume_service.py
│   │   ├── portfolio_service.py
│   │   ├── social_service.py
│   │   └── interview_service.py
│   ├── routes/               # API endpoints
│   │   ├── resume_routes.py
│   │   ├── portfolio_routes.py
│   │   ├── social_routes.py
│   │   └── interview_routes.py
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── app/                  # Next.js application
    │   ├── page.tsx         # Home page
    │   ├── resume/          # Resume feature
    │   ├── portfolio/       # Portfolio feature
    │   ├── social/         # Social media feature
    │   └── interview/      # Interview feature
    └── package.json        # Node.js dependencies
```

## Backend Development

### 1. Main Application (app.py)

The main Flask application serves as the entry point for the backend:

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
```

Key components:

- Flask application initialization
- CORS configuration for frontend communication
- Blueprint registration for modular routing
- Environment variable loading

### 2. Services Layer

The services layer contains the business logic for each feature:

#### Resume Service

```python
class ResumeService:
    def analyze_resume(self, resume_file):
        """
        Analyzes a resume file using OpenAI's GPT model
        """
        # Implementation details
        pass

    def generate_resume(self, job_description):
        """
        Generates a resume based on job description
        """
        # Implementation details
        pass
```

#### Portfolio Service

```python
class PortfolioService:
    def analyze_github(self, username):
        """
        Analyzes GitHub profile and generates portfolio data
        """
        # Implementation details
        pass

    def generate_portfolio(self, user_data):
        """
        Generates portfolio website from user data
        """
        # Implementation details
        pass
```

### 3. Routes Layer

Routes handle HTTP requests and responses:

```python
@bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Endpoint for resume analysis
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        result = resume_service.analyze_resume(file)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Frontend Development

### 1. Next.js Application Structure

The frontend uses Next.js 13+ with the App Router:

```
frontend/app/
├── page.tsx                 # Home page
├── resume/                  # Resume feature
│   ├── page.tsx
│   └── styles/
│       └── resume.css
├── portfolio/              # Portfolio feature
├── social/                # Social media feature
└── interview/             # Interview feature
```

### 2. Home Page (page.tsx)

The home page serves as the landing page:

```typescript
export default function Home() {
  return (
    <div className="home-container">
      <h1>AI Personal Branding Assistant</h1>
      <div className="features-grid">{/* Feature cards */}</div>
    </div>
  );
}
```

### 3. Resume Page (resume/page.tsx)

Example of a feature page with state management and API integration:

```typescript
export default function ResumePage() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeResume = async () => {
    if (!file) {
      toast.error("Please upload a resume first");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const response = await fetch(
        `${process.env.API_URL}/api/resume/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to analyze resume");
      }

      const data = await response.json();
      setAnalysis(data);
      toast.success("Resume analyzed successfully!");
    } catch (error) {
      toast.error("Failed to analyze resume");
    } finally {
      setLoading(false);
    }
  };

  return <div className="resume-container">{/* UI components */}</div>;
}
```

### 4. Styling (resume.css)

Custom CSS with modern design principles:

```css
.resume-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #e0f2fe, #f0f9ff);
  padding: 2rem;
}

.card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #bae6fd;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
```

## Features

### 1. Resume Analysis & Generation

- **File Upload**: Supports PDF and DOC formats
- **Analysis**: AI-powered resume analysis
- **Generation**: Creates tailored resumes based on job descriptions
- **Keywords**: Extracts relevant keywords and skills

### 2. Portfolio Generation

- **GitHub Integration**: Analyzes GitHub profiles
- **Project Showcase**: Displays projects and contributions
- **Customization**: Allows template selection and customization
- **Deployment**: One-click deployment to hosting platforms

### 3. Social Media Content

- **Platform Support**: LinkedIn, Twitter, Instagram
- **Content Generation**: AI-powered post creation
- **Hashtag Suggestions**: Relevant hashtag recommendations
- **Scheduling**: Post scheduling and management

### 4. Interview Preparation

- **Question Generation**: Creates relevant interview questions
- **Answer Suggestions**: Provides sample answers
- **Mock Interviews**: Simulates interview scenarios
- **Feedback**: Performance analysis and improvement tips

## API Integration

### 1. Backend API Endpoints

```python
# Resume Analysis
POST /api/resume/analyze
Content-Type: multipart/form-data
Body: resume (file)

# Portfolio Generation
POST /api/portfolio/generate
Content-Type: application/json
Body: {
  "github_username": "string",
  "template": "string"
}

# Social Media Content
POST /api/social/generate-post
Content-Type: application/json
Body: {
  "topic": "string",
  "platform": "string",
  "tone": "string"
}
```

### 2. Frontend API Integration

```typescript
const API_URL = process.env.API_URL;

async function makeApiCall(endpoint: string, options: RequestInit) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`);
  }

  return response.json();
}
```

## Database

### PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content TEXT NOT NULL,
    analysis JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolios table
CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    github_username VARCHAR(255),
    content JSONB,
    deployed_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Deployment

### 1. Docker Configuration

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]

# Frontend Dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

### 2. AWS Deployment

1. Create EC2 instance
2. Install Docker and Docker Compose
3. Deploy using Docker Compose:

```bash
docker-compose up -d
```

## Development Setup

### 1. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run development server
python app.py
```

### 2. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API URL

# Run development server
npm run dev
```

### 3. Database Setup

```bash
# Create database
createdb personal_branding

# Run migrations
flask db upgrade
```

## Best Practices

1. **Code Organization**

   - Follow modular architecture
   - Separate concerns (routes, services, models)
   - Use TypeScript for type safety

2. **Error Handling**

   - Implement proper error handling
   - Use try-catch blocks
   - Provide meaningful error messages

3. **Security**

   - Use environment variables for sensitive data
   - Implement proper authentication
   - Validate user input

4. **Performance**

   - Optimize database queries
   - Implement caching where appropriate
   - Use lazy loading for components

5. **Testing**
   - Write unit tests
   - Implement integration tests
   - Use test-driven development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
