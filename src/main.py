
from flask import Flask, request, redirect, jsonify, flash, render_template
import os
from werkzeug.utils import secure_filename
from download_handler import snapchat_downloader

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['json']) # file extensions allowed for uploaded file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'the random string'

@app.route("/")
def index():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/#first', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            memories_path = UPLOAD_FOLDER + filename
            receiver_email = request.form['text']

            snapchat_downloader(memories_path, receiver_email)

            # TODO: add folder for uploads by email
            try:
                os.remove(UPLOAD_FOLDER + filename)
            except:
                print("Error finding/deleting {}".format(UPLOAD_FOLDER + filename))

            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
