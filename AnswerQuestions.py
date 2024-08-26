import json
import re
import time
import os
import pickle

from openai import OpenAI
client = OpenAI(api_key = "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")

def run_gpt(system_prompt, query):
    done = False
    while not done:
        try:
            response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                  "role": "system",
                  "content": system_prompt
                },
                {
                  "role": "user",
                  "content": query
                }
                ],
                temperature=0,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            done = True
        except Exception as e:
            # Handle exception
            print(f"GPT failed!, trying again The error is: {e}")
            time.sleep(10)

    return response.choices[0].message.content

run_gpt("You are a symbolic mathematics problem solver. Using any tools at your disposal, work out the solution to the following problem:", f"""
Find the solution to the following problem:
"What's the square root of 16?"
""")


# In[ ]:


import pickle
#load from disk to continue where left off
with open('book_qas_with_answers.pkl', 'rb') as file:
    book_answers = pickle.load(file)

with open('book_qas.pkl', 'rb') as file:
    book_qas = pickle.load(file)

all_answered_problems = set([problem for _,_,problem,question,_,_ in book_answers])
unsolved_problems = [(book, how_solved, selected_problem, just_question, just_answer) for book, how_solved, selected_problem, just_question, just_answer in book_qas if selected_problem not in all_answered_problems]
    
while len(unsolved_problems)>0:
    book_qa = unsolved_problems[0]
    book, how_solved, selected_problem, just_question, just_answer = book_qa
    print(len(unsolved_problems), just_question)

    gpt_answer = run_gpt("You are a symbolic mathematics problem solver. Using any tools at your disposal, work out the solution to the following problem:", f"""
Find the solution to the following problem:
"{just_question}"
""")
    print(gpt_answer)

    book_answers.append((book, how_solved, selected_problem, just_question, just_answer, gpt_answer))
    
    # Open a file for writing binary data
    with open('book_qas_with_answers.pkl', 'wb') as file:
        pickle.dump(book_answers, file)

    #load again, because it may contain new problems now
    with open('book_qas.pkl', 'rb') as file:
        book_qas = pickle.load(file)

    all_answered_problems = set([problem for _,_,problem,question,_,_ in book_answers])
    unsolved_problems = [(book, how_solved, selected_problem, just_question, just_answer) for book, how_solved, selected_problem, just_question, just_answer in book_qas if selected_problem not in all_answered_problems]