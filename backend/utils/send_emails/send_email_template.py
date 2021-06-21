# -------------------------------------------------------------- Imports
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# -------------------------------------------------------------- Main Function
def send_email_template_function(output_email, output_subject_line, output_message_content):
  print('=========================================== send_email_template_function START ===========================================')

  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('TRIVIAFY_MAIN_EMAIL'), name = "Triviafy")  # Change to your verified sender
  to_email = To(output_email)  # Change to your recipient
  subject = output_subject_line
  content = Content("text/plain", output_message_content)
  mail = Mail(from_email, to_email, subject, content)

  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()


  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  try:
    sg.client.mail.send.post(request_body=mail_json)
    print('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    print('email did not send successfully...' + output_subject_line)
    print('=========================================== send_email_template_function END ===========================================')
    return False

  print('=========================================== send_email_template_function END ===========================================')
  return True