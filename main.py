import streamlit as st
import openai
import os
from dotenv import load_dotenv
from parse_hh import get_candidate_info, get_job_description

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = openai.Client(api_key=openai_api_key)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()

def request_gpt(sistem_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sistem_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1024,
        temperature=0,
    )
    return response.choices[0].message.content

st.title("CV Scoring App for FL.ru")

job_description_url = st.text_input("Job Description url")
cv_url = st.text_input("Upload CV url")

if st.button("Score CV"):
    with st.spinner("Scoring CV..."):
        job_description = get_job_description(job_description_url)
        cv = get_candidate_info(cv_url)
        
        st.write(job_description)
        st.write(cv)

        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)
    st.write(response)
