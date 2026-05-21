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


def extract_candidate_name(text):

    doc = nlp(text[:1000])

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            if len(ent.text.split()) >= 2:

                return ent.text

    lines = text.split("\n")

    for line in lines[:5]:

        line = line.strip()

        if len(line.split()) >= 2:

            return line

    return "Unknown"


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