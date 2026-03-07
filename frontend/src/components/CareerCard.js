/**
 * CareerCard.js — Detailed per-role analysis and visualization
 * =========================================================
 * Displays Fit Score, Reasoning, Radar Chart, Skill Metrics, and Roadmap.
 */
import React from "react";
import { Radar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const CareerCard = ({ career }) => {
    if (!career) return null;

    // Build data for radar chart
    // We want to combine the required skills (matching + missing)
    // Limit to 8 for radar aesthetics, prioritizing missing skills to show gaps clearly
    const radarLabels = [
        ...career.missing_skills.slice(0, 5),
        ...career.matching_skills.slice(0, 3)
    ].slice(0, 8);

    // Filter duplicates just in case
    const uniqueLabels = [...new Set(radarLabels)];

    const radarYou = uniqueLabels.map(label => career.matching_skills.includes(label) ? 1 : 0);
    const radarRole = uniqueLabels.map(() => 1);

    const radarData = {
        labels: uniqueLabels,
        datasets: [
            {
                label: "Your Skills",
                data: radarYou,
                backgroundColor: "rgba(99, 102, 241, 0.2)",
                borderColor: "rgba(99, 102, 241, 0.8)",
                borderWidth: 2,
                pointBackgroundColor: "rgba(99, 102, 241, 1)",
                pointRadius: 4,
            },
            {
                label: "Role Requirements",
                data: radarRole,
                backgroundColor: "rgba(236, 72, 153, 0.1)",
                borderColor: "rgba(236, 72, 153, 0.5)",
                borderWidth: 2,
                borderDash: [5, 5],
                pointBackgroundColor: "rgba(236, 72, 153, 0.8)",
                pointRadius: 3,
            },
        ],
    };

    const radarOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: "#e2e8f0", font: { size: 12 }, usePointStyle: true },
                position: 'bottom',
            },
        },
        scales: {
            r: {
                grid: { color: "rgba(148, 163, 184, 0.15)" },
                angleLines: { color: "rgba(148, 163, 184, 0.15)" },
                ticks: { display: false },
                pointLabels: { color: "#cbd5e1", font: { size: 11 } },
                min: 0,
                max: 1.2,
            },
        },
    };

    return (
        <div className="card career-card">
            {/* Header: Title and Fit Score */}
            <div className="career-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <h2>{career.role}</h2>
                    {career.is_highly_suitable && (
                        <span className="status-chip" style={{ backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981', marginLeft: '10px', fontSize: '0.8rem', padding: '4px 8px' }}>
                            ★ Highly Suitable
                        </span>
                    )}
                </div>
                <div className="fit-score-badge">
                    <span>{career.score}% Fit</span>
                </div>
            </div>

            {/* AI Reasoning */}
            <div className="career-reasoning">
                <div className="reasoning-icon">🤖</div>
                <p>{career.career_recommendation_summary}</p>
            </div>

            {/* Skill Coverage Progress Bar */}
            <div className="coverage-section">
                <div className="coverage-label">
                    <span>Skill Coverage</span>
                    <span>{career.skill_coverage}%</span>
                </div>
                <div className="progress-track">
                    <div
                        className="progress-fill"
                        style={{ width: `${career.skill_coverage}%` }}
                    ></div>
                </div>
            </div>

            <div className="career-body-grid">
                {/* Left: Lists */}
                <div className="career-lists">
                    {career.missing_skills.length > 0 && (
                        <div className="skill-group missing-group">
                            <h4>Missing Skills</h4>
                            <div className="chip-container">
                                {career.missing_skills.map((s, i) => (
                                    <span key={`miss-${i}`} className="status-chip missing">{s}</span>
                                ))}
                            </div>
                        </div>
                    )}

                    {career.matching_skills.length > 0 && (
                        <div className="skill-group matching-group">
                            <h4>Matching Skills</h4>
                            <div className="chip-container">
                                {career.matching_skills.map((s, i) => (
                                    <span key={`match-${i}`} className="status-chip matching">{s}</span>
                                ))}
                            </div>
                        </div>
                    )}

                    {career.transferable_skills.length > 0 && (
                        <div className="skill-group transferable-group">
                            <h4>Transferable Skills</h4>
                            <div className="chip-container">
                                {career.transferable_skills.slice(0, 10).map((s, i) => (
                                    <span key={`trans-${i}`} className="status-chip transferable">{s}</span>
                                ))}
                                {career.transferable_skills.length > 10 && (
                                    <span className="status-chip transferable">+{career.transferable_skills.length - 10} more</span>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                {/* Right: Radar Chart */}
                <div className="career-radar-container">
                    {uniqueLabels.length > 2 ? (
                        <Radar data={radarData} options={radarOptions} />
                    ) : (
                        <div className="not-enough-data">
                            Not enough data points for a radar chart.
                        </div>
                    )}
                </div>
            </div>

            {/* Roadmap */}
            {career.roadmap_steps && career.roadmap_steps.length > 0 && (
                <div className="career-roadmap">
                    <h3>Learning Roadmap</h3>
                    <div className="roadmap-steps">
                        {career.roadmap_steps.map((step, index) => (
                            <div key={index} className="roadmap-step">
                                <div className="step-number">{index + 1}</div>
                                <div className="step-text">{step}</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CareerCard;
