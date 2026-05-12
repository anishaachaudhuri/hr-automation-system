import re
from backend.utils.skills import SKILL_KEYWORDS

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))

def extract_marks(text):
    text = text.lower()

    tenth = None
    twelfth = None
    gpa = None

    # 10th patterns
    tenth_patterns = [
        r"(10th|class x|secondary|ssc|cbse|icse).*?(\d{2,3}\.?\d?)\s?%",
        r"(\d{2,3}\.?\d?)\s?%.*?(10th|class x|secondary)"
    ]

    # 12th patterns
    twelfth_patterns = [
        r"(12th|class xii|senior secondary|hsc|isc|intermediate).*?(\d{2,3}\.?\d?)\s?%",
        r"(\d{2,3}\.?\d?)\s?%.*?(12th|class xii|senior secondary)"
    ]

    # gpa patterns
    gpa_patterns = [
        r"(cgpa|gpa).*?(\d\.\d{1,2})",
        r"(\d\.\d{1,2}).*?(cgpa|gpa)"
    ]

    for pattern in tenth_patterns:
        match = re.search(pattern, text)
        if match:
            for group in match.groups():
                try:
                    tenth = float(group)
                    break
                except:
                    continue
        if tenth:
            break

    for pattern in twelfth_patterns:
        match = re.search(pattern, text)
        if match:
            for group in match.groups():
                try:
                    twelfth = float(group)
                    break
                except:
                    continue
        if twelfth:
            break

    for pattern in gpa_patterns:
        match = re.search(pattern, text)
        if match:
            for group in match.groups():
                try:
                    gpa = float(group)
                    break
                except:
                    continue
        if gpa:
            break

    return {
        "tenth": tenth,
        "twelfth": twelfth,
        "gpa": gpa
    }


MINIMUM_GPA = 8.0

DISALLOWED_BRANCHES = [
    "biotechnology",
    "biotech"
]

RESEARCH_KEYWORDS = [
    "research",
    "research paper",
    "publication",
    "journal",
    "ieee",
    "conference"
]

ACHIEVEMENT_KEYWORDS = [
    "hackathon",
    "winner",
    "award",
    "scholarship",
    "achievement"
]

SCORING_WEIGHTS = {
    "high_gpa": 30,
    "skills": 25,
    "research": 25,
    "achievements": 20
}


def evaluate_candidate(text, marks, skills):

    text = text.lower()

    score = 0
    reasons = []

    gpa = marks.get("gpa")

    if gpa is None or gpa < MINIMUM_GPA:
        return {
            "selected": False,
            "score": 0,
            "reasons": [
                f"GPA below minimum cutoff ({MINIMUM_GPA})"
            ]
        }

    if gpa >= 9:
        score += SCORING_WEIGHTS["high_gpa"]
        reasons.append("Excellent GPA detected")

    elif gpa >= 8:
        score += 20
        reasons.append("Good academic performance")

    for branch in DISALLOWED_BRANCHES:
        if branch in text:
            return {
                "selected": False,
                "score": 0,
                "reasons": [
                    f"Disallowed branch detected: {branch}"
                ]
            }

    skill_score = min(len(skills) * 3, SCORING_WEIGHTS["skills"])

    if skill_score > 0:
        score += skill_score
        reasons.append("Strong technical skill match")

    research_found = False

    for keyword in RESEARCH_KEYWORDS:
        if keyword in text:
            research_found = True
            break

    if research_found:
        score += SCORING_WEIGHTS["research"]
        reasons.append("Research experience detected")

    achievement_found = False

    for keyword in ACHIEVEMENT_KEYWORDS:
        if keyword in text:
            achievement_found = True
            break

    if achievement_found:
        score += SCORING_WEIGHTS["achievements"]
        reasons.append("Achievements/certifications detected")

    return {
        "selected": True,
        "score": score,
        "reasons": reasons
    }