from  main import lnt
from flask import *
import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.post('/validation')
def validation():
    file = request.files['file']
    f_name = "test/"+file.name + \
        str(datetime.datetime.now().microsecond)+'.jpeg'
    file.save(f_name)
    prediction = lnt(f_name)
    return render_template('validate.html', data=prediction)

if __name__ == "__main__":
    app.run(port=5000)
