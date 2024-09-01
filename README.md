## The *MATPROVE* dataset published at *AITP 2024*

This is a dataset of lessons and worked problems in undergraduate mathematics, created to train and benchmark automated problem solvers.

Read worked problems and lessons like this:
```python
import os, json, pickle

file_path = 'book_qas.pkl'

with open(file_path, 'rb') as file:
    book_qas = pickle.load(file)

json_url, _, selected_problem, just_question, work_and_answer = book_qas[123] #select any problem block

print("question:",just_question)
print("worked answer:",work_and_answer)
```

    question: Evaluate $\lim _{x \rightarrow 0+} x^{2} \ln x$.
    worked answer: $$
    \lim _{x \rightarrow 0+} x^{2} \operatorname{In} x=\lim _{x \rightarrow 0+} \frac{\operatorname{In} x}{1 / x^{2}}=\lim _{x \rightarrow 0+} \frac{1 / x}{-2 / x^{3}} \lim _{x \rightarrow 0+} \frac{-x^{2}}{2}=0
    $$
    
    The given limit has the "indeterminate form" $0 \cdot \infty$. In the second step the form is altered so as to give the indeterminate form $\infty / \infty$, and L'Hospital's rule is then applied.

```python
with open(json_url, 'r') as file:
    #this is an issue because I've dropped the lesson-problem association
    contents, solved_problems_this_book, supplementary_problems_this_book = json.load(file)

#[i for i, complete_chapter in enumerate(contents) if scomplete_chapter['all']
for i in range(0, len(contents)):
    if selected_problem in contents[i]['all']:
        print("this problem is in lesson",i)
        lesson = contents[i]['lesson']

print("lesson:",lesson[:100],"...and so on")
```

    this problem is in lesson 3
    lesson: section*{CHAPTER 4}
    
    \section*{Derivatives}
    
    \section*{The Concept and Definition of a Derivative}
    C ...and so on

 ## Several pipelines related to the dataset are included:

 - pipeline to convert each textbook into chapter blocks and individual exercises, saved as four .json files - one for each book. See *GPT-processing-[].ipynb* scripts (*Calculus 5th edition* is dropped, so 4 books remain)
 - pipeline to process each exercise into the triplet: question/worked solution/correct answer. Multi-part questions are treated in blocks  when answering *structured_books_to_qa.ipynb*
 - pipeline to solve each exercise, either with the chapter context, or without it *AnswerQuestions.ipynb*
 - pipeline to grade solutions *GradeAnswers.ipynb*. This takes into account every part of each multi-part question separately, and this is where the number of questions is counted (5221 questions in 3091 blocks. An additional 388 blocks are dropped by GPT)

Individual questions with work and answers are contained in *book_qas_with_answers.pkl*, and lessons are in 
-books/SCHAUM's Outlines - Advanced Calculus, 3rd Edition_2010/2024_04_03_ffb6ac533fe0a53b3ceeg/2024_04_03_ffb6ac533fe0a53b3ceeg.json
-books/Schaum's Outlines - Linear Algebra,Fourth Edition/2024_04_03_de2bde501961f6000cc6g/2024_04_03_de2bde501961f6000cc6g.json
-books/Schaum's Outlines - Tensor Calculus/2024_04_03_41f90be4f896e21f0dc9g/2024_04_03_41f90be4f896e21f0dc9g.json
-books/Schaum's_Outlines_-_Discrete_Mathematics,_3rd_Ed._by_Seymour_Lipschutz/2024_04_03_e2bc10318661343af903g/2024_04_03_e2bc10318661343af903g.json


