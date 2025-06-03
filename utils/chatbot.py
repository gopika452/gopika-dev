import config
import os
from llama_index.core import (
                              VectorStoreIndex, 
                              SimpleDirectoryReader, 
                              StorageContext, 
                              load_index_from_storage, 
                              Settings
                              )
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


def chat_bot(query):

    user_query = query

    system_prompt = """
    You are a Q&A assistant. Your role is to answer user questions using exclusively the content provided in the given documents. Do not incorporate any external knowledge or information from your training data.
    Always handle normal day to day conversations Gracefully and stay on topic.
    Guidelines:
    1. **Strict Contextual Basis:** Base all responses solely on the information contained within the provided documents.
    2. **Exclusivity:** Do not include any details, insights, or external context beyond what is explicitly given.
    3. **Detailed and Structured Answers:** When necessary, use bullet points, numbered lists, or other structured formats to provide clear and detailed explanations.
    4. **Accuracy:** Ensure every part of your response directly reflects the content and context of the documents provided.
    """

    prompt_template = f"""
    <|begin_of_text|>|
    <|start_header_id|>system<|end_header_id|>

    Cutting Knowledge Date: December 2023
    Today date: 17 Feb 2025

    {system_prompt}<|eot_id|>
    <|start_header_id|>user<|end_header_id|>

    {user_query}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """

    # print(prompt_template)
    model_name = config.LOCAL_EMBED_MODEL 
    base_url = config.BASE_URL
    print(model_name, base_url)

    PERSIST_DIR = config.PERSISTAND_PATH
    Settings.embed_model = OllamaEmbedding(model_name=config.LOCAL_EMBED_MODEL, base_url=config.BASE_URL)
    Settings.llm = Ollama(model=config.LOCAL_MODEL, base_url=config.BASE_URL)

    # Check if persistence files actually exist, not just the directory
    def is_index_persisted(persist_dir):
        if not os.path.exists(persist_dir):
            return False
        
        # Check for the essential persistence files
        required_files = ['docstore.json', 'index_store.json', 'vector_store.json']
        for file in required_files:
            if not os.path.exists(os.path.join(persist_dir, file)):
                return False
        return True

    if not is_index_persisted(PERSIST_DIR):
        print("Creating new index...")
        # Ensure the persist directory exists
        os.makedirs(PERSIST_DIR, exist_ok=True)
        
        documents = SimpleDirectoryReader(config.FILE_PATH).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        print(f"Index persisted to {PERSIST_DIR}")
    else:
        print("Loading existing index...")
        try:
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
            print("Index loaded successfully")
        except Exception as e:
            print(f"Error loading index: {e}")
            print("Creating new index...")
            # If loading fails, create a new index
            documents = SimpleDirectoryReader(config.FILE_PATH).load_data()
            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            index.storage_context.persist(persist_dir=PERSIST_DIR)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=7)
    post_processor = SimilarityPostprocessor(similarity_cutoff=0.40)
    query_engine = RetrieverQueryEngine(retriever=retriever, node_postprocessors=[post_processor])
    response = query_engine.query(prompt_template)
    return response