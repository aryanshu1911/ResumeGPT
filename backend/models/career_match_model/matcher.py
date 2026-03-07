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


def match_career(resume_text: str, entities: dict, top_n: int = 5) -> list:
    """
    Match a resume against predefined career roles using semantic similarity.
    Calculates detailed skill gap analytics per role using full entity context.
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

    # Gather user skills from explicit skills block
    all_user_skills = []
    user_skills_dict = entities.get("skills", {})
    for cat, items in user_skills_dict.items():
        all_user_skills.extend([s.lower() for s in items])

    # Optionally extract implicit skills/tools mentioned in projects or achievements 
    # if they are parsed as dicts or text blocks by NER.
    # Currently, assuming they're lists of strings describing the projects.
    # We heavily rely on the `resume_text` semantic match for these, but we can add
    # basic keyword extraction here if needed in future.
    
    all_user_skills_set = set(all_user_skills)

    # 1. Semantic search
    resume_embedding = _model.encode([resume_text], show_progress_bar=False)
    similarities = cosine_similarity(resume_embedding, _role_embeddings)[0]

    all_roles_evaluated = []

    for idx, role in enumerate(_career_roles):
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

        # 4. Composite Scoring Logic
        # Instead of just using semantic similarity, use a mix of semantic, required skill match, and transferable skill bonus
        semantic_score = score
        # For non-tech roles, semantic score (text context like leadership/projects) matters a lot
        skill_match_score = coverage / 100.0
        transferable_bonus = min(len(transferable_skills) * 0.05, 0.2) # Max 20% bonus from transferable skills
        
        # We increase semantic weight to represent holistic fit to the role description
        composite_score = (semantic_score * 0.6) + (skill_match_score * 0.4) + transferable_bonus
        final_score_pct = min(round(composite_score * 100, 1), 100.0)

        # DEBUG: Print exact raw scores before filtering
        # print(f"DEBUG {role['role']}: cover={coverage}%, semantic={semantic_score:.3f}, comp_pct={final_score_pct}%")

        # Threshold check: Lowered to 25% coverage OR high semantic score to accommodate non-tech roles
        # If semantic score is extremely high (e.g. they describe exactly what a PM does), let them through even with low extracted keywords
        # The previous bug: we were ANDing them, so it required BOTH < 25 AND < 0.4 to be skipped
        if coverage < 25 and semantic_score < 0.35:
            continue

        # Highly suitable flag
        is_highly_suitable = final_score_pct >= 80 or coverage >= 80

        # 5. Generate Reasoning
        if coverage >= 80:
            reason = f"Excellent fit! Your resume highly correlates with the {role['role']} profile. You have strong coverage in core skills."
        elif coverage > 40:
            reason = f"Good match. You have foundational skills like {', '.join(matching_formatted[:2])}, but need to acquire {', '.join(missing_formatted[:2])}."
        else:
            reason = f"Emerging match. You have transferable technical knowledge, but lack core domain expertise in tools like {', '.join(missing_formatted[:3])}."

        all_roles_evaluated.append({
            "role": role["role"],
            "score": final_score_pct,  # Use our new composite score
            "skill_coverage": coverage,
            "matching_skills": matching_formatted,
            "missing_skills": missing_formatted,
            "transferable_skills": transferable_formatted,
            "career_recommendation_summary": reason,
            "roadmap_steps": role.get("roadmap_steps", []),
            "is_highly_suitable": is_highly_suitable
        })

    # Sort strictly by skill_coverage (descending) then by score
    all_roles_evaluated.sort(key=lambda x: (x["skill_coverage"], x["score"]), reverse=True)

    # Return top N roles
    return all_roles_evaluated[:top_n]
