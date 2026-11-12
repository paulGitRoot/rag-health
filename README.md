# RAG Health

This repository currently provides a small text chunking utility. It splits text into word-count-limited chunks with a configurable overlap, which can be used as a building block for retrieval-augmented generation (RAG).

The repository does not yet include a health assistant, document ingestion pipeline, API, vector database, model integration, or health document corpus. No clinical or health information is provided by this code.

## Chunking

`app.core.chunking.chunk_text` accepts a string and returns a list of chunks:

```python
from app.core.chunking import chunk_text

text = "A document with enough words to split into multiple chunks..."
chunks = chunk_text(text, chunk_words=180, overlap_words=27)
```

The defaults are 180 words per chunk and 27 overlapping words between chunks. Words are separated by whitespace and normalized to single spaces in the returned chunks. Empty or whitespace-only input returns an empty list; input shorter than the chunk size returns one chunk.

For longer input, chunks are advanced by `chunk_words - overlap_words`. If the regular steps would leave a tail shorter than a full chunk, the last chunk is aligned to the end of the input so the final words are included. This can make the overlap with the preceding chunk larger than the configured overlap.

`chunk_words` must be greater than zero, and `overlap_words` must be nonnegative and smaller than `chunk_words`; invalid values raise `ValueError`.

## Development

There is no package or dependency manifest yet. The code uses the Python standard library; the tests use pytest. From the repository root, run:

```bash
python -m pytest
```

Tests are in `tests/test_chunking.py` and cover chunk sizes, overlap, input validation, and preservation of word order.

## Project status

The current implementation is limited to `app/core/chunking.py`. API endpoints, document loading, embeddings, retrieval, answer generation, citations, safety behavior, deployment configuration, and evaluation have not been implemented.
