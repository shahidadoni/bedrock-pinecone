import boto3
import json
from typing import Dict, Any, List
from src.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BEDROCK_EMBEDDING_MODEL_ID,
    BEDROCK_CHAT_MODEL_ID,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE
)

class BedrockManager:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text using Amazon Titan."""
        request_body = {
            "inputText": text
        }
        
        try:
            response = self.client.invoke_model(
                modelId=BEDROCK_EMBEDDING_MODEL_ID,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body.get('embedding')
        except Exception as e:
            print(f"\nError generating embedding: {str(e)}")
            print("Please check if you have access to the embedding model.")
            return [0.1] * 1536  # Return dummy embedding as fallback

    def generate_response(self, context: str, question: str) -> str:
        """Generate response using Claude model."""
        prompt = USER_PROMPT_TEMPLATE.format(context=context, question=question)
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": f"{SYSTEM_PROMPT}\n\n{prompt}"
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        try:
            response = self.client.invoke_model(
                modelId=BEDROCK_CHAT_MODEL_ID,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body.get('content')[0].get('text')
        except Exception as e:
            print(f"\nError generating response: {str(e)}")
            print("Please check if you have access to the chat model.")
            return "I apologize, but I'm unable to generate a response at this time. Please check your AWS Bedrock access and permissions." 