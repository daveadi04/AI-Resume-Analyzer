"use client";
import React, { useState } from "react";
import { toast } from "react-toastify";
import "./styles/resume.css";

// Get API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export default function ResumePage() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyzeResume = async () => {
    if (!file) {
      toast.error("Please upload a resume first");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      console.log("Sending request to:", `${API_URL}/api/resume/analyze`);
      const response = await fetch(`${API_URL}/api/resume/analyze`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to analyze resume");
      }

      const data = await response.json();
      setAnalysis(data);
      toast.success("Resume analyzed successfully!");
    } catch (error) {
      console.error("Error analyzing resume:", error);
      toast.error(
        error instanceof Error ? error.message : "Failed to analyze resume"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateResume = async () => {
    if (!jobDescription) {
      toast.error("Please enter a job description");
      return;
    }

    setLoading(true);
    try {
      console.log("Sending request to:", `${API_URL}/api/resume/generate`);
      const response = await fetch(`${API_URL}/api/resume/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ job_description: jobDescription }),
        credentials: "include",
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to generate resume");
      }

      const data = await response.json();
      setAnalysis(data);
      toast.success("Resume generated successfully!");
    } catch (error) {
      console.error("Error generating resume:", error);
      toast.error(
        error instanceof Error ? error.message : "Failed to generate resume"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
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
          <button
            onClick={handleAnalyzeResume}
            disabled={loading || !file}
            className={`btn btn-primary ${loading ? "loading" : ""}`}
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </div>

        <div className="card">
          <h2 className="card-title">Generate Resume</h2>
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
            onClick={handleGenerateResume}
            disabled={loading || !jobDescription}
            className={`btn btn-primary ${loading ? "loading" : ""}`}
          >
            {loading ? "Generating..." : "Generate Resume"}
          </button>
        </div>
      </div>

      {analysis && (
        <div className="results-card">
          <h2 className="results-title">Analysis Results</h2>
          <div className="form-group">
            <h3 className="section-title">Analysis</h3>
            <p className="analysis-text">{analysis.analysis}</p>
          </div>
          {analysis.keywords && (
            <div className="form-group">
              <h3 className="section-title">Keywords</h3>
              <div className="keywords-container">
                {analysis.keywords.map((keyword: string, index: number) => (
                  <span key={index} className="keyword-tag">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
