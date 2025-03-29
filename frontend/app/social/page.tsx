"use client";
import React from "react";
import { useState } from "react";
import { toast } from "react-toastify";

export default function SocialPage() {
  const [topic, setTopic] = useState("");
  const [platform, setPlatform] = useState("linkedin");
  const [tone, setTone] = useState("professional");
  const [length, setLength] = useState("medium");
  const [content, setContent] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGeneratePost = async () => {
    if (!topic) {
      toast.error("Please enter a topic");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.API_URL}/api/social/generate-post`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topic,
            platform,
            tone,
            length,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Content generation failed");
      }

      const data = await response.json();
      setContent(data);
      toast.success("Content generated successfully!");
    } catch (error) {
      toast.error("Failed to generate content");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateThread = async () => {
    if (!topic) {
      toast.error("Please enter a topic");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.API_URL}/api/social/generate-thread`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topic,
            platform,
            num_tweets: 5,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Thread generation failed");
      }

      const data = await response.json();
      setContent(data);
      toast.success("Thread generated successfully!");
    } catch (error) {
      toast.error("Failed to generate thread");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Social Media Content Generator</h1>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Generate Content</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Topic
            </label>
            <textarea
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="input h-24"
              placeholder="Enter your content topic..."
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Platform
              </label>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                className="input"
              >
                <option value="linkedin">LinkedIn</option>
                <option value="twitter">Twitter</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tone
              </label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="input"
              >
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="enthusiastic">Enthusiastic</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Length
              </label>
              <select
                value={length}
                onChange={(e) => setLength(e.target.value)}
                className="input"
              >
                <option value="short">Short</option>
                <option value="medium">Medium</option>
                <option value="long">Long</option>
              </select>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleGeneratePost}
              disabled={loading || !topic}
              className="btn btn-primary flex-1"
            >
              {loading ? "Generating..." : "Generate Post"}
            </button>
            <button
              onClick={handleGenerateThread}
              disabled={loading || !topic}
              className="btn btn-secondary flex-1"
            >
              {loading ? "Generating..." : "Generate Thread"}
            </button>
          </div>
        </div>
      </div>

      {content && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Generated Content</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium mb-2">Content</h3>
              <div className="bg-gray-50 p-4 rounded-md">
                {platform === "twitter" ? (
                  <div className="space-y-4">
                    {content.thread.map((tweet: string, index: number) => (
                      <div key={index} className="border-b pb-4 last:border-0">
                        <p className="text-gray-800">{tweet}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-800 whitespace-pre-wrap">
                    {content.post}
                  </p>
                )}
              </div>
            </div>

            {content.hashtags && (
              <div>
                <h3 className="font-medium mb-2">Hashtags</h3>
                <div className="flex flex-wrap gap-2">
                  {content.hashtags.map((hashtag: string, index: number) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-sm"
                    >
                      {hashtag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {content.best_time && (
              <div>
                <h3 className="font-medium mb-2">Best Time to Post</h3>
                <p className="text-gray-600">
                  {new Date(
                    content.best_time.next_optimal_time
                  ).toLocaleString()}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
