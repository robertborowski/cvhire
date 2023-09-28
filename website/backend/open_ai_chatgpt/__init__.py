# ------------------------ imports start ------------------------
import openai
import os
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
  message = f"I am providing you all of the text on a person's cv/resume. Please give me back this person's name and email address in a single string separated by one comma with no space inbetween. Content: [{file_contents}]"
  open_ai_reply = openai_chat_gpt_prompt_result_function(message)
  parts_arr = open_ai_reply.split(',')
  name = parts_arr[0]
  email = parts_arr[1]
  return name, email
# ------------------------ individual function end ------------------------