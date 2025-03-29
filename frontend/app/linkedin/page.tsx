"use client";

import React, { useState } from "react";
import { toast } from "react-toastify";

// Get API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export default function LinkedInPage() {
  const [profileUrl, setProfileUrl] = useState("");
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeProfile = async () => {
    if (!profileUrl) {
      toast.error("Please enter a LinkedIn profile URL");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/linkedin/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ profile_url: profileUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.status === "not_configured") {
          toast.warning(
            "LinkedIn integration is not configured. Some features may be limited."
          );
          return;
        }
        throw new Error(data.error || "Failed to analyze profile");
      }

      setAnalysis(data);
      toast.success("Profile analyzed successfully!");
    } catch (error) {
      toast.error(error.message || "Failed to analyze profile");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">LinkedIn Profile Analysis</h1>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Analyze Your Profile</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              LinkedIn Profile URL
            </label>
            <input
              type="url"
              value={profileUrl}
              onChange={(e) => setProfileUrl(e.target.value)}
              className="input"
              placeholder="https://www.linkedin.com/in/your-profile"
            />
          </div>

          <button
            onClick={handleAnalyzeProfile}
            disabled={loading || !profileUrl}
            className="btn btn-primary w-full"
          >
            {loading ? "Analyzing..." : "Analyze Profile"}
          </button>
        </div>
      </div>

      {analysis && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium mb-2">Profile Analysis</h3>
              <p className="text-gray-600 whitespace-pre-wrap">
                {analysis.analysis}
              </p>
            </div>

            <div>
              <h3 className="font-medium mb-2">Keywords</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.keywords.map((keyword: string, index: number) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Optimization Suggestions</h3>
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
