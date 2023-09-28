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