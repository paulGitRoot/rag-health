def chunk_text(text: str, chunk_words: int=180, overlap_words: int=27)->list[str]:
    if chunk_words<=0:
        raise ValueError("chunk_words must be greater than 0")
    if overlap_words<0:
        raise ValueError("overlap_words can not be negative")
    if overlap_words>=chunk_words:
        raise ValueError("overlap_words must be smaller than chunk_words")

    words = text.split()
    if not words:
        return []

    if len(words)<=chunk_words:
        return [" ".join(words)]

    step = chunk_words - overlap_words

    starts = list(range(0,len(words)-chunk_words+1,step))
    if starts[-1]+chunk_words<len(words):
        starts.append(len(words)-chunk_words)

    chunks = []
    for start in starts:
        chunk = words[start:start+chunk_words]
        chunks.append(" ".join(chunk))

    return chunks
