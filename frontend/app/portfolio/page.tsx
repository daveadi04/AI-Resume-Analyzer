"use client";

import React from "react";
import { useState } from "react";
import { toast } from "react-toastify";

export default function PortfolioPage() {
  const [githubUsername, setGithubUsername] = useState("");
  const [userData, setUserData] = useState({
    name: "",
    title: "",
    about: "",
    skills: "",
    experience: "",
  });
  const [portfolio, setPortfolio] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeGithub = async () => {
    if (!githubUsername) {
      toast.error("Please enter a GitHub username");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.API_URL}/api/portfolio/analyze-github`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ github_username: githubUsername }),
        }
      );

      if (!response.ok) {
        throw new Error("GitHub analysis failed");
      }

      const data = await response.json();
      setPortfolio(data);
      toast.success("GitHub profile analyzed successfully!");
    } catch (error) {
      toast.error("Failed to analyze GitHub profile");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePortfolio = async () => {
    if (!userData.name || !userData.title) {
      toast.error("Please fill in the required fields");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.API_URL}/api/portfolio/generate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user_data: userData }),
        }
      );

      if (!response.ok) {
        throw new Error("Portfolio generation failed");
      }

      const data = await response.json();
      setPortfolio(data);
      toast.success("Portfolio generated successfully!");
    } catch (error) {
      toast.error("Failed to generate portfolio");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeploy = async () => {
    if (!portfolio) {
      toast.error("Please generate a portfolio first");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.API_URL}/api/portfolio/deploy`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ portfolio_data: portfolio }),
        }
      );

      if (!response.ok) {
        throw new Error("Deployment failed");
      }

      const data = await response.json();
      toast.success("Portfolio deployed successfully!");
      window.open(data.url, "_blank");
    } catch (error) {
      toast.error("Failed to deploy portfolio");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Portfolio Generator</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Analyze GitHub Profile</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                GitHub Username
              </label>
              <input
                type="text"
                value={githubUsername}
                onChange={(e) => setGithubUsername(e.target.value)}
                className="input"
                placeholder="Enter your GitHub username"
              />
            </div>
            <button
              onClick={handleAnalyzeGithub}
              disabled={loading || !githubUsername}
              className="btn btn-primary w-full"
            >
              {loading ? "Analyzing..." : "Analyze GitHub Profile"}
            </button>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Generate Portfolio</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Name
              </label>
              <input
                type="text"
                value={userData.name}
                onChange={(e) =>
                  setUserData({ ...userData, name: e.target.value })
                }
                className="input"
                placeholder="Your full name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title
              </label>
              <input
                type="text"
                value={userData.title}
                onChange={(e) =>
                  setUserData({ ...userData, title: e.target.value })
                }
                className="input"
                placeholder="Your professional title"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                About
              </label>
              <textarea
                value={userData.about}
                onChange={(e) =>
                  setUserData({ ...userData, about: e.target.value })
                }
                className="input h-24"
                placeholder="Brief introduction about yourself"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Skills
              </label>
              <textarea
                value={userData.skills}
                onChange={(e) =>
                  setUserData({ ...userData, skills: e.target.value })
                }
                className="input h-24"
                placeholder="Your skills (comma-separated)"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Experience
              </label>
              <textarea
                value={userData.experience}
                onChange={(e) =>
                  setUserData({ ...userData, experience: e.target.value })
                }
                className="input h-24"
                placeholder="Your work experience"
              />
            </div>
            <button
              onClick={handleGeneratePortfolio}
              disabled={loading}
              className="btn btn-primary w-full"
            >
              {loading ? "Generating..." : "Generate Portfolio"}
            </button>
          </div>
        </div>
      </div>

      {portfolio && (
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Portfolio Preview</h2>
            <button
              onClick={handleDeploy}
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? "Deploying..." : "Deploy Portfolio"}
            </button>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium mb-2">HTML</h3>
              <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                <code>{portfolio.html}</code>
              </pre>
            </div>
            <div>
              <h3 className="font-medium mb-2">CSS</h3>
              <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                <code>{portfolio.css}</code>
              </pre>
            </div>
            <div>
              <h3 className="font-medium mb-2">JavaScript</h3>
              <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                <code>{portfolio.js}</code>
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
