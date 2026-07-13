"use client";

import { useState } from "react";
import { auth, googleProvider } from "./firebase";
import { signInWithPopup, signOut, User } from "firebase/auth";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [url, setUrl] = useState("");
  const [emailText, setEmailText] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      setUser(result.user);
    } catch (err) {
      setError("Login failed. Please try again.");
    }
  };

  const handleLogout = async () => {
    await signOut(auth);
    setUser(null);
    setReport("");
  };

  const handleAnalyze = async () => {
    if (!url) {
      setError("Please enter a URL to analyze.");
      return;
    }

    setLoading(true);
    setError("");
    setReport("");

    try {
      const token = await user!.getIdToken();

      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          url: url,
          email_text: emailText
        })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setReport(data.report);

    } catch (err: any) {
      setError(`Analysis failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <main className="min-h-screen bg-gray-950 flex flex-col items-center justify-center">
        <div className="text-center space-y-6">
          <h1 className="text-4xl font-bold text-white">phishnet</h1>
          <p className="text-gray-400 text-lg">AI-powered phishing detection platform</p>
          <button
            onClick={handleLogin}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg transition"
          >
            Sign in with Google
          </button>
          {error && <p className="text-red-400">{error}</p>}
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white p-8">

      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-blue-400">phishnet</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-400 text-sm">{user.email}</span>
          <button
            onClick={handleLogout}
            className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition"
          >
            Sign Out
          </button>
        </div>
      </div>

      <div className="max-w-2xl mx-auto space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Suspicious URL</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://suspicious-link.com"
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Email Body <span className="text-gray-600">(optional)</span>
          </label>
          <textarea
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
            placeholder="Paste the suspicious email text here..."
            rows={5}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none"
          />
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition"
        >
          {loading ? "Analyzing... (this takes ~20 seconds)" : "Analyze"}
        </button>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}
      </div>

      {report && (
        <div className="max-w-2xl mx-auto mt-8 bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-blue-400 mb-4">Threat Report</h2>
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown>{report}</ReactMarkdown>
          </div>
        </div>
      )}

    </main>
  );
}