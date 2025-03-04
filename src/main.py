from src.utils.pinecone_utils import PineconeManager
from src.utils.bedrock_utils import BedrockManager
from src.utils.data_utils import DataManager
import uuid

class MedicalChatbot:
    def __init__(self):
        self.pinecone_manager = PineconeManager()
        self.bedrock_manager = BedrockManager()
        self.data_manager = DataManager()
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize the vector store with medical report embeddings."""
        print("Initializing vector store with medical reports...")
        reports = self.data_manager.load_data()
        
        vectors = []
        for report in reports:
            # Generate embedding for the report content
            embedding = self.bedrock_manager.generate_embedding(report['content'])
            
            # Create vector metadata
            vector = {
                'id': str(uuid.uuid4()),
                'values': embedding,
                'metadata': {
                    'report_id': report['id'],
                    'patient_name': report['patient_name'],
                    'report_type': report['report_type'],
                    'date': report['date'],
                    'doctor': report['doctor'],
                    'department': report['department'],
                    'content': report['content']
                }
            }
            vectors.append(vector)
        
        # Upsert vectors to Pinecone
        self.pinecone_manager.upsert_vectors(vectors)
        print("Vector store initialization complete!")

    def process_query(self, query: str) -> str:
        """Process a user query and return a response."""
        # Generate embedding for the query
        query_embedding = self.bedrock_manager.generate_embedding(query)
        
        # Find similar reports using semantic search
        similar_reports = self.pinecone_manager.query_vectors(query_embedding)
        
        # Combine the content of similar reports for context
        context = "\n\n".join([report.metadata['content'] for report in similar_reports])
        
        # Generate response using Bedrock
        response = self.bedrock_manager.generate_response(context, query)
        return response

def main():
    print("Initializing Medical Report Chatbot...")
    chatbot = MedicalChatbot()
    
    print("\nWelcome to the Medical Report Chatbot!")
    print("You can ask questions about the medical reports in the system.")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("Your question: ").strip()
        if query.lower() == 'exit':
            break
            
        try:
            response = chatbot.process_query(query)
            print("\nResponse:", response, "\n")
        except Exception as e:
            print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    main() 