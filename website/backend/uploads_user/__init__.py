# ------------------------ imports start ------------------------
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def allowed_cv_file_upload_function(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['docx','pdf','txt']
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_file_suffix_function(filename):
  return '.' + filename.rsplit('.', 1)[1].lower()
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def allowed_img_file_upload_function(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg','jpeg','png']
# ------------------------ individual function end ------------------------