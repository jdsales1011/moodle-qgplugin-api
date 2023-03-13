import sys
import os

import openai

os.environ['OPENAI_API_KEY']='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'
openai.api_key = os.getenv("OPENAI_API_KEY")

# context = sys.argv[1]
# number = int (sys.argv[2])
# q_type = int(sys.argv[3])
number = 3
q_type = 2
context = '''
Architecturally, the school has a Catholic character. Atop the Main Building's gold dome is a golden statue of the Virgin Mary.
'''


def prompt_creator1(context, num=1): #identification
    return f"Generate {num} Questions and their short answers as a list from the following text, {context} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator2(context, num=1): #true or false
    return f"Generate {num} true or false questions and their answers as a list from the following text, {context} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator3(context, num=1): #multiple choice
    return f"Generate {num} multiple choice questions and their answers as a list from the following text, {context} using the format 'Q1.','Choices:' and 'Answer:'\n\nQuestions and Answers:"

def prompt_creator4(context, num=1): #essay
    return f"Generate {num} essay questions and the key answers as a list from the following text, {context} using the format 'Q1.' and 'Answer:'\n\nQuestions and Answers:"

prompt_creators = {
    1: prompt_creator1(context, number),
    2: prompt_creator2(context, number),
    3: prompt_creator3(context, number),
    4: prompt_creator4(context, number),
}


# AI PREDICT FUNCTION
def predict_questions(prompt):
  result =[]
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
#   result = new.split('\n')
  

#   result = [x for x in result if x.strip()]       # TO REMOVE EMPTY NEXT LINES

  # for index, data in enumerate(result):
  #   if index%2 == 0:          # QUESTION
  #     result[index] = data.split(".", 1)[1].strip()
  #   else:                     # ANSWER
  #     result[index] = data.split("Answer:", 1)[1].strip()

#   return result
  return new


prompt = prompt_creators[q_type]
print(prompt)

# PREDICT CODE HERE
print(predict_questions(prompt))