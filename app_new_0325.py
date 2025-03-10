
import streamlit as st
import os
import json
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel


class Packet(BaseModel):
    question: str
    choices: list[str]
    correct_answer: str
    explanation: str


def get_age():
    age = st.sidebar.slider("Select you AGE:", min_value=10, max_value=16, value=14, step=1,)
    return age


def get_subject():
    subject = st.sidebar.selectbox("What subject",
                                     ["Science","Technology","Engineering","Math"])
    return subject


def get_question(age, subject):
    question = f"""a {age} is preparing for a STEM competition. Generate only one random {subject} question for a {age} year old to help prepare for the competition.  
    provide four multiple choices for the correct answer. make sure that the correct answer is not always the first choice.\
     provide which is the correct answer separately and an explanation for the correct answer. \
    you must provide the response as a json format containing the keys and values for question, choices, correct_answer, explanation.\
        do not deviate from the instructions provided. make sure the keys are question, choices, correct_answer, explanation before you proceed.  keys and values must be in a CORRECT json format \
            where the keys are question, choices, correct answer, explanation. must come through as a string so that the json can be properly loaded."""
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=question,
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Packet,
        ),
    )
    
    if 'question' and 'choices' and 'correct_answer' and 'explanation' in response.text:
        data = json.loads(response.text)
    else:
        main()
    
    return data


def initialize_session_state():
    session_state = st.session_state
    session_state.form_count = 0
    session_state.quiz_data=''
    

def main():
    st.title('STEM Questions')
    st.sidebar.title("Options")
    age=get_age()
    subject=get_subject()
    if 'form_count' not in st.session_state:
        initialize_session_state()
    if 'answers' not in st.session_state:
        st.session_state.answers = 0
    if not st.session_state.quiz_data:
        st.session_state.quiz_data=get_question(age, subject)

    
    quiz_data = st.session_state.quiz_data
    st.markdown(f"Question: {quiz_data['question']}")
    
    form = st.form(key=f"quiz_form_{st.session_state.form_count}")
    user_choice = form.radio("Choose an answer:", quiz_data['choices'])
    submitted = form.form_submit_button("Submit your answer")
    
    if submitted:
        if user_choice == quiz_data['correct_answer']:
            st.session_state.answers += 1
            st.success("Correct")
        else:
            st.error("Incorrect")
        st.markdown(f"Explanation: {quiz_data['explanation']}")
        st.sidebar.write(f"Correct answers so far: {st.session_state.answers}")
        
        with st.spinner("Calling the model for the next question"):
            initialize_session_state()
        quiz_data = st.session_state.quiz_data
        
        another_question = st.button("Another question")

        if another_question:
            st.session_state.form_count += 1
        else:
            st.stop()
            


if __name__ == '__main__':
    api_key = os.environ.get('GOOGLE_API_KEY_NEW')
    client = genai.Client(api_key=api_key)
    MODEL_ID = "gemini-2.0-flash-001"
    main()
