import faiss
import numpy as np
import pytest


@pytest.fixture
def test_data():
    """
    Fixture to create test data.
    Returns random database vectors and query vectors along with their dimensions.
    """
    d = 128  # Dimensionality of the vectors
    nb = 100  # Number of database vectors
    nq = 10  # Number of query vectors
    np.random.seed(42)
    db_vectors = np.random.random((nb, d)).astype("float32")
    query_vectors = np.random.random((nq, d)).astype("float32")
    return db_vectors, query_vectors, d


def test_gpu_availability():
    """Check if GPU is available."""
    assert faiss.get_num_gpus() > 0, "GPU is not available"


def test_faiss_gpu_search(test_data):
    """Test if FAISS-GPU search works correctly."""
    db_vectors, query_vectors, d = test_data
    k = 5  # Number of nearest neighbors

    # Create a CPU index
    index_cpu = faiss.IndexFlatL2(d)

    # Transfer the index to GPU
    res = faiss.StandardGpuResources()  # Create GPU resources
    index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu)

    # Add database vectors to the index
    index_gpu.add(db_vectors)
    assert (
        index_gpu.ntotal == db_vectors.shape[0]
    ), "Number of vectors in the index is incorrect"

    # Perform a search
    distances, indices = index_gpu.search(query_vectors, k)

    assert distances.shape == (
        query_vectors.shape[0],
        k,
    ), "Shape of the distances array is incorrect"
    assert indices.shape == (
        query_vectors.shape[0],
        k,
    ), "Shape of the indices array is incorrect"
    assert indices.shape == (
        query_vectors.shape[0],
        k,
    ), "Shape of the indices array is incorrect"


def test_faiss_gpu_vs_cpu(test_data):
    """Test if GPU and CPU search results are consistent."""
    db_vectors, query_vectors, d = test_data
    k = 5  # Number of nearest neighbors

    # Create a CPU index and add database vectors
    index_cpu = faiss.IndexFlatL2(d)
    index_cpu.add(db_vectors)

    # Transfer the index to GPU
    res = faiss.StandardGpuResources()
    index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu)

    # Perform searches on both CPU and GPU
    distances_cpu, indices_cpu = index_cpu.search(query_vectors, k)
    distances_gpu, indices_gpu = index_gpu.search(query_vectors, k)

    np.testing.assert_allclose(
        distances_cpu,
        distances_gpu,
        atol=1e-5,
        err_msg="Distances differ between CPU and GPU",
    )
    np.testing.assert_array_equal(
        indices_cpu, indices_gpu, err_msg="Indices differ between CPU and GPU"
    )
    np.testing.assert_array_equal(
        indices_cpu, indices_gpu, err_msg="Indices differ between CPU and GPU"
    )
