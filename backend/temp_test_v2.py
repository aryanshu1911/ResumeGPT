import sys
import json
from models.resume_parser import parse_resume
from models.resume_ner_model.extractor import extract_entities
from models.career_match_model.matcher import match_career

import logging
logging.basicConfig(level=logging.ERROR)

print('--- V2 Backend Test ---')
print('Loading resume...')
with open('../data/sample_resumes/sample_resume.txt', 'rb') as f:
    text = parse_resume(f.read(), 'sample_resume.txt')

print('Extracting entities...')
entities = extract_entities(text)

skills = entities.get('skills', {})
print(f"Programming: {len(skills.get('programming', []))}")
print(f"Frameworks: {len(skills.get('frameworks', []))}")
print(f"Data: {len(skills.get('data', []))}")

print('Matching careers...')
suggestions = match_career(text, entities['skills'], top_n=3)

for s in suggestions:
    print(f"\n>> {s['role']} (Fit: {s['score']}%)")
    print(f"Recommendation: {s['career_recommendation_summary']}")
    print(f"Coverage: {s['skill_coverage']}%")
    print(f"Matching: {', '.join(s['matching_skills'])}")
    print(f"Missing (Gaps): {', '.join(s['missing_skills'])}")
    print(f"Transferable: {', '.join(s['transferable_skills'])}")
    print(f"Roadmap Steps: {len(s['roadmap_steps'])}")

print('\nDone!')
