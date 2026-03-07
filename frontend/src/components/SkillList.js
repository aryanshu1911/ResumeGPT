/**
 * SkillList.js — Extracted Skills Display V2
 * ========================================
 * Renders detected skills categorized using styled chips.
 */
import React from "react";

const SkillList = ({ skills }) => {
    if (!skills || typeof skills !== 'object' || Object.keys(skills).length === 0) return null;

    // Helper to format category names (e.g., "programming" -> "Programming")
    const formatCategory = (str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    };

    // Calculate total number of skills
    let totalSkills = 0;
    Object.values(skills).forEach(arr => {
        totalSkills += (arr || []).length;
    });

    if (totalSkills === 0) return null;

    return (
        <div className="card skill-card">
            <div className="card-header">
                <div className="card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="16 18 22 12 16 6" />
                        <polyline points="8 6 2 12 8 18" />
                    </svg>
                </div>
                <h2>Skills Detected</h2>
                <span className="badge">{totalSkills}</span>
            </div>

            <div className="skills-categorized">
                {Object.entries(skills).map(([category, items]) => {
                    if (!items || items.length === 0) return null;
                    return (
                        <div key={category} className="skill-category-group">
                            <h4 className="skill-category-title">{formatCategory(category)}</h4>
                            <div className="skill-tags">
                                {items.map((skill, index) => (
                                    <span
                                        key={index}
                                        className={`skill-tag category-${category}`}
                                        style={{ animationDelay: `${index * 0.05}s` }}
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default SkillList;
