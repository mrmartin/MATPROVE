#!/usr/bin/env python
# coding: utf-8

# In[5]:


#get json files containing books divided into:
#lesson, solved problems (list), supplementary with answers (list), and unanswered (list)
import os, json

import pickle

for root, dirs, files in os.walk('books'):
    for file in files:
        if file.endswith('.json'):
            json_url = os.path.join(root, file)
            print(json_url)
            
            with open(json_url, 'r') as file:
                contents, solved_problems_this_book, supplementary_problems_this_book = json.load(file)
            print(f"this book has {len(contents)} chapters, {len(solved_problems_this_book)} groups of solved problems, and {len(supplementary_problems_this_book)} groups of unworked problems with answers")


# In[6]:


if False:
    #the output structure will be:
    all_topics=[topic1, topic2, ...]
    #where
    topic1 = {
        "lesson":"There are two ways to motivate the notion of a vector: one is by means of lists ...",
        "solved_problems":[problem1, problem2, problem3, ...]
    }
    #where
    problem1 = {
        "question": "Let $u=(2,-7,1), v=(-3,0,4), w=(0,5,-8)$. Find: $3 u-4 v$,", 
        "work": "$3 u-4 v=3(2,-7,1)-4(-3,0,4)=(6,-21,3)+(12,0,-16)=(18,-21,-13)$",
        "answer": "$(18,-21,-13)$"
    }
    
    #problem 1: some problems are aggregated, like containing (a), (b), (c) in a single body of text
        #solution: get GPT to return each separately
    #problem 2: the question, work, and answer are joined together in a single string
        #solution: get GPT to split them apart
    #problem 3: I haven't conserved the link between lesson and problems
        #solution: refactor extractor code and re-run
    #problem 4: sometimes the work/answer split is nonexistent
        #solution: make the "work" and the "answer" overlap
    #problem 5: the solution can be formulated in different ways
        #solution: evaluation of answer correctness requires LLM


# In[16]:


import json
import re
import time
import os

from openai import OpenAI
client = OpenAI(api_key = "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")

def run_gpt(system_prompt, query):
    done = False
    while not done:
        try:
            response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
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

run_gpt("You are a document analysis bot. Answer very briefly right to the point, ideally in a single word or single number.", """
How many textbook questions are there in this text snippet:
"\section*{SOLVED PROBLEMS}

\section*{Vectors in $\mathbf{R}^{\boldsymbol{n}}$}"
""")


# In[39]:


book_qas = []

#load again, because it may contain new problems now
with open('book_qas.pkl', 'rb') as file:
    book_qas = pickle.load(file)


# In[40]:


book_qas


# In[48]:


def convert_book_to_qas(book, contents, solved_problems_this_book, supplementary_problems_this_book):
    print(f"this book has {len(contents)} chapters, {len(solved_problems_this_book)} groups of solved problems, and {len(supplementary_problems_this_book)} groups of unworked problems with answers")
    if book=="books/Schaum's_Outlines_-_Discrete_Mathematics,_3rd_Ed._by_Seymour_Lipschutz/2024_04_03_e2bc10318661343af903g/2024_04_03_e2bc10318661343af903g.json" or book=="books/Schaum's Outlines - Linear Algebra,Fourth Edition/2024_04_03_de2bde501961f6000cc6g/2024_04_03_de2bde501961f6000cc6g.json":
        for prob_num in range(0,len(solved_problems_this_book)):
            print("trying problem number:",prob_num)
            try:
                selected_problem = solved_problems_this_book[prob_num]
            except:
                keys = list(solved_problems_this_book.keys())
                selected_key = keys[prob_num]
                selected_problem = solved_problems_this_book[selected_key]
            print(prob_num, selected_problem)

        
            num_probs = run_gpt("You are a document analysis bot. Answer very briefly right to the point, ideally in a single word or single number.", f"""
    How many textbook questions are there in this text snippet:
    "{selected_problem}"
    """)
            try:
                print("num_probs response:",num_probs)
                if int(num_probs)>5:
                    print("too many, skipping")
                elif int(num_probs)>0:
                    print("There are ",num_probs, "converting into question-answers")
                    just_question = run_gpt("You are a document analysis bot. Give a verbatim answer contatining the requested text, with no other words before or after.", f"""
        For the problem below, repeat the question/questions only. Do not repeat the work or solution, and do not modify the way it's written:
        "{selected_problem}"
        """)
                    just_answer = run_gpt("You are a document analysis bot. Give a verbatim answer contatining the requested text, with no other words before or after.", f"""
        For the problem below, repeat the answer/answers. Do not repeat the question, but include all work and solution that is included below. Do not modify the way the solution written:
        "{selected_problem}"
        """)
                    print("problem", prob_num, "has question:",just_question, "and answer", just_answer)
                    book_qas.append((book, "solved with work", selected_problem, just_question, just_answer))
                else:
                    print("skip")
            except:
                print(num_probs, "is an invalid response from gpt")
                
            # Open a file for writing binary data
            with open('book_qas.pkl', 'wb') as file:
                pickle.dump(book_qas, file)        
    return []

def convert_book_to_qas_supplementary(book, contents, solved_problems_this_book, supplementary_problems_this_book):
    print(f"this book has {len(contents)} chapters, {len(solved_problems_this_book)} groups of solved problems, and {len(supplementary_problems_this_book)} groups of unworked problems with answers")
    
    for prob_num in range(0,len(supplementary_problems_this_book)):
        print("trying problem number:",prob_num)
        try:
            selected_problem = supplementary_problems_this_book[prob_num]
        except:
            keys = list(supplementary_problems_this_book.keys())
            selected_key = keys[prob_num]
            selected_problem = supplementary_problems_this_book[selected_key]
        print(prob_num, selected_problem)

    
        num_probs = run_gpt("You are a document analysis bot. Answer very briefly right to the point, ideally in a single word or single number.", f"""
How many textbook questions are there in this text snippet:
"{selected_problem}"
""")
        try:
            print("num_probs response:",num_probs)
            if int(num_probs)>5:
                print("too many, skipping")
            elif int(num_probs)>0:
                print("There are ",num_probs, "converting into question-answers")
                just_question = run_gpt("You are a document analysis bot. Give a verbatim answer contatining the requested text, with no other words before or after.", f"""
    For the problem below, repeat the question/questions only. Do not repeat the work or solution, and do not modify the way it's written:
    "{selected_problem}"
    """)
                just_answer = run_gpt("You are a document analysis bot. Give a verbatim answer contatining the requested text, with no other words before or after.", f"""
    For the problem below, repeat the answer/answers. Do not repeat the question, but include all work and solution that is included below. Do not modify the way the solution written:
    "{selected_problem}"
    """)
                print("problem", prob_num, "has question:",just_question, "and answer", just_answer)
                book_qas.append((book, "solved with work", selected_problem, just_question, just_answer))
            else:
                print("skip")
        except:
            print(num_probs, "is an invalid response from gpt")
            
        # Open a file for writing binary data
        with open('book_qas.pkl', 'wb') as file:
            pickle.dump(book_qas, file)        
   
     return []


# In[49]:


for root, dirs, files in os.walk('books'):
    for file in files:
        if file.endswith('.json'):
            json_url = os.path.join(root, file)
            print(json_url)
            
            with open(json_url, 'r') as file:
                contents, solved_problems_this_book, supplementary_problems_this_book = json.load(file)
            qas = convert_book_to_qas_supplementary(json_url, contents, solved_problems_this_book, supplementary_problems_this_book)


# In[ ]:




