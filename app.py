import streamlit as st
from streamlit_chat import message
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory

# Initialize session state variables
if 'conversations' not in st.session_state:
    st.session_state['conversations'] = {}
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

# Page configuration
st.set_page_config(page_title="Chat GPT Clone", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Enterprise AI Chat Assistant</h1>", unsafe_allow_html=True)

# Sidebar for API key input
st.sidebar.title("Settings")
st.session_state['API_Key'] = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

# Function to handle conversation logic
def get_response(user_input, api_key, chat_key):
    if chat_key not in st.session_state['conversations']:
        st.session_state['conversations'][chat_key] = {'messages': []}

    conversation = st.session_state['conversations'][chat_key]
    llm = OpenAI(temperature=0, openai_api_key=api_key, model_name='text-davinci-003')

    if 'chain' not in conversation:
        conversation['chain'] = ConversationChain(llm=llm,verbose=True, memory=ConversationSummaryMemory(llm=llm))

    response = conversation['chain'].predict(input=user_input)
    conversation['messages'].append((user_input, "user"))
    conversation['messages'].append((response, "AI"))
    return response

# Chat interface with tabs
num_tabs = st.sidebar.number_input("Number of Tabs", min_value=1, max_value=10, value=1)
tab_keys = [f'Chat {i+1}' for i in range(num_tabs)]
tabs = st.tabs(tab_keys)
for i, tab in enumerate(tabs):
    with tab:
        chat_key = f'chat_{i}'
        user_input = st.text_area(f"Your question:", key=f'input_{i}', height=100)
        submit_button = st.button(f'Send', key=f'submit_{i}')
        if submit_button:
            response = get_response(user_input, st.session_state['API_Key'], chat_key)
            for message_text, sender in st.session_state['conversations'][chat_key]['messages']:
                if sender == 'user':
                    message(message_text, is_user=True)
                else:
                    message(message_text)

# Optional: Summarize the conversation
if st.sidebar.button("Summarize All Conversations"):
    for i, tab_key in enumerate(tab_keys):
        chat_key = f'chat_{i}'
        conversation = st.session_state['conversations'].get(chat_key, {})
        messages = conversation.get('messages', [])
        if messages:
            st.sidebar.write(f"Summary of {tab_key}:")
            # Replaced the summarize method with a custom summary logic
            summary = ' '.join([msg for msg, sender in messages if sender == 'AI'])
            st.sidebar.write(summary)
# Additional Resources
st.sidebar.markdown("### Additional Resources")
st.sidebar.markdown("[Checkout Avinash's Hugging Face Profile](https://huggingface.co/AvinashPolineni)")
st.sidebar.markdown("[Checkout Avinash's GitHub Profile](https://github.com/polineniavinash)")
st.sidebar.markdown("[Contact Me on LinkedIn](https://linkedin.com/in/avinash-polineni/)")

# Footer
st.markdown("---")
st.caption("© 2023 Avinash Polineni. All Rights Reserved.")