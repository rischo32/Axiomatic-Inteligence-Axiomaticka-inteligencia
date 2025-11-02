# anchor.py
"""
Simple Merkle root helper for batch anchoring.
"""
import hashlib
import json
from pathlib import Path

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_hash_of_file(path: Path) -> str:
    data = path.read_bytes()
    return sha256_hex(data)

def merkle_root_from_hashes(hashes):
    if not hashes:
        return None
    cur = list(hashes)
    while len(cur) > 1:
        new = []
        for i in range(0, len(cur), 2):
            h1 = cur[i]
            h2 = cur[i+1] if i+1 < len(cur) else cur[i]
            new.append(sha256_hex((h1 + h2).encode()))
        cur = new
    return cur[0]

def merkle_root_from_dir(logdir):
    p = Path(logdir)
    files = sorted([f for f in p.iterdir() if f.is_file()])
    hashes = [canonical_hash_of_file(f) for f in files]
    return merkle_root_from_hashes(hashes)

if __name__ == "__main__":
    print("Merkle root helper ready")
