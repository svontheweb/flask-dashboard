from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'txt'}

@app.route('/')  
def main():  
    return render_template("index.html")  

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/success', methods = ['POST'])  
def success():  
  file = request.files['file']
  if file and allowed_file(file.filename):
    if request.method == 'POST':  
        file.save(os.path.join('static', file.filename))
        # f.save(f.filename)  
        return render_template("acknowledge.html", name = file.filename)
  return 'try again'

@app.route('/data', methods=['GET', 'POST'])
def data():
  if request.method == 'POST':
      file = request.form['upload-file']
      data = pd.read_excel(file)
  return render_template('data.html', data=data.to_dict())
 
# route to html page - "table"
@app.route('/table')
def table():
  # converting csv to html
  data = pd.read_csv('users.csv')
  return render_template('csvdisplay.html', tables=[data.to_html()], titles=[''])
 
 
# entry point
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
