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

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return list(set(found_skills))


def extract_marks(text):

    text = text.lower()

    tenth = None
    twelfth = None
    gpa = None

    lines = [

        line.strip()

        for line in text.split("\n")

        if line.strip()
    ]

    percentage_pattern = (
        r"(\d{2,3}(?:\.\d{1,2})?)\s?%"
    )

    tenth_keywords = [
        "10th",
        "class x",
        "secondary",
        "ssc",
        "matriculation"
    ]

    twelfth_keywords = [
        "12th",
        "class xii",
        "senior secondary",
        "hsc",
        "isc",
        "intermediate"
    ]

    for i, line in enumerate(lines):

        current_window = " ".join(

            lines[
                max(0, i - 1):
                min(len(lines), i + 3)
            ]
        )

        if any(
            keyword in current_window
            for keyword in tenth_keywords
        ):

            percentages = re.findall(
                percentage_pattern,
                current_window
            )

            if percentages:

                tenth = max(
                    [
                        float(p)
                        for p in percentages
                    ]
                )

        if any(
            keyword in current_window
            for keyword in twelfth_keywords
        ):

            percentages = re.findall(
                percentage_pattern,
                current_window
            )

            if percentages:

                twelfth = max(
                    [
                        float(p)
                        for p in percentages
                    ]
                )

    gpa_patterns = [

        r"(cgpa|gpa).*?(\d\.\d{1,2})",

        r"(\d\.\d{1,2}).*?(cgpa|gpa)"
    ]

    for pattern in gpa_patterns:

        match = re.search(
            pattern,
            text
        )

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
    skills,
    semantic_result,
    sections
):

    text = text.lower()
    education_text = sections.get(
        "education",
        ""
    ).lower()
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
            requirements["achievement_weight"],

        "semantic":
            20
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

    academic_score = (
        (gpa / 10)
        * weights["gpa"]
    )

    score += academic_score

    reasons.append(
        f"Academic score contribution: {round(academic_score, 2)}"
    )

    for branch in disallowed_branches:

        pattern = (
            r"\b"
            + re.escape(branch.lower())
            + r"\b"
        )

        if re.search(
            pattern,
            education_text
        ):

            return {
                "selected": False,
                "score": 0,
                "reasons": [
                    f"Disallowed branch: {branch}"
                ]
            }

    matched_required = []

    for skill in required_skills:

        if skill in skills:

            matched_required.append(
                skill
            )

    matched_preferred = []

    for skill in preferred_skills:

        if skill in skills:

            matched_preferred.append(
                skill
            )

    total_skill_score = (
        len(matched_required) * 8
        + len(matched_preferred) * 4
    )

    total_skill_score = min(
        total_skill_score,
        weights["skills"]
    )

    score += total_skill_score

    if total_skill_score > 0:

        reasons.append(
            "Matched skills: "
            + ", ".join(
                matched_required
                + matched_preferred
            )
        )

    semantic_similarity = semantic_result.get(
        "average_similarity",
        0
    )

    semantic_score = min(
        semantic_similarity * 30,
        weights["semantic"]
    )

    score += semantic_score

    reasons.append(
        f"Semantic score contribution: {round(semantic_score, 2)}"
    )

    if semantic_similarity > 0.3:

        semantic_explanations = []

        for item in semantic_result.get(
            "top_chunks",
            []
        ):

            semantic_explanations.append(

                f"{item['section']} "
                f"(similarity: {item['similarity']})"
            )

        if semantic_explanations:

            reasons.append(
                "Top semantic matches: "
                + "; ".join(
                    semantic_explanations
                )
            )

    research_keywords = [
        "research",
        "publication",
        "ieee",
        "journal"
    ]

    matched_research = set()

    for keyword in research_keywords:

        pattern = (
            r"\b"
            + re.escape(keyword)
            + r"\b"
        )

        if re.search(
            pattern,
            text
        ):

            matched_research.add(
                keyword
            )

    if matched_research:

        score += weights["research"]

        reasons.append(
            "Research keywords detected: "
            + ", ".join(
                matched_research
            )
        )

    achievement_keywords = [
        "winner",
        "award",
        "scholarship",
        "hackathon"
    ]

    matched_achievements = set()

    for keyword in achievement_keywords:

        pattern = (
            r"\b"
            + re.escape(keyword)
            + r"\b"
        )

        if re.search(
            pattern,
            text
        ):

            matched_achievements.add(
                keyword
            )

    if matched_achievements:

        score += weights["achievement"]

        reasons.append(
            "Achievements detected: "
            + ", ".join(
                matched_achievements
            )
        )

    return {
        "selected": True,
        "score": min(
            round(float(score), 2),
            100
        ),
        "reasons": reasons
    }