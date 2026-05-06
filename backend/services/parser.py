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