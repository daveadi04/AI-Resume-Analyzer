"use client";

import React, { useState } from "react";
import { toast } from "react-toastify";

export default function InterviewPage() {
  const [jobDescription, setJobDescription] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [numQuestions, setNumQuestions] = useState(10);
  const [questions, setQuestions] = useState<any>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<any>(null);
  const [response, setResponse] = useState("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateQuestions = async () => {
    if (!jobDescription) {
      toast.error("Please enter a job description");
      return;
    }

    setLoading(true);
    try {
      const apiResponse = await fetch(
        `${process.env.API_URL}/api/interview/generate-questions`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            job_description: jobDescription,
            difficulty,
            num_questions: numQuestions,
          }),
        }
      );

      if (!apiResponse.ok) {
        throw new Error("Failed to generate questions");
      }

      const data = await apiResponse.json();
      setQuestions(data);
      toast.success("Questions generated successfully!");
    } catch (error) {
      toast.error("Failed to generate questions");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeResponse = async () => {
    if (!response || !selectedQuestion) {
      toast.error("Please provide a response");
      return;
    }

    setLoading(true);
    try {
      const apiResponse = await fetch(
        `${process.env.API_URL}/api/interview/analyze-response`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: selectedQuestion,
            response,
            job_context: { job_description: jobDescription },
          }),
        }
      );

      if (!apiResponse.ok) {
        throw new Error("Failed to analyze response");
      }

      const data = await apiResponse.json();
      setAnalysis(data);
      toast.success("Response analyzed successfully!");
    } catch (error) {
      toast.error("Failed to analyze response");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Interview Preparation</h1>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">
          Generate Interview Questions
        </h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="input h-32"
              placeholder="Paste the job description here..."
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty
              </label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="input"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Questions
              </label>
              <input
                type="number"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                min="1"
                max="20"
                className="input"
              />
            </div>
          </div>

          <button
            onClick={handleGenerateQuestions}
            disabled={loading || !jobDescription}
            className="btn btn-primary w-full"
          >
            {loading ? "Generating..." : "Generate Questions"}
          </button>
        </div>
      </div>

      {questions && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Practice Questions</h2>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {questions.questions.map((question: string, index: number) => (
                <div
                  key={index}
                  className={`p-4 rounded-md cursor-pointer transition-colors ${
                    selectedQuestion === question
                      ? "bg-primary-100 border-primary-500"
                      : "bg-gray-50 hover:bg-gray-100"
                  }`}
                  onClick={() => setSelectedQuestion(question)}
                >
                  <p className="text-gray-800">{question}</p>
                </div>
              ))}
            </div>

            {selectedQuestion && (
              <div className="mt-6">
                <h3 className="font-medium mb-2">Your Response</h3>
                <textarea
                  value={response}
                  onChange={(e) => setResponse(e.target.value)}
                  className="input h-32"
                  placeholder="Type your response here..."
                />
                <button
                  onClick={handleAnalyzeResponse}
                  disabled={loading || !response}
                  className="btn btn-primary mt-4"
                >
                  {loading ? "Analyzing..." : "Analyze Response"}
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {analysis && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Response Analysis</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium mb-2">Analysis</h3>
              <p className="text-gray-600 whitespace-pre-wrap">
                {analysis.analysis}
              </p>
            </div>

            <div>
              <h3 className="font-medium mb-2">Score</h3>
              <div className="flex items-center">
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div
                    className="bg-primary-600 h-2.5 rounded-full"
                    style={{ width: `${analysis.score}%` }}
                  ></div>
                </div>
                <span className="ml-4 text-gray-600">{analysis.score}%</span>
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Suggestions for Improvement</h3>
              <ul className="list-disc list-inside space-y-2">
                {analysis.suggestions.map(
                  (suggestion: string, index: number) => (
                    <li key={index} className="text-gray-600">
                      {suggestion}
                    </li>
                  )
                )}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
