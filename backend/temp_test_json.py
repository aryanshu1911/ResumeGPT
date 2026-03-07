import sys
import json
from models.resume_parser import parse_resume
from models.resume_ner_model.extractor import extract_entities
from models.career_match_model.matcher import match_career

import logging
logging.basicConfig(level=logging.ERROR)

with open('../data/sample_resumes/sample_resume.txt', 'rb') as f:
    text = parse_resume(f.read(), 'sample_resume.txt')

entities = extract_entities(text)
suggestions = match_career(text, entities, top_n=5)

with open('test_output.json', 'w') as f:
    json.dump(suggestions, f, indent=2)
