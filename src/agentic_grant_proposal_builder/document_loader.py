from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader

from agentic_grant_proposal_builder.models import GrantDocument


def read_pdf_bytes(name: str, data: bytes) -> GrantDocument:
    reader = PdfReader(BytesIO(data))
    text_parts: list[str] = []

    for page in reader.pages:
        extracted = page.extract_text() or ""
        if extracted.strip():
            text_parts.append(extracted.strip())

    return GrantDocument(name=name, text="\n\n".join(text_parts), source_type="pdf")


def read_text_bytes(name: str, data: bytes) -> GrantDocument:
    return GrantDocument(
        name=name,
        text=data.decode("utf-8", errors="ignore"),
        source_type="text",
    )


def load_uploaded_file(name: str, data: bytes) -> GrantDocument:
    if name.lower().endswith(".pdf"):
        return read_pdf_bytes(name, data)
    return read_text_bytes(name, data)
