"use client";

import React, { useState } from "react";
import { toast } from "react-hot-toast";
import './styles/interview.css';

export default function InterviewPage() {
  const [jobDescription, setJobDescription] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answers, setAnswers] = useState(null);
  const [userResponse, setUserResponse] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const generateQuestions = async () => {
    if (!jobDescription.trim()) {
      toast.error('Please enter a job description');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/interview/generate-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          job_description: jobDescription,
          difficulty,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate questions');
      }

      const data = await response.json();
      console.log('Questions generated:', data);
      
      if (data.questions && data.questions.length > 0) {
        setQuestions(data.questions);
        setCurrentQuestion(data.questions[0]);
        await generateAnswers(data.questions[0]);
        toast.success('Questions generated successfully!');
      } else {
        throw new Error('No questions were generated');
      }
    } catch (error) {
      console.error('Error generating questions:', error);
      toast.error(error.message || 'Failed to generate questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateAnswers = async (question) => {
    if (!question) return;

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/interview/generate-answers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          question,
          job_context: jobDescription,
          difficulty,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate answers');
      }

      const data = await response.json();
      console.log('Answers generated:', data);
      setAnswers(data);
    } catch (error) {
      console.error('Error generating answers:', error);
      toast.error(error.message || 'Failed to generate answers. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const analyzeResponse = async () => {
    if (!userResponse.trim()) {
      toast.error('Please provide a response');
      return;
    }

    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/interview/analyze-response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          response: userResponse,
          question: currentQuestion,
          job_context: jobDescription,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to analyze response');
      }

      const data = await response.json();
      console.log('Analysis received:', data);
      setAnalysis(data);
      toast.success('Response analyzed successfully!');
    } catch (error) {
      console.error('Error analyzing response:', error);
      toast.error(error.message || 'Failed to analyze response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const nextQuestion = () => {
    const currentIndex = questions.indexOf(currentQuestion);
    if (currentIndex < questions.length - 1) {
      const next = questions[currentIndex + 1];
      setCurrentQuestion(next);
      setUserResponse('');
      setAnalysis(null);
      generateAnswers(next);
    }
  };

  return (
    <div className="interview-container">
      <h1 className="page-title">Interview Preparation</h1>
      
      <div className="input-section">
        <label className="input-label">Job Description</label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="text-input"
          placeholder="Paste the job description here..."
        />
      </div>

      <div className="input-section">
        <label className="input-label">Difficulty Level</label>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="select-input"
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <button
        onClick={generateQuestions}
        disabled={loading || !jobDescription.trim()}
        className={`button button-primary ${loading ? 'loading' : ''}`}
      >
        {loading ? (
          <>
            <span className="loading-spinner" />
            <span className="ml-2">Generating...</span>
          </>
        ) : (
          'Generate Questions'
        )}
      </button>

      {currentQuestion && (
        <div className="question-section">
          <h2 className="question-text">{currentQuestion}</h2>

          {answers && (
            <div className="answers-grid">
              <div className="answer-card strong">
                <h3 className="answer-title">Strong Answer Example</h3>
                <p>{answers.strong_answer}</p>
                <div className="mt-4">
                  <h4 className="font-medium mb-2">Key Points:</h4>
                  <ul className="list-disc list-inside">
                    {answers.key_points?.map((point, index) => (
                      <li key={index} className="text-sm">{point}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="answer-card weak">
                <h3 className="answer-title">Weak Answer Example</h3>
                <p>{answers.weak_answer}</p>
                <div className="mt-4">
                  <h4 className="font-medium mb-2">Common Pitfalls:</h4>
                  <ul className="list-disc list-inside">
                    {answers.common_pitfalls?.map((pitfall, index) => (
                      <li key={index} className="text-sm">{pitfall}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          <div className="response-section">
            <label className="input-label">Your Response</label>
            <textarea
              value={userResponse}
              onChange={(e) => setUserResponse(e.target.value)}
              className="text-input"
              placeholder="Type your response here..."
            />
          </div>

          <div className="button-group">
            <button
              onClick={analyzeResponse}
              disabled={loading || !userResponse.trim()}
              className={`button button-success ${loading ? 'loading' : ''}`}
            >
              {loading ? (
                <>
                  <span className="loading-spinner" />
                  <span className="ml-2">Analyzing...</span>
                </>
              ) : (
                'Analyze Response'
              )}
            </button>

            <button
              onClick={nextQuestion}
              disabled={loading || questions.indexOf(currentQuestion) === questions.length - 1}
              className="button button-primary"
            >
              Next Question
            </button>
          </div>

          {analysis && (
            <div className="analysis-section">
              <h3 className="text-lg font-medium mb-4">Analysis</h3>
              <div className="score-display">
                <span className="font-medium">Score:</span>
                <div className="score-bar">
                  <div 
                    className="score-fill"
                    style={{ width: `${analysis.score}%` }}
                  />
                </div>
                <span>{analysis.score}/100</span>
              </div>
              <div className="mb-4">
                <p className="whitespace-pre-wrap">{analysis.analysis}</p>
              </div>
              <div>
                <h4 className="font-medium mb-2">Suggestions for Improvement:</h4>
                <ul className="suggestions-list">
                  {analysis.suggestions?.map((suggestion, index) => (
                    <li key={index} className="suggestion-item">{suggestion}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
