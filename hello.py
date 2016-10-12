import os
from flask import Flask, url_for, request, render_template, redirect, send_from_directory, session, escape
from werkzeug.utils import secure_filename
from werkzeug import FileStorage

UPLOAD_FOLDER = '/tmp/flask'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'notareal123secretkey'

# @app.route('/')
# def hello_world():
    # return 'hello world'

@app.route('/')
def index():
    if 'username' in session:
        return 'Loggin in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username></p>
            <p><input type=submit value=Login></p>
        </form>
        '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/uploads', methods=['GET', 'POST'])
# def upload_file():
    # if request.method == 'POST':
        # if 'file' not in request.files:
            # flash('No file part')
            # return redirect(request.url)
        # file = request.files['file']
        # if file.filename == '':
            # flash('No selected file')
            # return redirect(request.url)
        # if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
    # return '''
    # <!doctype>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
    # <p><input type=file name=file>
        # <input type=submit value=Upload>
    # </form>
    # '''

def parse_file(file):
    return file.read().decode('utf-8')

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            session['text'] = parse_file(file)
            return redirect(url_for('output_file'))
    return '''
    <!doctype>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/done')
def output_file():
    return 'File contents: %s' % escape(session['text'])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
