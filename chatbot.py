import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

class BabyCareChatbot:
    def __init__(self, knowledge_base_path='baby_qa_data.json'):
        self.qa_pairs = self.load_knowledge_base(knowledge_base_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model for similarity
        
        # Precompute embeddings for all questions
        self.questions = [qa['question'] for qa in self.qa_pairs]
        self.question_embeddings = self.model.encode(self.questions)
    
    def load_knowledge_base(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def find_most_relevant_question(self, user_question, top_k=3):
        """Find most relevant question from knowledge base"""
        if not self.qa_pairs:
            return []
        
        # Encode user question
        user_embedding = self.model.encode([user_question])
        
        # Calculate similarities
        similarities = cosine_similarity(user_embedding, self.question_embeddings)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'question': self.questions[idx],
                'answer': self.qa_pairs[idx]['answer'],
                'score': similarities[idx]
            })
        
        return results
    
    def extract_age_info(self, question):
        """Extract age information from question"""
        age_patterns = [
            r'(\d+)\s*(week|weeks|wk)',
            r'(\d+)\s*(month|months|mo)',
            r'(\d+)\s*(year|years|yr)',
            r'newborn',
            r'infant',
            r'toddler'
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, question.lower())
            if match:
                if 'newborn' in pattern:
                    return 'newborn'
                elif 'infant' in pattern:
                    return '0-12 months'
                elif 'toddler' in pattern:
                    return '12-36 months'
                elif match.group(2) in ['week', 'weeks', 'wk']:
                    weeks = int(match.group(1))
                    return f'{weeks} weeks'
                elif match.group(2) in ['month', 'months', 'mo']:
                    months = int(match.group(1))
                    return f'{months} months'
                elif match.group(2) in ['year', 'years', 'yr']:
                    years = int(match.group(1))
                    return f'{years} years'
        return None
    
    def generate_response(self, user_question):
        """Generate response to user question"""
        # Extract age information
        age_info = self.extract_age_info(user_question)
        
        # Find relevant questions
        relevant_qa = self.find_most_relevant_question(user_question)
        
        if not relevant_qa or relevant_qa[0]['score'] < 0.3:
            return "I'm not sure about that specific question. Please consult with a pediatrician for advice tailored to your baby's needs."
        
        # Get the most relevant answer
        best_match = relevant_qa[0]
        answer = best_match['answer']
        
        # Add age context if relevant
        if age_info:
            answer = f"For a {age_info} old baby: {answer}"
        
        # Add disclaimer
        answer += "\n\n*Remember: This is general advice. Always consult with your pediatrician for concerns about your baby's health.*"
        
        return answer

# For testing
if __name__ == "__main__":
    chatbot = BabyCareChatbot()
    
    # Test questions
    test_questions = [
        "How to stop my baby from crying?",
        "What should I feed my 1 week old?",
        "How much sleep does a newborn need?",
        "When do babies start smiling?"
    ]
    
    for question in test_questions:
        print(f"Q: {question}")
        print(f"A: {chatbot.generate_response(question)}")
        print("-" * 50)