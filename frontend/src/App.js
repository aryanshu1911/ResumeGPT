/**
 * App.js — Career Path Analyzer (Main Application) V2
 * ===================================================
 * Root component orchestrating the new V2 visualization components:
 *   - SkillList (categorized)
 *   - CareerCards (dynamic, individual role cards with roadmaps)
 */
import React, { useState } from "react";
import axios from "axios";
import ResumeUpload from "./components/ResumeUpload";
import SkillList from "./components/SkillList";
import ProjectAnalysis from "./components/ProjectAnalysis";
import CareerCard from "./components/CareerCard";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = async (file) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Timeout set to 3 minutes for slow V2 TF loading if needed
      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 180000,
      });

      setResults(response.data);
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.message ||
        "Something went wrong. Please try again.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Background animated elements */}
      <div className="bg-gradient"></div>
      <div className="bg-grid"></div>

      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
              </svg>
            </div>
            <h1>ResumeGPT <span>v2</span></h1>
          </div>
          <p className="tagline">
            AI-Powered Career Advisor
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {/* Upload Section */}
        <ResumeUpload onFileSelect={handleFileSelect} isLoading={isLoading} />

        {/* Error Display */}
        {error && (
          <div className="error-banner">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Results Section */}
        {results && (
          <div className="results-section">
            <div className="results-header">
              <h2>Analysis Results</h2>
              <span className="results-filename">{results.filename}</span>
            </div>

            {/* Categorized Skills */}
            <SkillList skills={results.skills} />

            {/* Projects, Achievements, Extracurriculars */}
            <ProjectAnalysis
              projects={results.projects}
              achievements={results.achievements}
              extracurriculars={results.extracurriculars}
            />

            {/* V2 Career Suggestions rendered as Individual Detailed Cards */}
            {results.career_suggestions && results.career_suggestions.length > 0 && (
              <div className="career-suggestions-container">
                <div className="card-header" style={{ marginBottom: "20px", marginTop: "30px" }}>
                  <div className="card-icon career">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <line x1="18" y1="20" x2="18" y2="10" />
                      <line x1="12" y1="20" x2="12" y2="4" />
                      <line x1="6" y1="20" x2="6" y2="14" />
                    </svg>
                  </div>
                  <h2>Top Career Recommendations</h2>
                </div>
                {results.career_suggestions.map((career, idx) => (
                  <CareerCard key={idx} career={career} />
                ))}
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          Made with ❤️ by Aryanshu Singh •{" "}
          <strong>ResumeGPT</strong>
        </p>
      </footer>
    </div>
  );
}

export default App;
