import os, json, boto3
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/tmp/"
ALLOWED_EXTENSIONS = set(["txt"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER}"] = UPLOAD_FOLDER
app.secret_key = "insights"

def allowed_filename(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if 'file' in request.files:
            flash('no file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        '''
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        '''
    return render_template('upload.html')


@app.route("/")
def home():
    return "It's working"


@app.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    print("S3_BUCKET", S3_BUCKET)
    s3 = boto3.client('s3')

    pre_signed_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': pre_signed_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)