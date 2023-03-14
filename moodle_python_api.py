from flask import Flask
from flask import request

import sys
import os
import json

import openai

os.environ['OPENAI_API_KEY']='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'
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
@app.route("/qgplugin/api/", methods = ["POST"])
def get_questions():
    number = request.json.get('number')
    q_type = request.json.get('type')
    content = request.json.get('content')

    prompt_creators = {
        1: prompt_creator1(content, number),
        2: prompt_creator2(content, number),
        3: prompt_creator3(content, number),
        4: prompt_creator4(content, number),
    }
    prompt = prompt_creators[q_type]
    print(prompt)

    # PREDICT FUNCTION
    return predict_questions(prompt, q_type, number)


def prompt_creator1(content, num=1): #identification
    return f"Generate {num} Questions and their short answers as a list from the following text, {content} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator2(content, num=1): #true or false
    return f"Generate {num} true or false questions and their answers as a list from the following text, {content} using the format 'Q1.' and 'Answer:'. Answer should be either True or False\n\nQuestions and Answers:"

def prompt_creator3(content, num=1): #multiple choice
    return f"Generate {num} multiple choice questions and their answers as a list from the following text, {content} using the format 'Q1.','Choices: []' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator4(content, num=1): #essay
    return f"Generate {num} essay questions and the key answers as a list from the following text, {content} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"


# AI PREDICT FUNCTION
def predict_questions(prompt, q_type, number):
    result = []
    openai.api_key = os.getenv("OPENAI_API_KEY")    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )   
    new = response['choices'][0]['text']
    print(new)

    # new = '''
    # Q1. What type of character is the school architecturally?
    # Choices: [A. Catholic, B. Protestant, C. Jewish, D. Atheist]
    # Answer: A. Catholic

    # Q2. What is atop the Main Building's gold dome?
    # Choices: [A. A cross, B. A bell, C. A golden statue of the Virgin Mary, D. A flag]
    # Answer: C. A golden statue of the Virgin Mary

    # Q3. What color is the gold dome?
    # Choices: [A. White, B. Blue, C. Green, D. Gold]
    # Answer: D. Gold
    # '''

    result = new.split('\n')

    ques_bank = {}

    if q_type == 3:             # MULTIPLE CHOICE
        result = [x for x in result if x.strip()]       # TO REMOVE EMPTY NEXT LINES
    
        for i in range(0, number*3, 3):
            item = {
                "question" : result[i].split(".", 1)[1].strip(),
                "choices" : result[i+1].split("Choices:", 1)[1].strip(),
                "answer" : result[i+2].split("Answer:", 1)[1].split(".", 1)[0].strip()
                }
            ques_bank[int(i/3)+1] = item

    else:
        result = [x for x in result if x.strip()]       # TO REMOVE EMPTY NEXT LINES    
        
        for i in range(0, number*2, 2):
            item = {
                "question" : result[i].split(".", 1)[1].strip(),
                "answer" : result[i+1].split("Answer:", 1)[1].strip()
                }
            ques_bank[int(i/2)+1] = item

    # Convert dict to JSON
    ques_bank_json = json.dumps(ques_bank)
    # print(ques_bank_json)

    # Return a JSON 
    return ques_bank_json


if __name__ == '__main__':
    app.run(debug = True, port = 2000)