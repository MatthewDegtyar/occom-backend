from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import (
        CourseSection, 
        College, 
        Department, 
        Course, 
        Textbook, 
        course_textbooks
    )
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from core.deps import get_db

# TODO: dynamically trigger regeneration of cached files once db is updated with new data.
# This may be done daily or something later on due to relatively infrequent data loading

router = APIRouter(prefix="/vector_search", tags=["vector_search"])

class SearchBody(BaseModel):
    q: str
    k: int = 5 
    s: float = 0.35

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

INDEX_PATH = "./.cache/vector_cache.faiss"
META_PATH = "./.cache/vector_cache_ids.npy"

index = None
sections_cache = []
built = False

def save_cache():
    faiss.write_index(index, INDEX_PATH)
    ids = np.array([s["section_id"] for s in sections_cache], dtype=np.int32)
    np.save(META_PATH, ids)

def load_cache(db: Session):
    global index, sections_cache, built
    if not (os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)):
        return False
    try:
        index = faiss.read_index(INDEX_PATH)
        ids = np.load(META_PATH).tolist()
        rows = (
            db.query(CourseSection)
            .filter(CourseSection.section_id.in_(ids))
            .all()
        )
        sections_cache = [
            {
                "section_id": s.section_id,
                "course_id": s.course_id,
                "section_code": s.section_code,
                "description": s.description,
            }
            for s in rows
        ]
        built = True
        return True
    except Exception:
        return False

def build_index(db: Session):
    global index, sections_cache, built
    rows = db.query(CourseSection).all()
    texts = []
    sections_cache = []
    for s in rows:
        desc = (s.description or "").strip()
        lo = (s.learning_objectives or "").strip()
        if not desc:
            continue
        combined = f"{desc} {lo}".strip()
        sections_cache.append({
            "section_id": s.section_id,
            "course_id": s.course_id,
            "section_code": s.section_code,
            "description": s.description,
        })
        texts.append(combined)
    if not texts:
        index = None
        built = True
        return
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    save_cache()
    built = True

def ensure_index(db: Session):
    global built
    if built:
        return
    if load_cache(db):
        return
    build_index(db)

def get_textbooks_for_section(db: Session, course_id: int):
    q = (
        db.query(Textbook)
        .join(course_textbooks, course_textbooks.c.isbn_13 == Textbook.isbn_13)
        .filter(course_textbooks.c.course_id == course_id)
        .all()
    )
    return [
        {
            "isbn_13": t.isbn_13,
            "title": t.title,
            "edition": t.edition,
            "publisher": t.publisher,
            "contributors": t.contributors,
            "isbn_10": t.isbn_10,
            "asin": t.asin,
            "publication_year": t.publication_year,
            "print_length": t.print_length,
            "item_weight": t.item_weight,
            "dimensions": t.dimensions,
            "url": t.url,
            "list_price": float(t.list_price) if t.list_price else None,
        }
        for t in q
    ]

@router.post("/search")
def search_vector(body: SearchBody, db: Session = Depends(get_db)):
    ensure_index(db) # trigger index loading on request not on app startup otherwise dev restarts take long
    #emb = model.encode([body.q], convert_to_numpy=True, normalize_embeddings=True)
    emb = model.encode(["q"], convert_to_numpy=True, normalize_embeddings=True) # TODO: fix this shit
    scores, idxs = index.search(emb, body.k)

    thresh = body.s
    results = []

    summary_colleges = {}
    publisher_counts = {}
    college_publisher_counts = {}

    for i, score in zip(idxs[0], scores[0]):
        if score < thresh:
            continue

        sec_dict = sections_cache[i]
        sec_id = sec_dict["section_id"]

        college, department = (
            db.query(College, Department)
            .join(Department, Department.college_id == College.college_id)
            .join(Course, Course.department_id == Department.department_id)
            .filter(Course.course_id == sec_dict["course_id"])
            .first()
            or (None, None)
        )

        college_json = None
        department_json = None
        college_id = None

        if college:
            college_id = college.college_id
            college_json = {
                "college_id": college.college_id,
                "name": college.name,
                "abbreviation": college.abbreviation,
                "address": college.addr,
                "city": college.city,
                "state": college.state,
                "zip": college.zip,
                "latitude": college.latitude,
                "longitude": college.longitude,
            }

            if college_id not in summary_colleges:
                summary_colleges[college_id] = {
                    "name": college.name,
                    "abbreviation": college.abbreviation,
                    "course_count": 0,
                    "city": college.city,
                    "state": college.state,
                    "latitude": college.latitude,
                    "longitude": college.longitude,
                }

            summary_colleges[college_id]["course_count"] += 1

        if department:
            department_json = {
                "department_id": department.department_id,
                "name": department.name,
                "code": department.code,
            }

        textbooks = get_textbooks_for_section(db, sec_dict["course_id"])

        # GLOBAL publisher count
        for t in textbooks:
            pub = t.get("publisher")
            if not pub:
                continue

            publisher_counts[pub] = publisher_counts.get(pub, 0) + 1

            if college_id:
                if college_id not in college_publisher_counts:
                    college_publisher_counts[college_id] = {}
                college_publisher_counts[college_id][pub] = (
                    college_publisher_counts[college_id].get(pub, 0) + 1
                )

        results.append({
            "section_id": sec_id,
            "section_code": sec_dict["section_code"],
            "course_id": sec_dict["course_id"],
            "score": float(score),
            "description": sec_dict["description"],
            "college": college_json,
            "department": department_json,
            "textbooks": textbooks,
        })

    summary = {
        "college_count": len(summary_colleges),
        "colleges": summary_colleges,
        "publisher_counts": publisher_counts,
        "publishers_by_college": college_publisher_counts,
    }

    return {
        "summary": summary,
        "results": results,
        "dev": {"k": body.k, "q": body.q, "s": body.s}
    }
