#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 17:05:06 2024

@author: me
"""

import streamlit as st
import os
import json
import google.generativeai as genai


def get_question():
    model=genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Generate a random STEM related question for a 9 year old, provide four multiple choices for teh correct answer.  provid which is the correct answer separately and an explanation for the correct answer.  provide the response as a json containing question, choices, correct_answer, explanation.",
                                      generation_config=genai.types.GenerationConfig(temperature=0.5))
    data = json.loads(response.text)
    return data


def initialize_session_state():
    session_state = st.session_state
    session_state.form_count = 0
    session_state.quiz_data = get_question()
    

def main():
    st.title('STEM Questions')
    
    if 'form_count' not in st.session_state:
        initialize_session_state()
    if not st.session_state.quiz_data:
        st.seesion_state.quiz_data=get_question()

    quiz_data = st.session_state.quiz_data
    
    st.markdown(f"Question: {quiz_data['question']}")
    
    form = st.form(key=f"quiz_form_{st.session_state.form_count}")
    user_choice = form.radio("Choose an answer:", quiz_data['choices'])
    submitted = form.form_submit_button("Submit your answer")
    
    if submitted:
        if user_choice == quiz_data['correct_answer']:
            st.success("Correct")
        else:
            st.error("Incorrect")
        st.markdown(f"Explanation: {quiz_data['explanation']}")
        
        another_question = st.button("Another question")
        with st.spinner("Calling the model fo the next question"):
            session_state = st.session_state
            session_state.quiz_data= get_question()
        
        if another_question:
            st.session_state.form_count += 1
        else:
            st.stop()
            


if __name__ == '__main__':
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    main()
    
