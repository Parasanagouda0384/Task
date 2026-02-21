import nltk
import random
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Resource Initialization ---
# Downloading necessary NLTK data packages
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# --- 2. Knowledge Base & Intents ---
# A dictionary defining user intents and potential responses
intents = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "hola", "greetings"],
        "responses": ["Hello! How can I help you today?", "Hi there! What's on your mind?", "Hey! I'm your AI assistant."]
    },
    "capabilities": {
        "patterns": ["what can you do", "help", "tasks", "features"],
        "responses": ["I can chat with you, answer basic questions, and demonstrate NLP techniques like intent recognition!"]
    },
    "identity": {
        "patterns": ["who are you", "your name", "are you a bot"],
        "responses": ["I am a Python-based AI chatbot built using NLTK and Scikit-learn.", "I'm your friendly neighborhood NLP bot!"]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "exit", "quit", "see you"],
        "responses": ["Goodbye! Have a great day.", "See you later!", "Talk to you soon!"]
    }
}

# --- 3. NLP Preprocessing ---
lemmer = nltk.stem.WordNetLemmatizer()

def lemmatize_tokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def preprocess(text):
    # Tokenize, lowercase, remove punctuation, and lemmatize
    tokens = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    return lemmatize_tokens(tokens)

# --- 4. Intent Recognition Logic ---
def get_response(user_input):
    all_patterns = []
    intent_map = []
    
    # Flatten the patterns for vectorization
    for intent, data in intents.items():
        for pattern in data['patterns']:
            all_patterns.append(pattern)
            intent_map.append(intent)

    # Add the user input to the list for comparison
    all_patterns.append(user_input)

    # TF-IDF Vectorization
    tfidf_vec = TfidfVectorizer(tokenizer=preprocess, stop_words='english')
    tfidf_matrix = tfidf_vec.fit_transform(all_patterns)

    # Calculate Cosine Similarity between user input (last item) and all patterns
    vals = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    idx = vals.argsort()[0][-1]
    flat = vals.flatten()
    flat.sort()
    best_match_score = flat[-1]

    # Threshold for intent recognition
    if best_match_score < 0.2:
        return "I'm sorry, I didn't quite understand that. Could you rephrase?", False
    
    matched_intent = intent_map[idx]
    is_goodbye = matched_intent == "goodbye"
    
    return random.choice(intents[matched_intent]['responses']), is_goodbye

# --- 5. Conversation Loop ---
def start_chatbot():
    print("--- NLP AI Chatbot Initialized ---")
    print("Type 'bye' to exit the conversation.")
    
    while True:
        user_text = input("\nYou: ").strip()
        
        if not user_text:
            continue
            
        response, should_exit = get_response(user_text)
        print(f"Bot: {response}")
        
        if should_exit:
            break

if __name__ == "__main__":
    start_chatbot()
