from sentence_transformers import SentenceTransformer
import numpy as np
import os
from vector_db import build_faiss_index, search_index
from data_preprocessing import get_chunks

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks using a pre-trained model.
    Args:
        chunks (list): List of text chunks.
    Returns:
        np.ndarray: Array of embeddings.
    """
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_tensor=True)
    return np.array(embeddings)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", 'data', 'TSLA_10k.html')
    chunks = get_chunks(file_path, chunk_size=5000)
    print("Total chunks:", len(chunks))
    
    embeddings = generate_embeddings(chunks)
    print("Embeddings shape:", embeddings.shape)

    np.savez_compressed("embeddings.npz", embeddings=embeddings)
    
    index = build_faiss_index(embeddings)
    print("Total vectors in index:", index.ntotal)

    query = "What are Tesla's automotive sales details?"
    query_embedding = generate_embeddings([query])
    D, I = search_index(query_embedding, index, k=1)

    results = [chunks[i] for i in I[0]]
    print("Search results:")
    for i in results:
        print(i)
