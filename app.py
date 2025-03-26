import streamlit as st
import pandas as pd
import openai

# Set OpenAI API Key (Ensure to keep this secure)
openai.api_key = "YOUR_OPENAI_API_KEY"

def query_csv(data, query):
    prompt = f"### SQL data query based on natural language
# Data
{data.head().to_string()}

# Question: {query}
# SQL Query:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0
    )

    sql_query = response.choices[0].text.strip()

    try:
        result = pd.DataFrame(eval(f"data.query('{sql_query}')"))
        return result
    except Exception as e:
        return f"Error executing query: {e}"

# Streamlit UI
st.title("CSV Chatbot - Natural Language to SQL")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Preview of Data")
    st.write(data.head())

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        st.write(message)

    query = st.text_input("Ask a question about the data:")

    if st.button("Submit"):
        if query:
            result = query_csv(data, query)
            response = f"**You:** {query}\n**Bot:** {result}"
            st.session_state.chat_history.append(response)
            st.write(response)
        else:
            st.warning("Please enter a question about the data.")
