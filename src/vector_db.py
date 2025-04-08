import faiss
import numpy as np

def build_faiss_index(embeddings_array):
    """
    Build a FAISS index from the given embeddings array.
    Args:
        embeddings_array (np.ndarray): Array of embeddings.
    Returns:
        faiss.IndexFlatL2: FAISS index built from the embeddings.
    """
    d = embeddings_array.shape[1]
    index = faiss.IndexFlatL2(d)  # Using L2 distance for the index
    index.add(embeddings_array)  # Add the embeddings to the index
    return index

def search_index(query_embedding, index, k=3):
    """
    Search the FAISS index for the k nearest neighbors of the query embedding.
    Args:
        query_embedding (np.ndarray): The query embedding which shape is (1, embedding_dim).
        index (faiss.IndexFlatL2): The FAISS index.
        k (int): Number of nearest neighbors to return.
    Returns:
        list: List of indices of the nearest neighbors.
    """
    query_embedding = np.array(query_embedding).astype('float32')  # Search the index
    D, I = index.search(query_embedding, k)  # D is distances, I is indices
    return D, I
