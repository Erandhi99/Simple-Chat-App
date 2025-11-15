import streamlit as st
import os
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="Joke Explainer", page_icon="😂", layout="centered")

# --- OPENAI CLIENT ---
token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# --- TITLE ---
st.title("😂 Joke Explainer")
st.write("Enter any joke and I'll explain why it's funny!")

# --- INPUT AREA ---
joke_input = st.text_area("✍️ Type your joke here:", height=140)

# --- SESSION STATE ---
if "explanation" in st.session_state is False:
    st.session_state.explanation = ""

# --- PROCESS BUTTON ---
if st.button("Explain Joke", type="primary"):
    if not joke_input.strip():
        st.warning("Please enter a joke before submitting.")
    else:
        with st.spinner("Thinking... 🤔"):
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": f"Explain this joke clearly: {joke_input}"}
                    ],
                    model=model_name,
                )

                st.session_state.explanation = response.choices[0].message.content

            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- OUTPUT ---
if st.session_state.explanation:
    st.subheader("💡 Explanation")
    st.success(st.session_state.explanation)
