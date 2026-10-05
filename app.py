## Step 1 Import the tool we need

import os 
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_groq import ChatGroq

## Setp 2 Load our secret Api Key
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")


## Step 3  Streamlit Page

st.set_page_config(
    page_title="My First Chatbot",
    page_icon="",
    layout="wide"
)


## Step 4 App title

st.title("My First AI Chatbot")
st.caption("Analytics flow")

## Step 5 check APi key
if not groq_api_key:
    st.error("Groq key not available ")
    st.info(
        "Project folder does not have .env so kindly add it"
    )
    st.code("GROQ_API_KEY= real_key_here",language="Text")
    st.stop()


## Step 6 create Simple model options

model_options={
    "GPT 20B TP":"openai/gpt-oss-20b",
    "GPT 120B TP": "openai/gpt-oss-120b"
}

## Step 7 create a chat memory with session state
if "messages" not in st.session_state:
    st.session_state.messages= []
    

if "input_tokens" not in st.session_state:
    st.session_state.input_tokens = 0

if "output_tokens" not in st.session_state:
    st.session_state.output_tokens = 0

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0


## Step8: Build side bar controls

with st.sidebar:
    st.header("📐 Chatbot Control ")
    
    selected_model_name = st.selectbox(
        "Choose AI Model",
        options=list(model_options.keys())
    )
    
    model_id= model_options[selected_model_name]
    
    
    temperature = st.slider(
        "creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Low= more focused. High=more varied"
        
    )
    
    
    max_tokens= st.slider(
        "Maximum Answer tokens",
        max_value=1024,
        min_value=128,
        value=512,
        step=128,
        help="This controls the approximate maximum response length"
        
    )
    
    st.divider()
    
    if st.button("Clear Chat",use_container_width=True):
        st.session_state.messages = []
        st.session_state.input_tokens=0
        st.session_state.output_tokens=0
        st.session_state.total_tokens=0
        st.rerun()
    
## Step 9 crete AI model conection
llm=ChatGroq(
    api_key=groq_api_key,
    model= model_id,
    temperature=temperature,
    max_tokens=max_tokens
)

 # 10  
  
user_messages = sum(
    1 for message in st.session_state.messages
    if message.get("role") == "user"
)
col1, col2, col3, col4= st.columns(4)

with col1:
    st.metric("Question Asked", user_messages)
    
with col2:
    st.metric("Saved Messages",len(st.session_state.messages))
    
with col3:
    st.metric("Creativity", f"{temperature:.1f}")

with col4:
    st.metric("Total Token Used", st.session_state.total_tokens)

st.subheader("Try a starter question")

starter_promp = None

p1, p2, p3 = st.columns(3)

with p1:
        if st.button(" 🤷‍♂️Explain AI", use_container_width=True):
            starter_promp = "Explain artificial intelligence to a 10 year "

with p2:
        if st.button("😎 Python Idea", use_container_width=True):
            starter_promp = "Give me very easy and funny project idea "
            
with p1:
        if st.button("💕Future of AI", use_container_width=True):
            starter_promp = " Tell me three exciting things AI can help humdan do "
            
st.divider()

## Step 12 Display old Chat

for message in st.session_state.messages:
    with st.chat_message("role"):
        st.markdown(message["content"])


# step 13 take new Qeustion

typed_prompt= st.chat_input("ASk me something........")
user_prompt= starter_promp or typed_prompt


# step 14 
# 1. user messgae memory m save hoga
# 2. user mssage screen per show hoga
# 3. system instruction banygi
# 4. old history langchain  message main convert hoga
# 5. Grogcloud ko request jaigi
# 6. AI ka answer mily ga
# 7. Answer screen per show hoga
# 8. Answer memmory main save hoga


if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

# 14 c 

    langchain_messages = [
        
        SystemMessage(
            content=(
                "You are a Documenter controller assistant."
                "Explain things in accuratley in easy words"
                "use short examples when needed"
                "If you are unsure,say you are unsure instead of inventing facts"
                
            )
        )
    ]


# 14 D add  in the full conversation history

    for message in st.session_state.messages:
        if message.get("role") == "user":
            langchain_messages.append(
                HumanMessage(content=message ["content"])
            )
            
        else:
            
            langchain_messages.append(
                AIMessage(content=message["content"])
            )


# 14 E ask the model for answer


    for message in st.session_state.messages:

        if message.get("role") == ["user"]:
            langchain_messages.append(
                HumanMessage(content=message["content"])
            )

        else:
            langchain_messages.append(
                AIMessage(content=message["content"])
            )

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):

            response = llm.invoke(langchain_messages)
            answer = response.content
            
            usage=response.usage_metadata or {}
            
            input_tokens= usage.get("input_tokens",0)
            output_tokens= usage.get("output_tokens",0)
            total_tokens= usage.get("total_tokens",0)
            
            st.session_state.input_tokens += input_tokens
            st.session_state.output_tokens += output_tokens
            st.session_state.total_tokens  += total_tokens
            st.markdown(answer)
            answer= ""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

            
# 14 f  save the ai answer

    if answer:
        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer,
                "usage":{
                    "input_tokens":input_tokens,
                    "output_tokens":output_tokens,
                    "total_tokens":total_tokens,
                },
                
            }
        )
        st.rerun()
    
    
    
# step 15

with st.expander("How does its chatbot works"):
  
  st.markdown(  
  
    
    """ 

    1. this showing the documents controller procedures

    """
    )
  
  
  
  # step 16
  
  st.caption(
      "Document controller assistant bot completed"
  )