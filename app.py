import os, json, boto3
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from helpers import *


UPLOAD_FOLDER = "/tmp/"
ALLOWED_EXTENSIONS = set(["txt", ".csv"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER}"] = UPLOAD_FOLDER
app.secret_key = "insights"
app.config.from_object("config")
#app.config.from_object("insights.config")


def allowed_filename(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        print(type(request.files))
        if 'file' in request.files.getlist('file'):
            flash('no file part')
            print("NO FILE PART")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("FILE.FILENAME")
            return redirect(request.url)
        print(file.readlines())
        if file and allowed_filename(file.filename):
            print("type of file", type(file), type(file.filename))
            print(file)
            file.filename = secure_filename(file.filename)
            output = upload_file_to_s3(file, app.config['S3_BUCKET'])
            print("OUTPUT: ", output)
            print(app.config["S3_LOCATION"], file.filename)
            return render_template('uploadsuccess.html')
    print("NOT POST")
    return render_template('upload.html')


@app.route("/")
def home():
    return "It's working"


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
    '''
    app.run()
    '''