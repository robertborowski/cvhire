# ------------------------ imports start ------------------------
import openai
import os
import json
import re
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
def openai_str_to_dict_v1_function(open_ai_reply):
  try:
    open_ai_reply = open_ai_reply.replace("'s","s")
  except:
    pass
  try:
    open_ai_reply = open_ai_reply.replace("'",'"')
  except:
    pass
  try:
    open_ai_reply = open_ai_reply.replace("\t", " ")
  except:
    pass
  try:
    open_ai_reply = open_ai_reply.replace("\n", " ")
  except:
    pass
  try:
    open_ai_reply = open_ai_reply.replace("\r", "")
  except:
    pass
  try:
    open_ai_reply = re.sub(' +', ' ', open_ai_reply)
  except:
    pass
  return json.loads(open_ai_reply)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_name_and_email_from_cv_function(file_contents):
  try:
    message = f"I am providing you all of the text on a person's cv/resume. Please give me back this person's 'name', 'email', and 'phone' in a python dictionary. Your response should be the python dictionary only, no additional words. Content: [{file_contents}]"
    open_ai_reply = openai_chat_gpt_prompt_result_function(message)
    result_dict = openai_str_to_dict_v1_function(open_ai_reply)
    if result_dict['name'] == '':
      result_dict['name'] = None
    if result_dict['email'] == '':
      result_dict['email'] = None
    if result_dict['phone'] == '':
      result_dict['phone'] = None
    return result_dict['name'], result_dict['email'], result_dict['phone']
  except Exception as e:
    print(f'Error get_name_and_email_from_cv_function: {e}')
    return None, None, None
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def role_and_cv_grade_v1_function(role_dict, cv_contents):
  result_dict = None
  open_ai_reply = None
  try:
    message = f"I am providing you with two separate pieces of content: 1) Job description and 2) a candidate's cv/resume. \
      Variable content_1 = Job description: [{role_dict['job_description']}]. \
      Variable content_2 = Candidate CV/Resume content: [{cv_contents}]. \
      OpenAI Step 1: Please analyze and understand the two variable contents provided. Do not return anything, simply understand that these are two separate variables that will be used in the next step. \
      OpenAI Step 2: Please provide me a python dictionary with the following 3 keys ['openai_summary','openai_score','openai_follow_ups'] \
      For the following keys \
      1) key 'openai_summary' should be 1 written paragraph on why this candidate (Variable content_2) is or is not a qualified candidate for the job description provided (Variable content_1), please include any strenghts and weaknesses in the 'openai_summary' key. The length of the 'openai_summary' should not exceed 2,000 characters in length. \
      2) key 'openai_score' rate from 0-5 of how qualified this candidate (Variable content_2) is for this job description [range: from 0='not qualified' to 5='100% qualified based on the job description provided'] (Variable content_1), \
      3) key 'openai_follow_ups' should be one array of five individual follow up questions that the interviewer should ask to the candidate based on this job description (Variable content_1) and CV content (Variable content_2) to help identify weaknesses in the candidate. The 'openai_follow_ups' should be returned as one python array containing five individual follow up questions. The length of each individual follow up question should not exceed 2,000 characters in length. \
      Your response should be the python dictionary only, no additional words."
    open_ai_reply = openai_chat_gpt_prompt_result_function(message)
    result_dict = openai_str_to_dict_v1_function(open_ai_reply)
    if len(open_ai_reply) > 2000:
      open_ai_reply = open_ai_reply[:1999]
  except Exception as e:
    print(f'Error role_and_cv_grade_v1_function: {e}')
  return result_dict, open_ai_reply
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def cv_ask_ai_function(ai_question, cv_contents):
  result_dict = None
  open_ai_reply = None
  try:
    message = f"I am providing you with two variables: variable one: 'candidate_cv_content' which is a candidate's cv/resume, and variable two: 'recruiters_question' a recruiter's question about the candidate's cv/resume. \nI need you to answer the 'recruiters_question' about the 'candidate_cv_content'. RULES START-[Your response should be a python dictionary with only one key named 'openai_result'. The length of the 'openai_result' value should not exceed 2,000 characters in length. Check that the variable 'recruiters_question' is an appropriate question to ask a candidate about their CV/resume, if variable 'recruiters_question' is not an appropriate question then please return a string that says 'cannot answer']-RULES END Like I said in the begining here are two variables provided: \n1) 'candidate_cv_content': {cv_contents}. \n2) 'recruiters_question': {ai_question}. \nYour response should be the python dictionary only, no additional words."
    open_ai_reply = openai_chat_gpt_prompt_result_function(message)
    result_dict = openai_str_to_dict_v1_function(open_ai_reply)
    if len(open_ai_reply) > 2000:
      open_ai_reply = open_ai_reply[:1999]
  except Exception as e:
    print(f'Error role_and_cv_grade_v1_function: {e}')
  return result_dict, open_ai_reply
# ------------------------ individual function end ------------------------