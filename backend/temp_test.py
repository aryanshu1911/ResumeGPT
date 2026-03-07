import sys
from models.resume_parser import parse_resume
from models.resume_ner_model.extractor import extract_entities
from models.career_match_model.matcher import match_career

import logging
logging.basicConfig(level=logging.ERROR)

print('Loading resume...')
with open('../data/sample_resumes/sample_resume.txt', 'rb') as f:
    text = parse_resume(f.read(), 'sample_resume.txt')

print('Extracting entities...')
entities = extract_entities(text)
print(f"Found {len(entities['skills'])} skills, {len(entities['projects'])} projects.")
print("Skills:", entities['skills'])

print('Matching careers...')
suggestions = match_career(text, top_n=3)
for s in suggestions:
    print(f" - {s['role']} (Score: {s['score']}%)")
print("Done!")
