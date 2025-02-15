import numpy as np
import os

from AIProxy import get_embeddings

def execute_task(filename: str, targetfile: str) -> str:
    # Read comments from file    
    with open(filename, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]
        
    # Generate embeddings
    emd_data = get_embeddings(comments)
    embeddings = np.array([emb["embedding"] for emb in emd_data])
    similarity = np.dot(embeddings, embeddings.T)
    # Create mask to ignore diagonal (self-similarity)
    np.fill_diagonal(similarity, -np.inf)
    # Get indices of maximum similarity
    i, j = np.unravel_index(similarity.argmax(), similarity.shape)
    expected = "\n".join(sorted([comments[i], comments[j]]))
    
    # Write the most similar comments to output file
    if expected:
        with open(targetfile, "w", encoding="utf-8") as f:
            f.write(expected)

    print("Most similar comments written to:", targetfile)
    return targetfile

# # Function to get embeddings
# def get_embeddings(texts):
#     response = client.embeddings.create(
#         input=texts,
#         model="text-embedding-3-small"
#     )

#     #print(response.data[0].embedding)
#     return response.data
