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

     chunks = []
     step = chunk_words - overlap_words
     for start in range(0,len(words),step):
         chunk = words[start:start+chunk_words]
         chunks.append(" ".join(chunk))

         if start+chunk_words>=len(words):
             break

     return chunks
