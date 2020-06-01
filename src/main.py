from flask import Flask, request, redirect, jsonify, flash, render_template
import os
from werkzeug.utils import secure_filename
from download_handler import snapchat_downloader
import config

ALLOWED_EXTENSIONS = set(['json'])  # file extensions allowed for uploaded file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.UPLOADS_PATH
app.config['SECRET_KEY'] = config.SECRET_KEY 

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

            memories_path = config.UPLOADS_PATH + filename
            receiver_email = request.form['text']

            snapchat_downloader(memories_path, receiver_email, web=True)

            # TODO: add folder for uploads by email
            try:
                os.remove(config.UPLOADS_PATH + filename)
            except:
                print("Error finding/deleting {}".format(config.UPLOADS_PATH + filename))

            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, port=5000)
