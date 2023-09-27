# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def allowed_cv_file_upload_function(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['docx','doc','pdf','txt']
# ------------------------ individual function end ------------------------
