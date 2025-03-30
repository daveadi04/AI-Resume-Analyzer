"use client";
import React, { useState } from "react";
import { toast } from "react-toastify";
import "./styles/resume.css";
import ResumeBuilder from './components/ResumeBuilder';
import './styles/resume-builder.css';

// Get API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

const ResumePage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<'analyzer' | 'builder'>('analyzer');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      // Check file size (16MB limit)
      if (selectedFile.size > 16 * 1024 * 1024) {
        toast.error("File size must be less than 16MB");
        return;
      }
      // Check file type
      if (!selectedFile.type.match('application/pdf|application/msword|application/vnd.openxmlformats-officedocument.wordprocessingml.document')) {
        toast.error("Please upload a PDF or DOC/DOCX file");
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleAnalyzeResume = async () => {
    if (!file || !jobDescription) {
      toast.error("Please upload a resume and provide a job description");
      return;
    }

    setLoading(true);
    setAnalysis(null);  // Clear previous analysis

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("job_description", jobDescription);

      console.log("Sending request to:", `${API_URL}/api/analyze-resume`);
      console.log("File:", file.name, "Size:", file.size);

      const response = await fetch(`${API_URL}/api/analyze-resume`, {
        method: "POST",
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include',
      });

      console.log("Response status:", response.status);
      const contentType = response.headers.get("content-type");
      
      if (!response.ok) {
        let errorMessage = "Failed to analyze resume";
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || `Error: ${response.status}`;
        } catch (e) {
          console.error("Error parsing error response:", e);
        }
        throw new Error(errorMessage);
      }

      if (!contentType || !contentType.includes("application/json")) {
        throw new Error("Invalid response format from server");
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }
      
      setAnalysis(data);
      toast.success("Resume analysis completed!");
    } catch (error) {
      console.error("Error analyzing resume:", error);
      toast.error(error instanceof Error ? error.message : "Failed to analyze resume. Please try again.");
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-page">
      <div className="tab-buttons">
        <button 
          className={`tab-button ${activeTab === 'analyzer' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyzer')}
        >
          Resume Analyzer
        </button>
        <button 
          className={`tab-button ${activeTab === 'builder' ? 'active' : ''}`}
          onClick={() => setActiveTab('builder')}
        >
          Resume Builder
        </button>
      </div>

      {activeTab === 'analyzer' ? (
        <div className="resume-container">
          <h1 className="page-title">Resume & LinkedIn Analyzer</h1>

          <div className="content-grid">
            <div className="card">
              <h2 className="card-title">Analyze Your Resume</h2>
              <div className="form-group">
                <label className="label">Upload Resume</label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={handleFileChange}
                  className="input"
                />
              </div>

              <div className="form-group">
                <label className="label">Job Description</label>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="input"
                  placeholder="Paste the job description here..."
                />
              </div>

              <button
                onClick={handleAnalyzeResume}
                disabled={loading || !file || !jobDescription}
                className={`btn btn-primary ${loading ? "loading" : ""}`}
              >
                {loading ? "Analyzing..." : "Analyze Resume"}
              </button>
            </div>

            {analysis && (
              <div className="results-card">
                <h2 className="results-title">Analysis Results</h2>
                
                {analysis.match_score !== undefined && (
                  <div className="score-section">
                    <h3 className="section-title">Match Score</h3>
                    <div className="score-display">
                      <div className="score-circle" style={{
                        background: `conic-gradient(#38bdf8 ${analysis.match_score}%, #e0f2fe ${analysis.match_score}% 100%)`
                      }}>
                        <span className="score-number">{analysis.match_score}%</span>
                      </div>
                    </div>
                  </div>
                )}

                <div className="analysis-sections">
                  <div className="analysis-section">
                    <h3 className="section-title">Content and Structure</h3>
                    <p className="analysis-text">{analysis.analysis?.content_and_structure}</p>
                  </div>

                  <div className="analysis-section">
                    <h3 className="section-title">ATS Optimization</h3>
                    <p className="analysis-text">{analysis.analysis?.ats_optimization}</p>
                  </div>

                  <div className="analysis-section">
                    <h3 className="section-title">Strengths</h3>
                    <ul className="analysis-list">
                      {analysis.analysis?.strengths.map((strength: string, index: number) => (
                        <li key={index} className="analysis-item">✓ {strength}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="analysis-section">
                    <h3 className="section-title">Areas for Improvement</h3>
                    <ul className="analysis-list">
                      {analysis.analysis?.areas_for_improvement.map((area: string, index: number) => (
                        <li key={index} className="analysis-item">⚡ {area}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="analysis-section">
                    <h3 className="section-title">Job Match Analysis</h3>
                    <p className="analysis-text">{analysis.analysis?.job_match_analysis}</p>
                  </div>

                  <div className="analysis-section">
                    <h3 className="section-title">Action Items</h3>
                    <ul className="analysis-list">
                      {analysis.analysis?.action_items.map((item: string, index: number) => (
                        <li key={index} className="analysis-item">→ {item}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {analysis.keywords && analysis.keywords.length > 0 && (
                  <div className="keywords-section">
                    <h3 className="section-title">Key Skills and Keywords</h3>
                    <div className="keywords-container">
                      {analysis.keywords.map((keyword: string, index: number) => (
                        <span key={index} className="keyword-tag">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {analysis.suggestions && analysis.suggestions.length > 0 && (
                  <div className="suggestions-section">
                    <h3 className="section-title">Suggestions for Improvement</h3>
                    <ul className="analysis-list">
                      {analysis.suggestions.map((suggestion: string, index: number) => (
                        <li key={index} className="analysis-item">💡 {suggestion}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ) : (
        <ResumeBuilder />
      )}
    </div>
  );
};

export default ResumePage;
