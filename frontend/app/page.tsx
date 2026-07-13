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

  // Sign in with Google
  const handleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      setUser(result.user);
    } catch (err) {
      setError("Login failed. Please try again.");
    }
  };

  // Sign out
  const handleLogout = async () => {
    await signOut(auth);
    setUser(null);
    setReport("");
  };

  // Submit URL and email for analysis
  const handleAnalyze = async () => {
    if (!url) {
      setError("Please enter a URL to analyze.");
      return;
    }

    setLoading(true);
    setError("");
    setReport("");

    try {
      // Get the Firebase token from the logged in user
      const token = await user!.getIdToken();

      // Send to our FastAPI backend
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

  // NOT LOGGED IN — show login screen
  if (!user) {
    return (