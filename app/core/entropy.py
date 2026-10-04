from collections import Counter
from math import log2

def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c/n) * log2(c/n) for c in counts.values())

def file_entropy(path, sample_bytes=65536) -> float:
    with open(path, "rb") as f:
        return shannon_entropy(f.read(sample_bytes))
