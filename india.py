# Importing Necessary Libraries and Nodules 
import os 
import constants 
import streamlit as st 
from langchain.memory import ConversationBufferMemory 
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory 
from langchain.chains import LLMChain 
from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate 

## Setting up the 0penAT API  Key 
os.environ["OPENAI_API_KEY"] = constants.APIKEY 
#Initialize the chat message history 
msgs = StreamlitChatMessageHistory(key='langchain_messages') 

# Create an expander to view the message contents in the session state 
view_messages = st.expander("view the message contents in session state") 

# Set up the chatbot's memory 
memory = ConversationBufferMemory(memory_key="history", chat_memory=msgs)

# If there are no messages,start the conversation 
if len(msgs.messages) == 0:
	msgs.add_ai_message("How can I help you?") 

# Define the chatbot's prompt template
template = """You are an AI chatbot having a conversation with a human.
{history}
Human: {human_input}
AI: """ 
prompt = PromptTemplate(input_variables=["history","human_input"], template=template) 

# Initialize the  LLMChain with the chatbot's memory 
llm_chain = LLMChain(llm=OpenAI(), prompt=prompt, memory=memory)

# Display the chat messages 
for msg in msgs.messages:
	st.chat_message(msg.type).write(msg.content) 

# Get input from the user and display the chatbot's response 
if prompt_input := st.chat_input():
	st.chat_message("human").write(prompt_input)
	response = llm_chain.run(prompt_input)
	st.chat_message("ai").write(response) 

# viewing the conversation History Users can expand a section to view the entire conversat 
with view_messages:
	view_messages.json(st.session_state.langchain_messages)
