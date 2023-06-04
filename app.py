from flask import Flask, render_template, request, session, redirect
# from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import math


app = Flask(__name__)

with open('params.json', 'r') as param:
    params = json.load(param)['params']

# mail = Mail(app)
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USE_TLS = False,
#     # MAIL_USERNAME = params['username'],
#     MAIL_USERNAME = 'kartikdixt8595@gmail.com',
#     MAIL_PASSWORD = 'DontTellYou5'
# )

# mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cyberhub'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
app.config['SQLALCHEMY_TRACK_MDIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)


class Contactform(db.Model):
    """ This class will create a database for our site. """

    sno = db.Column(db.Integer, primary_key=True, nullable=True)
    phone = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    def __repr__(self) -> str:
        return f"{self.serial_no} {self.title} {self.date_created}"


class Posts(db.Model):
    """ This class will create a database for our site. """

    sno = db.Column(db.Integer, primary_key=True, nullable=True)
    slug = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    tag_line = db.Column(db.String(70), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)


active_tabs = {'home': 'none',
               'get_started': 'none',
               'downloads': 'none',
               'all_post': 'none',
               'help': 'none'}

# users = Contactform.query.filter_by().all()
# for user in users:
#     user_ = str(user['name']).lower()
#     pass_ = str(user['password'])
#     print(user_)
#     print(pass_)


@app.route('/', methods=['GET'])
def home():
    """ This will servres the root or main index.html file to the server. """

    active_tabs = {'home': 'active',
                   'get_started': 'none',
                   'downloads': 'none',
                   'all_post': 'none',
                   'help': 'none'}
    if 'user' in session:
        return redirect('/dashboard')

    else:
        posts = Posts.query.filter_by().all()
        last = math.ceil(len(posts)/int(params['no_of_posts']))
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        posts = posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
        if page==1:
            prev = "#"
            next = "/?page="+ str(page+1)
        elif page==last:
            prev = "/?page="+ str(page-1)
            next = "#"
        else:
            prev = "/?page="+ str(page-1)
            next = "/?page="+ str(page+1)
        
        return render_template('index.html',active_tabs=active_tabs, params=params, posts=posts, prev=prev, next=next)


@app.route('/logout')
def logout():
    """ This method will help in logging out the user. (Prevent unauthorized people to edit page. ) """
    session.pop('user')
    return redirect('/dashboard')


@app.route('/post', methods=['GET', 'POST'])
def post():
    """ This will servres the post.html file to the server. """

    posts = Posts.query.filter_by().all()
    active_tabs = {'home': 'none',
                   'get_started': 'none',
                   'downloads': 'none',
                   'all_post': 'active',
                   'help': 'none'}

    if request.method == 'POST':
        title = request.form.get('title')
        sub_title = request.form.get('sub_title')
        content = request.form.get('content')
        slug = f"{title.replace(' ', '-')}-post"
        user = session['user']

        entry = Posts(title=title, slug=slug,
                      tag_line=sub_title, content=content, user=user)
        db.session.add(entry)
        db.session.commit()

        post_page = '/post/' + slug
        return redirect(post_page)

    return render_template('all_post.html', posts=posts, active_tabs=active_tabs)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    active_tabs = {'home': 'active',
                   'get_started': 'none',
                   'downloads': 'none',
                   'all_post': 'none',
                   'help': 'none'}

    if 'user' in session:

        user = session['user']
        all_posts = Posts.query.filter_by(user=user).all()
        return render_template('dashboard.html', active_tabs=active_tabs, posts=all_posts)
    else:
        return redirect('/login')


@app.route('/downloads')
def downloads():
    """ This will servres the downloads.html file to the server. """

    active_tabs = {'home': 'none',
                   'get_started': 'none',
                   'downloads': 'active',
                   'all_post': 'none',
                   'help': 'none'}

    return render_template('downloads.html', active_tabs=active_tabs)


@app.route('/help')
def help():

    active_tabs = {'home': 'none',
                   'get_started': 'none',
                   'downloads': 'none',
                   'all_post': 'none',
                   'help': 'active'}
    # if request.method == 'POST':
    #     send_email = request.form.get('u_email')
    #     recieve_email = request.form.get('r_email')
    #     subject = request.form.get('subject')
    #     message = request.form.get('message')

    #     mail.send_message('hello',
    #                       sender=send_email,
    #                       recipients=recieve_email,
    #                       body=message
    #                       )

    #  or -:

    # msg = Message(subject, sender=send_email, recipients = [recieve_email])
    # msg.body = message
    # mail.send(msg)
    # return "Sent"

    return render_template('help.html', active_tabs=active_tabs)


@app.route('/register', methods=['GET', 'POST'])
def register():

    active_tabs = {'home': 'none',
                   'get_started': 'active',
                   'downloads': 'none',
                   'all_post': 'none',
                   'help': 'none'}

    if 'user' in session:

        return redirect('/dashboard')

    else:

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone_num = request.form.get('phone_num')
            password = request.form.get('password')

            entry = Contactform(name=name, email=email, phone=phone_num,
                                password=password, date=datetime.now())
            db.session.add(entry)
            db.session.commit()

            return redirect('/login')
        return render_template('register.html', active_tabs=active_tabs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ This will servres the downloads.html file to the server. """
    # users = Contactform.query.filter_by().all()
    active_tabs = {'home': 'none',
                   'get_started': 'active',
                   'downloads': 'none',
                   'all_post': 'none',
                   'help': 'none'}

    if 'user' in session:

        return redirect('/dashboard')

    if request.method == 'POST':

        username = str(request.form.get('username')).lower()
        password = request.form.get('password')

        if username == params['admin_username'] and password == params['admin_password']:
            session['user'] = 'Admin'
            return redirect('/dashboard')

        # for user in users:
        #     if username == user['name'] and password == user['password']:
        #         session['user'] = user['name']
        #         return dashboard()

        #     elif username == user['name'] and password != user['password']:
        #         return 'WRONG CREDENTIALS'

        #     else:
        #         return 'WRONG CREDENTIALS'

        else:

            return render_template('login.html', active_tabs=active_tabs), 'User Not Found'
    else:

        return render_template('login.html', active_tabs=active_tabs)
    # return render_template('login.html', active_tabs=active_tabs)


@app.route("/post/<string:post_slug>")
def get_post(post_slug):

    post = Posts.query.filter_by(slug=post_slug).first()
    active_tabs = {'home': 'none',
                   'get_started': 'none',
                   'downloads': 'none',
                   'add_post_': 'none',
                   'all_post': 'active',
                   'help': 'none', }

    return render_template('post.html', post=post, active_tabs=active_tabs)


@app.route('/edit/post/<string:post_slug>', methods=['GET', 'POST'])
def edit_post(post_slug):

    active_tabs = {'home': 'none',
                   'get_started': 'active',
                   'downloads': 'none',
                   'add_post_': 'none',
                   'all_post': 'none',
                   'help': 'none',
                   }

    if 'user' in session:
        post = Posts.query.filter_by(slug=post_slug).first()

        if request.method == 'POST':
            post.title = request.form.get('title')
            post.tag_line = request.form.get('sub_title')
            post.content = request.form.get('content')

            db.session.commit()
            post_url = '/post/' + post_slug
            return redirect(post_url)

        return render_template('edit_post.html', post=post, active_tabs=active_tabs)
    else:

        return redirect('/login')


@app.route('/delete/<string:post_slug>')
def delete(post_slug):

    if 'user' in session:

        post = Posts.query.filter_by(slug=post_slug).first()
        db.session.delete(post)
        db.session.commit()

        # return 'Sucess'
        return redirect('/dashboard')


if __name__ == '__main__':

    app.run(debug=True)
