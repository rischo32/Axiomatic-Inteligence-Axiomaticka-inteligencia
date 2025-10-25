from hashlib import sha256
import json

def merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]
    new_hashes = []
    for i in range(0, len(hashes), 2):
        h1 = hashes[i]
        h2 = hashes[i+1] if i+1 < len(hashes) else h1
        new_hashes.append(sha256(h1 + h2).hexdigest())
    return merkle_root(new_hashes)

# Príklad: Hashes rozhodnutí/logov
decision_hashes = [sha256(json.dumps({"id":1, "score":0.85}).encode()).hexdigest(),
                   sha256(json.dumps({"id":2, "score":0.68}).encode()).hexdigest()]
root = merkle_root(decision_hashes)
print(f"Merkle Root: {root}") # Anchorovať toto do blockchainu (napr. Ethereum transaction)
