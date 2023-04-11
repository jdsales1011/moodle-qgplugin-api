from flask import Flask
from flask import request

import sys
import os
import json
import io
import base64

import openai
import PyPDF2

os.environ['OPENAI_API_KEY']='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'
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
@app.route("/qgplugin/api/", methods = ["POST"])
def get_questions():
    # Get JSON parameter
    json_data = request.get_data(as_text=True)

    # Decode JSON data into dictionary
    params = json.loads(json_data)

    number = int(params['number'])
    q_type = int(params['type'])
    files = params['files']

    file_content = ''

    for file in files:
        file_extension = file['file_name'].split('.')[-1]
        file_decoded = base64.b64decode(file['file_encoded'])
        print(file['file_name'])
        print(file_extension)

        file_content += "\n"

        if (file_extension == "txt"):
            file_content += file_decoded.decode('utf-8')

        elif (file_extension == "pdf"):
            # Convert contents to bytes (BytesIO obj)
            file_bytes = io.BytesIO(file_decoded)
            pdf_reader = PyPDF2.PdfReader(file_bytes)
            for page in range(len(pdf_reader.pages)):
                file_content += pdf_reader.pages[page].extract_text()

            # Close BytesIO obj
            file_bytes.close()

        elif (file_extension == "docx" or file_extension == "docs"):
            print("docs")

    prompt_creators = {
        1: prompt_creator1(file_content, number),
        2: prompt_creator2(file_content, number),
        3: prompt_creator3(file_content, number),
    }
    prompt = prompt_creators[q_type]
    print(prompt)

    # PREDICT FUNCTION
    return predict_questions(prompt, q_type, number)


def prompt_creator1(content, num=1): #identification
    return f"Generate {num} Questions and their short answers as a list from the following text, {content} using the format 'Q1.' and 'Answer:', Answer must be a direct, concise, short answer. \n\nQuestions and Answers:"

def prompt_creator2(content, num=1): #true or false
    return f"Generate {num} true or false questions and their answers as a list from the following text, {content} using the format 'Q1.' and 'Answer:'. Phrase question in declarative form. Answer should be either True or False.\n\nQuestions and Answers:"

def prompt_creator3(content, num=1): #multiple choice
    return f"Generate {num} multiple choice questions and their answers as a list from the following text, {content} using the format 'Q1.','Choices: []' and 'Answer:'\n\nQuestions and Answers:"


# AI PREDICT FUNCTION
def predict_questions(prompt, q_type, number):
    result = []
    # openai.api_key = os.getenv("OPENAI_API_KEY")    
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=prompt,
    #     temperature=0.7,
    #     max_tokens=256,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )   
    # print("Response: ", response)
    # new = response['choices'][0]['text']
    # print(new)

    new = '''
    Q1. The school has a Catholic character?
    Answer: True 

    Q2. Is there a golden statue of the Virgin Mary atop the Main Building's gold dome?
    Answer: True

    Q3. Is the Main Building's gold dome the only architectural feature with a religious character?
    Answer: False
    '''

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

    ques_bank = []

    print(result)

    if q_type == 3:             # MULTIPLE CHOICE
        result = [x for x in result if x.strip()]       # TO REMOVE EMPTY NEXT LINES
    
        for i in range(0, number*3, 3):
            item = {
                "question" : result[i].split(".", 1)[1].strip(),
                "choices" : result[i+1].split("Choices:", 1)[1].strip(),
                "answer" : result[i+2].split("Answer:", 1)[1].split(".", 1)[0].strip()
                }
            ques_bank.append(item)

    else:
        result = [x for x in result if x.strip()]       # TO REMOVE EMPTY NEXT LINES    
        
        for i in range(0, number*2, 2):
            item = {
                "question" : result[i].split(".", 1)[1].strip(),
                "answer" : result[i+1].split("Answer:", 1)[1].strip()
                }
            ques_bank.append(item)

    ques_bank_json = {
        "questions": ques_bank
    }

    # Convert dict to JSON
    ques_bank_json = json.dumps(ques_bank_json)

    print("JSON RESULT: ", ques_bank_json)

    # Return a JSON 
    return ques_bank_json


if __name__ == '__main__':
    app.run(debug = True, port = 2000)