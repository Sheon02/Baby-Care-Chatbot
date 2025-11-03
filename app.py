import streamlit as st
import time
from chatbot import BabyCareChatbot

# Set page config
st.set_page_config(
    page_title="BabyCare Chatbot",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize chatbot
@st.cache_resource
def load_chatbot():
    return BabyCareChatbot('baby_qa_data.json')

chatbot = load_chatbot()

# Custom CSS with enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #fafafa;
    }
    
    /* Header styling */
    .header {
        background-color: #e6f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #4da6ff;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: #e6f7ff;
        border: 1px solid #b3e0ff;
    }
    
    .bot-message {
        background-color: #fff5e6;
        border: 1px solid #ffd9b3;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f0f8ff;
        background-image: linear-gradient(to bottom, #e6f7ff, #f0f8ff);
    }
    
    /* Button styling */
    .stButton button {
        background-color: #4da6ff;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #0080ff;
        color: white;
    }
    
    /* Chat input styling */
    .stChatInput {
        bottom: 3rem;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        color: #666;
        font-size: 0.8rem;
    }
    
    /* Example questions styling */
    .example-question {
        background-color: #fff5e6;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffaa00;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .example-question:hover {
        background-color: #ffe6cc;
        transform: translateX(5px);
    }
    
    /* Clear button styling */
    .clear-btn {
        background-color: #ff6666 !important;
    }
    
    .clear-btn:hover {
        background-color: #ff3333 !important;
    }
    
    /* Hidden button styling */
    .hidden-button {
        display: none;
    }
    
    /* Custom button for example questions */
    .example-btn {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        text-align: left !important;
        background-color: #fff5e6 !important;
        color: #333 !important;
        border: 1px solid #ffd9b3 !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem !important;
        margin: 0.25rem 0 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        white-space: normal !important;
        height: auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .example-btn:hover {
        background-color: #ffe6cc !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* Ensure all example buttons have the same width */
    .stSidebar .stButton button {
        width: 100% !important;
    }
    
    /* Container for example buttons to ensure consistent width */
    .example-btn-container {
        width: 100% !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("👶 BabyCare Chatbot")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Ask me about:
    - 🤱 Feeding & nutrition
    - 💤 Sleep patterns
    - 🎯 Developmental milestones
    - 🩺 Common health concerns
    - 🧼 Hygiene & care
    - 😢 Crying & soothing
    """)
    
    st.divider()
    st.markdown("### Example Questions")
    
    example_questions = [
        "How to stop a baby from crying?",
        "How to burp a baby?",
        "How to change a diaper?",
        "How to know if baby is hungry?",
        "How much should my newborn sleep?",
        "When do babies start to smile?",
        "How to soothe a teething baby?"
    ]
    
    for question in example_questions:
        # Create a custom-styled button for each example question
        if st.button(question, key=f"btn_{question}", help="Click to ask this question"):
            # Set the question in session state
            st.session_state.user_input = question
            # Add a small delay to ensure the session state is updated before rerun
            time.sleep(0.1)
            st.rerun()

# Main chat interface
st.title("👶 BabyCare Chat-Bot")
st.markdown("Ask me anything about baby care! I'm here to help with feeding, sleep, development, and more.")
st.markdown('</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "👶"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Check if there's a user input from the example questions
if "user_input" in st.session_state and st.session_state.user_input:
    prompt = st.session_state.user_input
    # Clear the user input from session state to prevent reprocessing
    del st.session_state.user_input
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Generate and display bot response
    with st.chat_message("assistant", avatar="👶"):
        with st.spinner("Thinking..."):
            response = chatbot.generate_response(prompt)
        st.markdown(response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to clear any state issues
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask a question about baby care..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Generate and display bot response
    with st.chat_message("assistant", avatar="👶"):
        with st.spinner("Thinking..."):
            response = chatbot.generate_response(prompt)
        st.markdown(response)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Clear Conversation", type="secondary", use_container_width=True, 
                key="clear_btn", help="Click to clear the conversation"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class='footer'>
    <small>Disclaimer: This chatbot provides general information only. 
    It is not a substitute for professional medical advice. 
    Always consult with a pediatrician for specific health concerns.</small>
</div>
""", unsafe_allow_html=True)

# Apply custom CSS to the example buttons
st.markdown("""
<script>
    // Apply custom styling to example question buttons
    document.addEventListener('DOMContentLoaded', function() {
        // Find all buttons with keys starting with "btn_"
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            if (button.getAttribute('data-testid') && button.getAttribute('data-testid').includes('btn_')) {
                button.classList.add('example-btn');
                // Wrap each button in a container for consistent width
                const container = document.createElement('div');
                container.className = 'example-btn-container';
                button.parentNode.insertBefore(container, button);
                container.appendChild(button);
            }
        });
    });
</script>
""", unsafe_allow_html=True)