# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 23:21:34 2025

@author: Debodip Chowdhury
"""
import os
import re
import streamlit as st
from openai import OpenAI

# Hugging Face API token (use os.environ or directly paste in testing)
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

def get_portfolio(amount, risk):
    prompt = f"""
    I have ${amount} and my risk level is '{risk}'.
    Please generate a cryptocurrency portfolio as a Python dictionary with coin names as keys and USD allocation as values.
    Only return the dictionary — no explanation, no code block, no markdown.
    """

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.choices[0].message.content
    st.text("Raw LLM Output:\n" + raw_text)

    try:
        match = re.search(r"\{[\s\S]*?\}", raw_text)
        if match:
            portfolio = eval(match.group())
            return portfolio
        else:
            return {"error": "No dictionary found in response."}
    except Exception as e:
        return {"error": str(e)}

# Streamlit interface
st.title("🧠💸 LLM-Powered Crypto Portfolio Generator")

amount = st.number_input("💰 How much do you want to invest?", min_value=10, step=10)
risk = st.selectbox("⚖️ Select your risk level", ["low", "medium", "high"])

if st.button("🚀 Generate Portfolio"):
    portfolio = get_portfolio(amount, risk)
    st.subheader("📊 Suggested Portfolio")
    st.json(portfolio)
