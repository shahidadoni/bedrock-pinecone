from src.utils.pinecone_utils import PineconeManager
from src.utils.bedrock_utils import BedrockManager
from src.utils.patient_manager import PatientManager
import json
import os

class MedicalChatbot:
    def __init__(self):
        self.pinecone_manager = PineconeManager()
        self.bedrock_manager = BedrockManager()
        self.patient_manager = PatientManager()
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Initialize the healthcare knowledge base in Pinecone."""
        print("Initializing healthcare knowledge base...")
        
        # Load healthcare knowledge base
        kb_path = os.path.join(os.path.dirname(__file__), 'data', 'healthcare_kb.json')
        with open(kb_path, 'r') as f:
            healthcare_kb = json.load(f)
        
        # Convert healthcare knowledge into vectors
        vectors = []
        
        # Store hospital and department information
        for hospital in healthcare_kb['hospitals']:
            for department in hospital['departments']:
                # Create text representation of department information
                dept_text = f"Hospital: {hospital['name']}\n"
                dept_text += f"Department: {department['name']}\n"
                dept_text += "Doctors:\n"
                for doctor in department['doctors']:
                    dept_text += f"- {doctor['name']} ({doctor['specialization']})\n"
                    dept_text += f"  Experience: {doctor['experience']}\n"
                    dept_text += f"  Expertise: {', '.join(doctor['expertise'])}\n"
                
                # Generate embedding
                embedding = self.bedrock_manager.generate_embedding(dept_text)
                
                # Create vector with metadata
                vector = {
                    'id': f"dept_{hospital['name'].lower().replace(' ', '_')}_{department['name'].lower().replace(' ', '_')}",
                    'values': embedding,
                    'metadata': {
                        'type': 'department',
                        'hospital': hospital['name'],
                        'department': department['name'],
                        'content': dept_text
                    }
                }
                vectors.append(vector)
        
        # Store disease information
        for disease in healthcare_kb['diseases']:
            # Create text representation of disease information
            disease_text = f"Disease: {disease['name']}\n"
            disease_text += f"Symptoms: {', '.join(disease['symptoms'])}\n"
            disease_text += f"Treatments: {', '.join([t['type'] for t in disease['treatments']])}\n"
            disease_text += f"Diet Recommendations: {', '.join(disease['diet_recommendations'])}"
            
            # Generate embedding
            embedding = self.bedrock_manager.generate_embedding(disease_text)
            
            # Create vector with metadata
            vector = {
                'id': f"disease_{disease['name'].lower().replace(' ', '_')}",
                'values': embedding,
                'metadata': {
                    'type': 'disease',
                    'name': disease['name'],
                    'content': disease_text
                }
            }
            vectors.append(vector)
        
        # Store general recommendations
        for category, items in healthcare_kb['general_recommendations'].items():
            rec_text = f"Category: {category.replace('_', ' ').title()}\n"
            rec_text += f"Recommendations: {', '.join(items)}"
            
            # Generate embedding
            embedding = self.bedrock_manager.generate_embedding(rec_text)
            
            # Create vector with metadata
            vector = {
                'id': f"rec_{category.lower().replace(' ', '_')}",
                'values': embedding,
                'metadata': {
                    'type': 'recommendation',
                    'category': category,
                    'content': rec_text
                }
            }
            vectors.append(vector)
        
        # Upsert vectors to Pinecone
        self.pinecone_manager.upsert_vectors(vectors)
        print("Healthcare knowledge base initialization complete!")

    def process_query(self, query: str) -> str:
        """Process a user query and return a response."""
        # Get current patient context
        patient_context = self.patient_manager.format_patient_context()
        
        # Generate embedding for the query
        query_embedding = self.bedrock_manager.generate_embedding(query)
        
        # Find relevant healthcare information from Pinecone
        similar_kb_entries = self.pinecone_manager.query_vectors(query_embedding)
        
        # Format healthcare knowledge based on type
        kb_context_parts = []
        for entry in similar_kb_entries:
            metadata = entry.metadata
            if metadata['type'] == 'department':
                kb_context_parts.append(f"Available Healthcare Providers:\n{metadata['content']}")
            elif metadata['type'] == 'disease':
                kb_context_parts.append(f"Healthcare Information:\n{metadata['content']}")
            elif metadata['type'] == 'recommendation':
                kb_context_parts.append(f"General Recommendations:\n{metadata['content']}")
        
        # Combine all context
        kb_context = "\n\n".join(kb_context_parts)
        full_context = f"{patient_context}\n\n{kb_context}"
        
        # Generate response using Bedrock
        response = self.bedrock_manager.generate_response(full_context, query)
        return response

def main():
    print("Initializing Medical Report Chatbot...")
    chatbot = MedicalChatbot()
    
    # Assign random patient
    patient = chatbot.patient_manager.assign_random_patient()
    print(f"\nWelcome! You are viewing the medical report for {patient['name']}.")
    print(f"Condition: {patient['condition']}")
    print(f"Department: {patient['department']}")
    print(f"Doctor: {patient['doctor']}")
    print("\nYou can ask questions about the medical report or related healthcare information.")
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