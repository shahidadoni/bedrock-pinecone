import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Pinecone Configuration
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX_NAME = 'medical-reports'

# Bedrock Configuration
BEDROCK_EMBEDDING_MODEL_ID = 'amazon.titan-embed-text-v2:0'  # Latest Titan embedding model
BEDROCK_CHAT_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'  # Latest Claude model

# Vector Configuration
VECTOR_DIMENSION = 1024  # Titan v2 embedding dimension

# Prompt Templates
SYSTEM_PROMPT = """You are a medical report analysis assistant. Your role is to help users understand medical reports by providing clear, accurate, and helpful explanations. 
Always maintain medical accuracy and confidentiality. If you're unsure about any information, please say so."""

USER_PROMPT_TEMPLATE = """Based on the following medical report context, please answer the question. If the context doesn't contain enough information to answer the question, please say so.

Context: {context}

Question: {question}

Please provide a clear and concise answer.""" 