"""
extractor.py — Resume Entity Extractor (NER + Heuristics) V2
==========================================================
Detects resume sections and extracts structured entities dynamically categorized:
  - Skills (categorized into programming, frameworks, tools, platforms, security, data)
  - Projects (name, tech stack, domain)
  - Achievements (awards, certifications, competitions)
  - Extracurriculars (clubs, volunteering, leadership)
"""

import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ---------------------------------------------------------------------------
# Categorized Skill Dictionaries & Normalization Maps
# ---------------------------------------------------------------------------
# Key = Exact matched word in lowercase, Value = Normalized/Display name
SKILL_CATEGORIES = {
    "programming": {
        "python": "Python", "javascript": "JavaScript", "js": "JavaScript", 
        "java": "Java", "c++": "C++", "cpp": "C++", "c#": "C#", "csharp": "C#",
        "c": "C", "typescript": "TypeScript", "ts": "TypeScript", "go": "Go", 
        "golang": "Go", "rust": "Rust", "ruby": "Ruby", "php": "PHP", 
        "swift": "Swift", "kotlin": "Kotlin", "dart": "Dart", "r": "R",
        "scala": "Scala", "solidity": "Solidity", "bash": "Bash", "shell": "Bash"
    },
    "frameworks": {
        "react": "React", "react.js": "React", "reactjs": "React", 
        "angular": "Angular", "vue": "Vue", "vue.js": "Vue", 
        "next.js": "Next.js", "nextjs": "Next.js", "node.js": "Node.js", 
        "nodejs": "Node.js", "express": "Express", "django": "Django",
        "flask": "Flask", "fastapi": "FastAPI", "spring": "Spring", 
        "spring boot": "Spring Boot", ".net": " .NET", "laravel": "Laravel",
        "tailwind": "Tailwind CSS", "bootstrap": "Bootstrap", "sass": "Sass"
    },
    "tools": {
        "git": "Git", "github": "GitHub", "gitlab": "GitLab", "docker": "Docker",
        "kubernetes": "Kubernetes", "k8s": "Kubernetes", "jenkins": "Jenkins",
        "terraform": "Terraform", "ansible": "Ansible", "webpack": "Webpack",
        "vite": "Vite", "postman": "Postman", "figma": "Figma", "jira": "Jira",
        "excel": "Excel"
    },
    "platforms": {
        "aws": "AWS", "azure": "Azure", "gcp": "GCP", "linux": "Linux",
        "ubuntu": "Linux", "windows server": "Windows Server", "vercel": "Vercel",
        "heroku": "Heroku", "firebase": "Firebase", "android": "Android", "ios": "iOS"
    },
    "security": {
        "wireshark": "Wireshark", "nmap": "Nmap", "burp suite": "Burp Suite",
        "metasploit": "Metasploit", "splunk": "Splunk", "siem": "SIEM",
        "owasp": "OWASP", "owasp zap": "OWASP ZAP", "cryptography": "Cryptography",
        "penetration testing": "Penetration Testing"
    },
    "data": {
        "sql": "SQL", "postgresql": "PostgreSQL", "mysql": "MySQL", "mongodb": "MongoDB",
        "redis": "Redis", "tensorflow": "TensorFlow", "tf": "TensorFlow",
        "pytorch": "PyTorch", "scikit-learn": "Scikit-Learn", "sklearn": "Scikit-Learn",
        "pandas": "Pandas", "numpy": "Numpy", "keras": "Keras", "tableau": "Tableau",
        "power bi": "Power BI", "matplotlib": "Matplotlib", "seaborn": "Seaborn",
        "jupyter": "Jupyter", "hadoop": "Hadoop", "spark": "Apache Spark"
    }
}

# ---------------------------------------------------------------------------
# Section heading patterns
# ---------------------------------------------------------------------------
SECTION_PATTERNS = {
    "skills": re.compile(r"^[=\-\s]*(?:technical\s+)?skills[=\-\s]*$", re.IGNORECASE),
    "projects": re.compile(r"^[=\-\s]*(?:technical\s+|academic\s+)?projects[=\-\s]*$", re.IGNORECASE),
    "achievements": re.compile(r"^[=\-\s]*(?:achievements?|awards?|honors?|certifications?)[=\-\s]*$", re.IGNORECASE),
    "extracurriculars": re.compile(r"^[=\-\s]*(?:extracurricular(?:\s+activities)?|activities|clubs?|volunteering|leadership)[=\-\s]*$", re.IGNORECASE),
    "education": re.compile(r"^[=\-\s]*education[=\-\s]*$", re.IGNORECASE),
    "experience": re.compile(r"^[=\-\s]*(?:work\s+)?experience[=\-\s]*$", re.IGNORECASE),
}

def _split_sections(text: str) -> dict:
    lines = text.split("\n")
    sections = {"__header__": []}
    current_section = "__header__"

    for line in lines:
        stripped = line.strip()
        if stripped and all(c in "=-_* " for c in stripped):
            continue

        matched = False
        for section_name, pattern in SECTION_PATTERNS.items():
            if pattern.match(stripped):
                current_section = section_name
                if section_name not in sections:
                    sections[section_name] = []
                matched = True
                break

        if not matched:
            if current_section not in sections:
                sections[current_section] = []
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if v}


def _extract_skills_categorized(text: str) -> dict:
    text_lower = text.lower()
    # To handle things like .net, react.js -> pad with spaces to use word boundaries safely
    # Or just use regex boundaries
    
    categorized_skills = {
        "programming": set(),
        "frameworks": set(),
        "tools": set(),
        "platforms": set(),
        "security": set(),
        "data": set()
    }

    for category, category_dict in SKILL_CATEGORIES.items():
        for keyword, normalized_name in category_dict.items():
            # word boundary matching. Note: \b doesn't work well with ".net" or "c++"
            if not keyword[0].isalnum() or not keyword[-1].isalnum():
                pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
            else:
                pattern = r"\b" + re.escape(keyword) + r"\b"
            
            if re.search(pattern, text_lower):
                categorized_skills[category].add(normalized_name)

    # Convert sets to sorted lists
    return {k: sorted(list(v)) for k, v in categorized_skills.items()}


def _extract_projects(text: str) -> list:
    projects = []
    blocks = re.split(r"\n\s*\d+\.\s+", text)
    
    for block in blocks:
        block = block.strip()
        if not block or len(block) < 10:
            continue
        project = {"name": "", "tech_stack": [], "domain": "General"}
        lines = block.split("\n")
        project["name"] = lines[0].strip().rstrip(":")
        
        tech_match = re.search(r"tech\s*stack\s*:\s*(.+)", block, re.IGNORECASE)
        if tech_match:
            project["tech_stack"] = [t.strip() for t in tech_match.group(1).split(",")]
            
        domain_match = re.search(r"domain\s*:\s*(.+)", block, re.IGNORECASE)
        if domain_match:
            project["domain"] = domain_match.group(1).strip()
            
        projects.append(project)
    return projects


def _extract_list_items(text: str) -> list:
    items = []
    for line in text.split("\n"):
        line = line.strip().lstrip("-*•").strip()
        if line and len(line) > 5:
            items.append(line)
    return items


def extract_entities(resume_text: str) -> dict:
    sections = _split_sections(resume_text)
    
    categorized_skills = _extract_skills_categorized(resume_text)
    
    projects_text = sections.get("projects", "")
    projects = _extract_projects(projects_text) if projects_text else []
    
    achievements_text = sections.get("achievements", "")
    achievements = _extract_list_items(achievements_text) if achievements_text else []
    
    extras_text = sections.get("extracurriculars", "")
    extracurriculars = _extract_list_items(extras_text) if extras_text else []
    
    return {
        "skills": categorized_skills,
        "projects": projects,
        "achievements": achievements,
        "extracurriculars": extracurriculars,
    }
