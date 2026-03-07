/**
 * CareerChart.js — Career Fit Score Visualization
 * =================================================
 * Uses Chart.js (via react-chartjs-2) to render:
 *   1. A horizontal bar chart of career fit scores.
 *   2. A radar chart showing skill coverage vs gaps for the top match.
 */
import React from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
} from "chart.js";
import { Bar, Radar } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
);

const CareerChart = ({ careerSuggestions, skills }) => {
    if (!careerSuggestions || careerSuggestions.length === 0) return null;

    // --- Bar Chart: Career Fit Scores ---
    const barData = {
        labels: careerSuggestions.map((c) => c.role),
        datasets: [
            {
                label: "Fit Score (%)",
                data: careerSuggestions.map((c) => c.score),
                backgroundColor: [
                    "rgba(99, 102, 241, 0.8)",
                    "rgba(168, 85, 247, 0.8)",
                    "rgba(236, 72, 153, 0.8)",
                ],
                borderColor: [
                    "rgba(99, 102, 241, 1)",
                    "rgba(168, 85, 247, 1)",
                    "rgba(236, 72, 153, 1)",
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
            },
        ],
    };

    const barOptions = {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: "rgba(15, 23, 42, 0.95)",
                titleColor: "#e2e8f0",
                bodyColor: "#e2e8f0",
                borderColor: "rgba(99, 102, 241, 0.3)",
                borderWidth: 1,
                cornerRadius: 8,
                padding: 12,
            },
        },
        scales: {
            x: {
                min: 0,
                max: 100,
                grid: { color: "rgba(148, 163, 184, 0.1)" },
                ticks: { color: "#94a3b8", font: { size: 12 } },
            },
            y: {
                grid: { display: false },
                ticks: { color: "#e2e8f0", font: { size: 13, weight: "500" } },
            },
        },
    };

    // --- Radar Chart: Skill Coverage for Top Match ---
    const topMatch = careerSuggestions[0];
    const skillsLower = (skills || []).map((s) => s.toLowerCase());

    // Pick up to 8 skill gaps + matched skills for the radar
    const radarLabels = [
        ...skillsLower.slice(0, 5).map((s) => s.charAt(0).toUpperCase() + s.slice(1)),
        ...topMatch.skill_gaps
            .slice(0, 5)
            .map((s) => s.charAt(0).toUpperCase() + s.slice(1)),
    ].slice(0, 10);

    const radarYou = radarLabels.map((label) =>
        skillsLower.includes(label.toLowerCase()) ? 1 : 0
    );
    const radarRole = radarLabels.map(() => 1); // All required

    const radarData = {
        labels: radarLabels,
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
                label: `${topMatch.role} Requirements`,
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
            },
        },
        scales: {
            r: {
                grid: { color: "rgba(148, 163, 184, 0.15)" },
                angleLines: { color: "rgba(148, 163, 184, 0.15)" },
                ticks: { display: false },
                pointLabels: { color: "#cbd5e1", font: { size: 11 } },
                min: 0,
                max: 1,
            },
        },
    };

    return (
        <div className="career-section">
            <div className="card career-card">
                <div className="card-header">
                    <div className="card-icon career">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="18" y1="20" x2="18" y2="10" />
                            <line x1="12" y1="20" x2="12" y2="4" />
                            <line x1="6" y1="20" x2="6" y2="14" />
                        </svg>
                    </div>
                    <h2>Career Path Suggestions</h2>
                </div>

                {/* Career fit rankings */}
                <div className="career-rankings">
                    {careerSuggestions.map((career, index) => (
                        <div key={index} className="career-rank-item">
                            <div className="rank-badge">#{index + 1}</div>
                            <div className="rank-info">
                                <h3>{career.role}</h3>
                                <div className="score-bar-container">
                                    <div
                                        className="score-bar-fill"
                                        style={{ width: `${career.score}%` }}
                                    ></div>
                                </div>
                            </div>
                            <div className="rank-score">{career.score}%</div>
                        </div>
                    ))}
                </div>

                {/* Bar chart */}
                <div className="chart-container">
                    <h3>Fit Score Comparison</h3>
                    <div style={{ height: "200px" }}>
                        <Bar data={barData} options={barOptions} />
                    </div>
                </div>
            </div>

            {/* Radar chart */}
            <div className="card radar-card">
                <div className="card-header">
                    <div className="card-icon radar">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10" />
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                        </svg>
                    </div>
                    <h2>Skill Gap Analysis — {topMatch.role}</h2>
                </div>
                <div style={{ height: "320px" }}>
                    <Radar data={radarData} options={radarOptions} />
                </div>

                {/* Skill gaps list */}
                {topMatch.skill_gaps && topMatch.skill_gaps.length > 0 && (
                    <div className="skill-gaps">
                        <h3>Skills to Develop</h3>
                        <div className="gap-tags">
                            {topMatch.skill_gaps.map((gap, i) => (
                                <span key={i} className="gap-tag">
                                    {gap}
                                </span>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CareerChart;
