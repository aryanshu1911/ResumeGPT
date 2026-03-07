/**
 * ResumeUpload.js — Drag-and-Drop Resume Upload Component
 * ========================================================
 * Provides a styled file upload area with drag-and-drop support.
 * Accepts PDF, DOCX, and TXT files. Shows loading state during analysis.
 */
import React, { useCallback, useState } from "react";

const ResumeUpload = ({ onFileSelect, isLoading }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(
        (e) => {
            e.preventDefault();
            setIsDragging(false);
            const file = e.dataTransfer.files[0];
            if (file) {
                setSelectedFile(file);
                onFileSelect(file);
            }
        },
        [onFileSelect]
    );

    const handleFileInput = useCallback(
        (e) => {
            const file = e.target.files[0];
            if (file) {
                setSelectedFile(file);
                onFileSelect(file);
            }
        },
        [onFileSelect]
    );

    return (
        <div className="upload-section">
            <div
                className={`upload-zone ${isDragging ? "dragging" : ""} ${isLoading ? "loading" : ""
                    }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() =>
                    !isLoading && document.getElementById("file-input").click()
                }
            >
                <input
                    id="file-input"
                    type="file"
                    accept=".pdf,.docx,.txt"
                    onChange={handleFileInput}
                    style={{ display: "none" }}
                />

                {isLoading ? (
                    <div className="upload-loading">
                        <div className="spinner"></div>
                        <p>Analyzing your resume with AI...</p>
                        <span className="upload-subtitle">
                            This may take a moment on first run
                        </span>
                    </div>
                ) : (
                    <div className="upload-content">
                        <div className="upload-icon">
                            <svg
                                width="48"
                                height="48"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                <polyline points="17 8 12 3 7 8" />
                                <line x1="12" y1="3" x2="12" y2="15" />
                            </svg>
                        </div>
                        <p className="upload-title">
                            {selectedFile
                                ? selectedFile.name
                                : "Drop your resume here or click to browse"}
                        </p>
                        <span className="upload-subtitle">
                            Supports PDF, DOCX, and TXT files
                        </span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ResumeUpload;
