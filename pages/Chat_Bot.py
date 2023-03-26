import streamlit as st 
import os 
import openai 


url = st.text_input("Enter some URL")

ques = st.text_input("Ask yout question")

if st.button("Submit question"):

    input ="Use thw following source url :"+ str(url) + " : Inorder to answer the following question  : "+ str(ques)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input,
        temperature=0.56,
        max_tokens=2066,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    out = response.choices[0].text
    st.write(out)