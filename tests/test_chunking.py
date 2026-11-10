from app.core.chunking import chunk_text

def test_basic_chunking():
    text = " ".join(f"word{i}" for i in range(25))

    chunks = chunk_text(
        text,
        chunk_words=10,
        overlap_words=3
    )

    assert len(chunks) == 4
    assert len(chunks[0].split()) == 10
    assert len(chunks[1].split()) == 10
    assert len(chunks[2].split()) == 10
    assert len(chunks[3].split()) == 4


def test_empty_text():
    assert chunk_text("") == []


def test_invalid_overlap():
    try:
        chunk_text("hello world", 10, 10)
        assert False
    except ValueError:
        pass

