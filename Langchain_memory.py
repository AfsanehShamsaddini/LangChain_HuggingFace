import os  
import textwrap  
import sqlite3  
from dotenv import load_dotenv, find_dotenv  
from langchain_core.output_parsers import StrOutputParser  
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  
from langchain_huggingface import HuggingFaceEndpoint  
from langchain_core.chat_history import (  
    BaseChatMessageHistory,  
    InMemoryChatMessageHistory,  
)  
from langchain_core.runnables.history import RunnableWithMessageHistory  

load_dotenv(find_dotenv())  
hf_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")  
# Get your token from here: https://huggingface.co/settings/tokens and set it in the .env file

callbacks = [StreamingStdOutCallbackHandler()]  

# Define the HuggingFace model endpoint  
llm = HuggingFaceEndpoint(  
    repo_id="gpt2",  
    max_new_tokens=100,  
    top_k=10,  
    top_p=0.95,  
    typical_p=0.95,  
    temperature=0.9,  
    repetition_penalty=1.2,  
    huggingfacehub_api_token=hf_token,  
)  

def init_db():  
    conn = sqlite3.connect('chat_history.db')  
    cursor = conn.cursor()  
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS chat_history (  
            session TEXT PRIMARY KEY,  
            history TEXT  
        )  
    ''')  
    conn.commit()  
    conn.close()  

def save_history(session_id, history):  
    conn = sqlite3.connect('chat_history.db')  
    cursor = conn.cursor()  
    cursor.execute('INSERT OR REPLACE INTO chat_history (session, history) VALUES (?, ?)',  
                   (session_id, history))  
    conn.commit()  
    conn.close()  

def get_history_by_session_id(session_id):  
    conn = sqlite3.connect('chat_history.db')  
    cursor = conn.cursor()  
    cursor.execute('SELECT history FROM chat_history WHERE session = ?', (session_id,))  
    row = cursor.fetchone()  
    conn.close()  
    return row[0] if row else ""  

init_db()  

def chat(session_id):  
    history = get_history_by_session_id(session_id)  

    print("Chatbot is ready! Type 'exit' to end the conversation.")  
    
    while True:  
        user_input = input("You: ")  
        if user_input.lower() == 'exit':  
            break  

        prompt = ChatPromptTemplate.from_messages(  
            [  
                ("system", "You're an assistant who's good at giving brief answers to questions."),  
                MessagesPlaceholder(variable_name="history"),  
                ("human", "{question}"),  
            ]  
        )  

        chain = prompt | llm | StrOutputParser()  
        chain_with_history = RunnableWithMessageHistory(  
            chain,  
            lambda _: InMemoryChatMessageHistory(),  
            input_messages_key="question",  
            history_messages_key="history",  
        )  

        config = {"configurable": {"session_id": session_id}}  

        response = chain_with_history.invoke(  
            {"question": user_input, "history": history}, config=config  
        )  

        wrapped_text = textwrap.fill(  
            response, width=100, break_long_words=False, replace_whitespace=False  
        )  
        parsed_response = response.split("\nHuman:")[0].strip()  
        final_response = f"AI: {parsed_response}"  

        # Update and save history  
        updated_history = f"{history}\nYou: {user_input}\nAI: {parsed_response}"  
        save_history(session_id, updated_history)  

        history = updated_history  
        print(final_response)  

if __name__ == '__main__':  
    session_id = "1"  
    chat(session_id)
