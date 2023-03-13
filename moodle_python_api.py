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
    context = request.json.get('context')
    # context = '''
    # Architecturally, the school has a Catholic character. Atop the Main Building's gold dome is a golden statue of the Virgin Mary.
    # '''
    prompt_creators = {
        1: prompt_creator1(context, number),
        2: prompt_creator2(context, number),
        3: prompt_creator3(context, number),
        4: prompt_creator4(context, number),
    }
    prompt = prompt_creators[q_type]
    print(prompt)

    # PREDICT FUNCTION
    return predict_questions(prompt, q_type, number)



def prompt_creator1(context, num=1): #identification
    return f"Generate {num} Questions and their short answers as a list from the following text, {context} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator2(context, num=1): #true or false
    return f"Generate {num} true or false questions and their answers as a list from the following text, {context} using the format 'Q1.' and 'Answer:'. Answer should be either True or False\n\nQuestions and Answers:"

def prompt_creator3(context, num=1): #multiple choice
    return f"Generate {num} multiple choice questions and their answers as a list from the following text, {context} using the format 'Q1.','Choices:' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator4(context, num=1): #essay
    return f"Generate {num} essay questions and the key answers as a list from the following text, {context} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"


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

    # new = '''
    # Q1. The school has a Catholic character?
    # Answer: True 

    # Q2. Is there a golden statue of the Virgin Mary atop the Main Building's gold dome?
    # Answer: True

    # Q3. Is the Main Building's gold dome the only architectural feature with a religious character?
    # Answer: False
    # '''

    result = new.split('\n')

    ques_bank = {}

    if q_type == 3:
        print("NaN")
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