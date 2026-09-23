import os
from chromadb import Documents, EmbeddingFunction, Embeddings
from openai import AzureOpenAI

class AzureOpenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
        api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        
        if not endpoint or not api_key:
            print("[Warning] Azure OpenAI credentials not fully configured. Embeddings may fail.")
            self.client = None
        else:
            self.client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
            )

    def __call__(self, input: Documents) -> Embeddings:
        if not self.client:
            # Return dummy embeddings to prevent hard crashes if not configured during build
            return [[0.0] * 1536 for _ in input]
            
        response = self.client.embeddings.create(
            input=input, 
            model=self.deployment
        )
        return [data.embedding for data in response.data]

def get_embedding_function() -> EmbeddingFunction:
    """Returns the Azure OpenAI embedding function for ChromaDB."""
    return AzureOpenAIEmbeddingFunction()
