import re

from backend.utils.skills import (
    SKILL_KEYWORDS
)

from backend.auth_db import (
    get_requirements
)


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

    tenth_patterns = [
    r"(10th|class x|secondary|ssc|cbse|icse).*?(\d{2,3}\.?\d?)\s?%",
    r"(\d{2,3}\.?\d?)\s?%.*?(10th|class x|secondary)"
]

    twelfth_patterns = [
        r"(12th|class xii|senior secondary|hsc|isc|intermediate).*?(\d{2,3}\.?\d?)\s?%",
        r"(\d{2,3}\.?\d?)\s?%.*?(12th|class xii|senior secondary)"
    ]

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


def evaluate_candidate(
    text,
    marks,
    skills
):

    text = text.lower()

    requirements = get_requirements()

    minimum_gpa = (
        requirements["minimum_gpa"]
    )

    required_skills = [

        skill.strip().lower()

        for skill in (
            requirements["required_skills"] or ""
        ).split(",")

        if skill.strip()
    ]

    preferred_skills = [

        skill.strip().lower()

        for skill in (
            requirements["preferred_skills"] or ""
        ).split(",")

        if skill.strip()
    ]

    disallowed_branches = [

        branch.strip().lower()

        for branch in (
            requirements["disallowed_branches"] or ""
        ).split(",")

        if branch.strip()
    ]

    weights = {

        "skills":
            requirements["skill_weight"],

        "gpa":
            requirements["gpa_weight"],

        "research":
            requirements["research_weight"],

        "achievement":
            requirements["achievement_weight"]
    }

    score = 0

    reasons = []

    gpa = marks.get("gpa")

    if gpa is None or gpa < minimum_gpa:

        return {
            "selected": False,
            "score": 0,
            "reasons": [
                "GPA below threshold"
            ]
        }

    score += (
        (gpa / 10)
        * weights["gpa"]
    )

    reasons.append(
        "Academic score matched"
    )

    for branch in disallowed_branches:

        if branch in text:

            return {
                "selected": False,
                "score": 0,
                "reasons": [
                    f"Disallowed branch: {branch}"
                ]
            }

    matched_required = 0

    for skill in required_skills:

        if skill in skills:

            matched_required += 1

    matched_preferred = 0

    for skill in preferred_skills:

        if skill in skills:

            matched_preferred += 1

    total_skill_score = (
        matched_required * 8
        + matched_preferred * 4
    )

    total_skill_score = min(
        total_skill_score,
        weights["skills"]
    )

    score += total_skill_score

    if total_skill_score > 0:

        reasons.append(
            "Skill match detected"
        )

    research_keywords = [
        "research",
        "publication",
        "ieee",
        "journal"
    ]

    for keyword in research_keywords:

        if keyword in text:

            score += weights["research"]

            reasons.append(
                "Research experience detected"
            )

            break

    achievement_keywords = [
        "winner",
        "award",
        "scholarship",
        "hackathon"
    ]

    for keyword in achievement_keywords:

        if keyword in text:

            score += weights["achievement"]

            reasons.append(
                "Achievements detected"
            )

            break

    return {
        "selected": True,
        "score": round(score, 2),
        "reasons": reasons
    }