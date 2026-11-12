import pytest
from app.core.chunking import chunk_text

def test_basic_chunking():
    text = " ".join(f"word{i}" for i in range(25))
    chunks = chunk_text(text,10,3)

    assert len(chunks) == 4
    assert [len(chunk.split()) for chunk in chunks] == [10,10,10,10]

def test_overlap_content():
    text = " ".join(f"word{i}" for i in range(25))
    chunks = chunk_text(text,10,3)

    # Check the normal 3-word overlap between regular chunks.
    # The final chunk intentionally has a larger overlap.
    for i in range(len(chunks)-2):
        chunk_last_words = chunks[i].split()[-3:]
        next_first_words = chunks[i+1].split()[:3]
        assert chunk_last_words == next_first_words

def test_all_words_are_preserved():
    text = " ".join(f"word{i}" for i in range(25))
    chunks = chunk_text(text,10,3)

    original_words = set(text.split())
    chunk_words = set(" ".join(chunks).split())
    assert original_words == chunk_words

def test_empty_text():
    assert chunk_text("") == []

def test_white_space_only():
    assert chunk_text("  \n  \t  ") == []

def test_shorter_than_chunk_size():
    assert chunk_text("one two three",10,3) == ["one two three"]

def test_exact_chunk_size():
    text = " ".join(f"word{i}" for i in range(10))
    chunks = chunk_text(text,10,3)

    assert len(chunks) == 1
    assert len(chunks[0].split()) == 10

def test_chunk_size_plus_one():
    text = " ".join(f"word{i}" for i in range(11))
    chunks = chunk_text(text, 10, 3)

    assert len(chunks) == 2
    assert all(len(chunk.split()) == 10 for chunk in chunks)

def test_negative_overlap():
    with pytest.raises(ValueError):
        chunk_text("hello world", 10, -1)

def test_overlap_equal_to_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("hello world", 10, 10)

def test_final_chunk_covers_remaining_words():
    text = " ".join(f"word{i}" for i in range(25))
    chunks = chunk_text(text,10,3)

    expected_final_words = text.split()[-10:]
    assert expected_final_words == chunks[-1].split()

def test_invariants_for_many_lengths():
    for n in range(1, 120):
        words = [f"w{i}" for i in range(n)]
        chunks = chunk_text(" ".join(words), 10, 3)

        # Every chunk must contain at most 10 words.
        assert all(len(chunk.split()) <= 10 for chunk in chunks), f"n={n}"

        # If there are at least 10 words, every chunk must contain 10.
        if n >= 10:
            assert all(len(chunk.split()) == 10 for chunk in chunks), f"n={n}"

        # Reconstruct the original sequence, removing overlapping words.
        reconstructed = chunks[0].split() if chunks else []

        for chunk in chunks[1:]:
            current = chunk.split()

            overlap = max(
                k
                for k in range(1, min(len(reconstructed), len(current)) + 1)
                if reconstructed[-k:] == current[:k]
            )

            reconstructed.extend(current[overlap:])

        # Every word must be preserved in its original order.
        assert reconstructed == words, f"n={n}"

        # Every consecutive pair must overlap by at least 3 words.
        for i in range(len(chunks) - 1):
            previous = chunks[i].split()
            current = chunks[i + 1].split()

            shared = max(
                k
                for k in range(1, min(len(previous), len(current)) + 1)
                if previous[-k:] == current[:k]
            )

            assert shared >= 3, f"n={n}, pair={i}, overlap={shared}"
