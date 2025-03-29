"use client";

import React, { useState } from "react";
import Link from "next/link";
import "./styles/home.css";

export default function Home() {
  const [resumeData, setResumeData] = useState(null);
  const [error, setError] = useState(null);

  // Function to handle the API request
  const handleAnalyzeResume = async (data: any) => {
    try {
      const response = await fetch("http://localhost:5000/api/resume/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
        credentials: "include", // Ensure credentials (cookies) are sent if needed
      });

      if (!response.ok) {
        throw new Error("Failed to analyze resume");
      }

      const result = await response.json();
      setResumeData(result);
    } catch (err) {
      setError("An error occurred while analyzing the resume.");
      console.error(err);
    }
  };

  return (
    <div className="home-container">
      <main className="main-content">
        <div className="header">
          <h1 className="title">AI Personal Branding Assistant</h1>
          <p className="subtitle">
            Transform your professional presence with AI-powered tools
          </p>
        </div>

        {/* Example of triggering the API request */}
        <button
          onClick={() => handleAnalyzeResume({ resume: "sample resume data" })}
        >
          Analyze Resume
        </button>

        {/* Displaying response data */}
        {resumeData && <div>Results: {JSON.stringify(resumeData)}</div>}
        {error && <div>{error}</div>}

        <div className="features-grid">
          <Link href="/resume">
            <div className="feature-card">
              <div className="feature-icon">📄</div>
              <h2 className="feature-title">Resume & LinkedIn Analyzer</h2>
              <p className="feature-description">
                Get AI-powered analysis and optimization suggestions for your
                resume and LinkedIn profile
              </p>
            </div>
          </Link>

          <Link href="/portfolio">
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h2 className="feature-title">Portfolio Generator</h2>
              <p className="feature-description">
                Create a professional portfolio website from your GitHub profile
                and projects
              </p>
            </div>
          </Link>

          <Link href="/social">
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h2 className="feature-title">Social Media Content</h2>
              <p className="feature-description">
                Generate engaging social media posts and threads to build your
                brand
              </p>
            </div>
          </Link>

          <Link href="/interview">
            <div className="feature-card">
              <div className="feature-icon">💼</div>
              <h2 className="feature-title">Interview Preparation</h2>
              <p className="feature-description">
                Get personalized interview questions and practice responses
              </p>
            </div>
          </Link>
        </div>

        <section className="how-it-works">
          <h2 className="section-title">How It Works</h2>
          <div className="steps-grid">
            <div className="step-item">
              <div className="icon-container">
                <span className="icon">📤</span>
              </div>
              <h3 className="step-title">Upload Your Data</h3>
              <p className="step-description">
                Share your resume, LinkedIn profile, or job description
              </p>
            </div>
            <div className="step-item">
              <div className="icon-container">
                <span className="icon">🤖</span>
              </div>
              <h3 className="step-title">AI Analysis</h3>
              <p className="step-description">
                Get personalized insights and recommendations
              </p>
            </div>
            <div className="step-item">
              <div className="icon-container">
                <span className="icon">✨</span>
              </div>
              <h3 className="step-title">Optimize & Improve</h3>
              <p className="step-description">
                Enhance your professional presence with AI suggestions
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
