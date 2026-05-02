from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from agentic_grant_proposal_builder.models import GrantDocument


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    text: str
    score: float


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    clean = " ".join(text.split())

    if not clean:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(clean):
        end = min(start + chunk_size, len(clean))
        chunks.append(clean[start:end])

        if end == len(clean):
            break

        start = max(0, end - overlap)

    return chunks


class LocalRetriever:
    def __init__(self, documents: list[GrantDocument]) -> None:
        self.rows: list[tuple[str, str]] = []

        for doc in documents:
            for chunk in chunk_text(doc.text):
                self.rows.append((doc.name, chunk))

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None

        if self.rows:
            self.matrix = self.vectorizer.fit_transform([row[1] for row in self.rows])

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if not self.rows or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        ranked_indices = scores.argsort()[::-1][:top_k]

        return [
            RetrievedChunk(
                source=self.rows[index][0],
                text=self.rows[index][1],
                score=float(scores[index]),
            )
            for index in ranked_indices
            if scores[index] > 0
        ]
