import re
import spacy

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

import numpy as np


nlp = spacy.load(
    "en_core_web_sm"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

INVALID_NAME_WORDS = {

    "linkedin",
    "github",
    "leetcode",
    "jupyter",
    "notebook",
    "machine",
    "learning",
    "skills",
    "education",
    "profile",
    "summary",
    "professional",
    "experience",
    "project",
    "projects",
    "internship",
    "certifications",
    "technical",
    "core",
    "ai",
    "ml",
    "python",
    "java",

    "email",
    "mobile",
    "phone",
    "contact",
    "gmail",
    "yahoo",
    "hotmail",

    "present",
    "btech",
    "b.tech",
    "cse",
    "ece",
    "engineer",
    "developer",
    "software",
    "student",

    "sector",
    "india",
    "delhi",
    "noida",
    "uttar",
    "pradesh",
    "west",
    "east",
    "kolkata",
    "punjab",
    "hindi",

    "about",
    "me",
    "resume",
    "objective",
    "address",

    "html",
    "css",
    "javascript",
    "react",
    "node",
    "mongodb",
    "sql",
    "mysql",

    "achievement",
    "achievements",

    "communication",
    "leadership",
    "problem",
    "solving",

    "computer",
    "science",
    "technology"
}


def clean_name(text):

    text = re.sub(
        r"[^A-Za-z\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def is_valid_name(candidate):

    if not candidate:
        return False

    candidate = candidate.strip()

    words = candidate.split()

    if len(words) < 2:
        return False

    if len(words) > 4:
        return False

    lower_words = [
        w.lower()
        for w in words
    ]

    for word in lower_words:

        if word in INVALID_NAME_WORDS:
            return False

    if re.search(r"\d", candidate):
        return False

    if "@" in candidate:
        return False

    if "www" in candidate.lower():
        return False

    if "http" in candidate.lower():
        return False

    if len(candidate) > 35:
        return False

    for word in words:

        if len(word) == 1:
            return False

        if not word[0].isupper():
            return False

    return True


def score_name_candidate(candidate, line_index):

    score = 0

    words = candidate.split()

    if len(words) == 2:
        score += 30

    if len(words) == 3:
        score += 20

    if candidate.isupper():
        score += 40

    if line_index <= 3:
        score += 50

    if all(word[0].isupper() for word in words):
        score += 20

    doc = nlp(candidate)

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            score += 60

    return score


def extract_candidate_name(text):

    lines = text.split("\n")

    candidates = []

    top_lines = lines[:25]

    for i, line in enumerate(top_lines):

        cleaned = clean_name(line)

        if not cleaned:
            continue

        if not is_valid_name(cleaned):
            continue

        if cleaned.isupper():
            score_bonus = 40

        elif len(cleaned.split()) <= 3:
            score_bonus = 20

        else:
            score_bonus = 0

        score = (
            score_name_candidate(
                cleaned,
                i
            )
            + score_bonus
        )

        candidates.append({
            "name": cleaned,
            "score": score
        })

    if candidates:

        best_candidate = max(
            candidates,
            key=lambda x: x["score"]
        )

        return best_candidate["name"].title()

    return "Unknown Candidate"


def extract_resume_sections(text):

    text = text.replace("\r", "")

    patterns = {

        "projects":
            r"(projects|project experience)",

        "skills":
            r"(skills|technical skills)",

        "education":
            r"(education|academic)",

        "experience":
            r"(experience|work experience)",

        "achievements":
            r"(achievements|certifications)"
    }

    sections = {}

    lines = text.split("\n")

    current_section = "other"

    sections[current_section] = []

    for line in lines:

        clean_line = line.strip().lower()

        matched = False

        for section_name, pattern in patterns.items():

            if re.search(pattern, clean_line):

                current_section = section_name

                if current_section not in sections:
                    sections[current_section] = []

                matched = True
                break

        if not matched:
            sections[current_section].append(line)

    for key in sections:

        sections[key] = "\n".join(
            sections[key]
        )

    return sections


def compute_semantic_similarity(
    text1,
    text2
):

    embedding1 = embedding_model.encode(
        [text1]
    )

    embedding2 = embedding_model.encode(
        [text2]
    )

    similarity = cosine_similarity(
        embedding1,
        embedding2
    )[0][0]

    return float(similarity)


def semantic_project_match(
    sections,
    semantic_profile
):

    chunks = []

    for section_name in [
        "projects",
        "skills",
        "achievements",
        "experience"
    ]:

        section_text = sections.get(
            section_name,
            ""
        )

        lines = section_text.split("\n")

        for line in lines:

            clean_line = line.strip()

            if len(clean_line) > 20:

                chunks.append({
                    "section":
                        section_name,

                    "text":
                        clean_line
                })

    ranked_chunks = []

    similarity_scores = []

    for chunk in chunks:

        similarity = (
            compute_semantic_similarity(
                chunk["text"],
                semantic_profile
            )
        )

        ranked_chunks.append({

            "section":
                chunk["section"],

            "text":
                chunk["text"],

            "similarity":
                round(
                    similarity,
                    2
                )
        })

        similarity_scores.append(
            similarity
        )

    ranked_chunks = sorted(
        ranked_chunks,
        key=lambda x:
            x["similarity"],
        reverse=True
    )

    top_chunks = ranked_chunks[:5]

    if similarity_scores:

        average_similarity = max(
            similarity_scores
        )

    else:
        average_similarity = 0

    return {

        "average_similarity":
            round(
                average_similarity,
                2
            ),

        "top_chunks":
            top_chunks
    }