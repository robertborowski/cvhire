# ------------------------ imports start ------------------------
import os, time
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def send_email_template_function(output_email, output_subject_line, output_message_content):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('CVHIRE_SUPPORT_EMAIL'), name = "CVhire")  # Change to your verified sender
  to_email = To(output_email)  # Change to your recipient
  subject = output_subject_line
  content = Content("text/html", output_message_content)
  mail = Mail(from_email, to_email, subject, content)
  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()
  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  try:
    sg.client.mail.send.post(request_body=mail_json)
    # print('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    print('email did not send successfully...' + output_subject_line)
    return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def send_email_with_attachment_template_function(output_email, output_subject_line, output_message_content, output_attachment, csv_file_name):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('CVHIRE_SUPPORT_EMAIL'), name = "CVhire")  # Change to your verified sender
  to_email = To(output_email)  # Change to your recipient
  subject = output_subject_line
  content = Content("text/html", output_message_content)
  mail = Mail(from_email, to_email, subject, content)
  # ------------------------ add attachment start ------------------------
  encoded_csv_content = base64.b64encode(output_attachment.encode('utf-8')).decode()
  attachment = Attachment(
    FileContent(encoded_csv_content),
    FileName(f"{csv_file_name}.csv"),
    FileType('text/csv'),
    Disposition('attachment')
  )
  mail.attachment = attachment
  # ------------------------ add attachment end ------------------------
  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()
  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  try:
    sg.client.mail.send.post(request_body=mail_json)
    # print('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    print('email did not send successfully...' + output_subject_line)
    return False
  return True
# ------------------------ individual function end ------------------------
