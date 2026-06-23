from pathlib import Path
import re

from src.config import KNOWLEDGE_BASE_DIR


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_knowledge_documents():
    documents = []

    if not KNOWLEDGE_BASE_DIR.exists():
        return documents

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents


def split_into_chunks(text: str, chunk_size: int = 700):
    text = clean_text(text)
    words = text.split()

    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)

        if len(" ".join(current_chunk)) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def keyword_score(query: str, text: str) -> int:
    query_words = set(clean_text(query.lower()).split())
    text_lower = clean_text(text.lower())

    score = 0
    for word in query_words:
        if len(word) > 2 and word in text_lower:
            score += 1

    return score


def search_knowledge_base(query: str, top_k: int = 3):
    documents = load_knowledge_documents()
    results = []

    for document in documents:
        chunks = split_into_chunks(document["content"])

        for chunk in chunks:
            score = keyword_score(query, chunk)

            if score > 0:
                results.append(
                    {
                        "source": document["source"],
                        "score": score,
                        "content": chunk,
                    }
                )

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]


def build_rag_context(query: str) -> str:
    results = search_knowledge_base(query)

    if not results:
        return "No relevant knowledge base information was found."

    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\nContent: {result['content']}"
        )

    return "\n\n---\n\n".join(context_parts)


if __name__ == "__main__":
    test_query = "Can the patient cancel appointment?"
    context = build_rag_context(test_query)
    print(context)