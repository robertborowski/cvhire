# -------------------------------------------------------------- Imports
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# -------------------------------------------------------------- Main Function
def send_test_email_function():
  print('=========================================== send_test_email_function START ===========================================')
  
  # ------------------------ Test 1 START ------------------------
  # message = Mail(
  #   from_email='robert@triviafy.com',
  #   to_emails='rborowski141@gmail.com',
  #   subject='Testing Send Grid',
  #   html_content='Hello World!')
  # try:
  #   sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  #   response = sg.send(message)
  #   print(response.status_code)
  #   print(response.body)
  #   print(response.headers)
  # except Exception as e:
  #   print(e.message)  
  # ------------------------ Test 1 END ------------------------



  # ------------------------ Test 2 START ------------------------
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = "robert@triviafy.com", name = "TRIVIAFY")  # Change to your verified sender
  to_email = To('rborowski141@gmail.com')  # Change to your recipient
  subject = "Weekly Recap"
  content = Content("text/plain","HELLO WORLD")
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()

  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  sg.client.mail.send.post(request_body=mail_json)
  # ------------------------ Test 2 END ------------------------

  print('=========================================== send_test_email_function END ===========================================')
  return True

# ---------------------------------------------------------------------------------------------------------------------------- Job to Run The Main Function
if __name__ == "__main__":
  send_test_email_function()