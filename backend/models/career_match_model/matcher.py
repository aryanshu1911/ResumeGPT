"""
matcher.py — Career Path Matcher (Semantic Embeddings) V2
=======================================================
Uses Sentence Transformers to compute semantic similarity between
the user's resume and predefined career role descriptions.

V2 Upgrades:
  - Precomputes role embeddings instantly.
  - Returns categorized matching, missing, and transferable skills.
  - Calculates skill_coverage percentage.
  - Returns reasoning summary.
  - Returns roadmap steps.
"""

import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
CAREER_ROLES_PATH = os.path.join(_DATA_DIR, "career_roles.json")

MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading SentenceTransformer Model...")
# Pre-initialize globally so it only boots once in Uvicorn
try:
    _model = SentenceTransformer(MODEL_NAME)
except Exception:
    _model = None  # Will lazy-load if initial fails

# Load and process career roles
with open(CAREER_ROLES_PATH, "r", encoding="utf-8") as f:
    _career_roles = json.load(f)

print("Precomputing semantic embeddings for all career roles...")
if _model:
    role_texts = [
        f"{role['role']}. {role['description']} "
        f"Keywords: {', '.join(role.get('keywords', role.get('required_skills', [])))}"
        for role in _career_roles
    ]
    _role_embeddings = _model.encode(role_texts, show_progress_bar=False)
else:
    _role_embeddings = None


def match_career(resume_text: str, user_categorized_skills: dict, top_n: int = 3) -> list:
    """
    Match a resume against predefined career roles using semantic similarity.
    Calculates detailed skill gap analytics per role.
    """
    global _model, _role_embeddings
    if not _model:
        _model = SentenceTransformer(MODEL_NAME)
        role_texts = [
            f"{role['role']}. {role['description']} "
            f"Keywords: {', '.join(role.get('keywords', role.get('required_skills', [])))}"
            for role in _career_roles
        ]
        _role_embeddings = _model.encode(role_texts, show_progress_bar=False)

    # Flatten user skills for easy matching
    all_user_skills = []
    for cat, items in user_categorized_skills.items():
        all_user_skills.extend([s.lower() for s in items])

    all_user_skills_set = set(all_user_skills)

    # 1. Semantic search
    resume_embedding = _model.encode([resume_text], show_progress_bar=False)
    similarities = cosine_similarity(resume_embedding, _role_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_n]

    results = []

    for idx in top_indices:
        role = _career_roles[idx]
        score = float(similarities[idx])

        # Get the role requirements
        reqs = set([s.lower() for s in role.get("required_skills", []) + role.get("tools", [])])
        
        # 2. Match Analysis
        matching_skills = all_user_skills_set.intersection(reqs)
        missing_skills = reqs - all_user_skills_set
        transferable_skills = all_user_skills_set - reqs

        # Formatter helper
        def format_skill_names(skill_set, lookup_list):
            formatted = []
            for s in skill_set:
                # Find matching capitalization from the actual role list
                found = next((orig for orig in lookup_list if orig.lower() == s), None)
                if found:
                    formatted.append(found)
                else:
                    # Title case fallback
                    formatted.append(s.title() if len(s) > 3 else s.upper())
            return sorted(list(set(formatted)))

        role_list_orig = role.get("required_skills", []) + role.get("tools", [])
        
        matching_formatted = format_skill_names(matching_skills, role_list_orig)
        missing_formatted = format_skill_names(missing_skills, role_list_orig)
        transferable_formatted = sorted(list(set([s.title() if len(s) > 3 else s.upper() for s in transferable_skills])))

        # 3. Coverage Math
        coverage = 0
        if len(reqs) > 0:
            coverage = round((len(matching_skills) / len(reqs)) * 100, 1)

        # 4. Generate Reasoning
        if coverage > 70:
            reason = f"Excellent fit! Your resume highly correlates with the {role['role']} profile. You have strong coverage in core skills."
        elif coverage > 40:
            reason = f"Good match. You have foundational skills like {', '.join(matching_formatted[:2])}, but need to acquire {', '.join(missing_formatted[:2])}."
        else:
            reason = f"Emerging match. You have transferable technical knowledge, but lack core domain expertise in tools like {', '.join(missing_formatted[:3])}."

        results.append({
            "role": role["role"],
            "score": round(score * 100, 1),
            "skill_coverage": coverage,
            "matching_skills": matching_formatted,
            "missing_skills": missing_formatted,
            "transferable_skills": transferable_formatted,
            "career_recommendation_summary": reason,
            "roadmap_steps": role.get("roadmap_steps", [])
        })

    return results
