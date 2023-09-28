# ------------------------ imports start ------------------------
import PyPDF2
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_file_contents_function(input_file, input_file_type):
  file_content = ''
  # ------------------------ pdf start ------------------------
  if input_file_type == '.pdf':
    pdf_reader = PyPDF2.PdfReader(input_file)
    for page in pdf_reader.pages:
      file_content += page.extract_text()
  # ------------------------ pdf end ------------------------
  # ------------------------ pdf start ------------------------
  if input_file_type == '.docx':
    pass
  # ------------------------ pdf end ------------------------
  return file_content
# ------------------------ individual function end ------------------------
