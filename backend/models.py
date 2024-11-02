from sentence_transformers import SentenceTransformer

# Load the model once at startup
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)
