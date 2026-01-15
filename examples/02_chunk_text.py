"""Example: Text chunking utilities."""

from aup.chunking import chunk_by_max_chars, chunk_by_tokens


def main():
    """Demonstrate text chunking."""
    print("=== Text Chunking Example ===\n")

    # Sample text
    text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines,
    in contrast to the natural intelligence displayed by humans and animals.
    Leading AI textbooks define the field as the study of "intelligent agents":
    any device that perceives its environment and takes actions that maximize
    its chance of achieving its goals. Some popular accounts use the term
    "artificial intelligence" to describe machines that mimic "cognitive"
    functions that humans associate with the human mind, such as "learning"
    and "problem solving". However, this definition is rejected by major
    AI researchers.
    """ * 3  # Repeat to make it longer

    print(f"Original text length: {len(text)} characters\n")

    # Character-based chunking
    print("1. Chunking by max characters (100 chars, 20 char overlap):")
    chunks = chunk_by_max_chars(text, max_chars=100, overlap=20)
    print(f"   Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3], 1):  # Show first 3
        print(f"   Chunk {i} ({len(chunk)} chars): {chunk[:60]}...")
    if len(chunks) > 3:
        print(f"   ... and {len(chunks) - 3} more chunks\n")
    else:
        print()

    # Token-based chunking (approximate)
    print("2. Chunking by approximate tokens (25 tokens, 5 token overlap):")
    token_chunks = chunk_by_tokens(text, max_tokens=25, overlap_tokens=5)
    print(f"   Created {len(token_chunks)} chunks")
    for i, chunk in enumerate(token_chunks[:3], 1):
        print(f"   Chunk {i} ({len(chunk)} chars): {chunk[:60]}...")
    if len(token_chunks) > 3:
        print(f"   ... and {len(token_chunks) - 3} more chunks\n")


if __name__ == "__main__":
    main()
