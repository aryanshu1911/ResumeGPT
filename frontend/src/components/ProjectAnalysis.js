/**
 * ProjectAnalysis.js — Extracted Projects Display
 * =================================================
 * Renders project cards showing name, tech stack, and domain.
 * Also displays achievements and extracurricular activities.
 */
import React from "react";

const ProjectAnalysis = ({ projects, achievements, extracurriculars }) => {
    return (
        <div className="analysis-grid">
            {/* --- Projects Section --- */}
            {projects && projects.length > 0 && (
                <div className="card project-card">
                    <div className="card-header">
                        <div className="card-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
                                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
                            </svg>
                        </div>
                        <h2>Projects</h2>
                        <span className="badge">{projects.length}</span>
                    </div>
                    <div className="project-list">
                        {projects.map((project, index) => (
                            <div
                                key={index}
                                className="project-item"
                                style={{ animationDelay: `${index * 0.1}s` }}
                            >
                                <h3 className="project-name">{project.name}</h3>
                                <span className="project-domain">{project.domain}</span>
                                {project.tech_stack && project.tech_stack.length > 0 && (
                                    <div className="tech-stack">
                                        {project.tech_stack.map((tech, i) => (
                                            <span key={i} className="tech-tag">
                                                {tech}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* --- Achievements Section --- */}
            {achievements && achievements.length > 0 && (
                <div className="card achievement-card">
                    <div className="card-header">
                        <div className="card-icon trophy">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
                                <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
                                <path d="M4 22h16" />
                                <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
                                <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
                                <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" />
                            </svg>
                        </div>
                        <h2>Achievements</h2>
                        <span className="badge">{achievements.length}</span>
                    </div>
                    <ul className="achievement-list">
                        {achievements.map((item, index) => (
                            <li key={index} style={{ animationDelay: `${index * 0.08}s` }}>
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* --- Extracurriculars Section --- */}
            {extracurriculars && extracurriculars.length > 0 && (
                <div className="card extras-card">
                    <div className="card-header">
                        <div className="card-icon extras">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                                <circle cx="9" cy="7" r="4" />
                                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                            </svg>
                        </div>
                        <h2>Extracurriculars</h2>
                        <span className="badge">{extracurriculars.length}</span>
                    </div>
                    <ul className="extras-list">
                        {extracurriculars.map((item, index) => (
                            <li key={index} style={{ animationDelay: `${index * 0.08}s` }}>
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ProjectAnalysis;
