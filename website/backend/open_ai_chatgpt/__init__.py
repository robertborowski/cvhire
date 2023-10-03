# ------------------------ imports start ------------------------
import openai
import os
import json
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_prompt_result_function(message):
  openai.api_key = os.environ.get('OPENAI_API_KEY')
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": message}
    ]
  )
  # Retrieve and return the assistant's reply
  reply = response['choices'][0]['message']['content']
  return reply
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_name_and_email_from_cv_function(file_contents):
  message = f"I am providing you all of the text on a person's cv/resume. Please give me back this person's 'name', 'email', and 'phone' in a python dictionary. Your response should be the python dictionary only, no additional words. Content: [{file_contents}]"
  open_ai_reply = openai_chat_gpt_prompt_result_function(message)
  open_ai_reply = open_ai_reply.replace("'",'"')
  result_dict = json.loads(open_ai_reply)
  if result_dict['name'] == '':
    result_dict['name'] = None
  if result_dict['email'] == '':
    result_dict['email'] = None
  if result_dict['phone'] == '':
    result_dict['phone'] = None
  return result_dict['name'], result_dict['email'], result_dict['phone']
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def role_and_cv_grade_v1_function(role_dict, cv_contents):
  message = f"I am providing you with 1) a job description and 2) a candidate's cv/resume. Please provide me a python dictionary with the following keys ['summary','overall_score','follow_ups'] 1) 'summary' key should be 1 paragraph why this candidate is or is not qualified for this job description, 2) 'overall_score' key from 0-10 of how qualified this candidate is for the job description, 3) 'follow_ups' key five follow up questions that the interviewer should ask the candidate during an interview for this job description. Job description: [about: {role_dict['about']}. Requirements: {role_dict['requirements']}. Nice-to-haves: {role_dict['nice_to_haves']}]. Candidate CV/Resume content: [{cv_contents}]"
  open_ai_reply = openai_chat_gpt_prompt_result_function(message)
  print(' ------------- 3 ------------- ')
  print(f"open_ai_reply | type: {type(open_ai_reply)} | {open_ai_reply}")
  print(' ------------- 3 ------------- ')
  return open_ai_reply
# ------------------------ individual function end ------------------------