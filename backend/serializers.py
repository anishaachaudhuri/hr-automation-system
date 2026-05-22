def candidate_to_dict(candidate):

    return {

        "id": candidate.id,

        "name": candidate.name,

        "filename": candidate.filename,

        "skills": candidate.skills,

        "tenth": candidate.tenth,

        "twelfth": candidate.twelfth,

        "gpa": candidate.gpa,

        "selected": candidate.selected,

        "score": candidate.score,

        "semantic_score":
            candidate.semantic_score,

        "top_semantic_chunk":
            candidate.top_semantic_chunk,

        "reasons": candidate.reasons
    }