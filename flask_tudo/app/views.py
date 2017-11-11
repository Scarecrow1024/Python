from app import app
from app.models import Todo, User
from wtforms import StringField, validators, BooleanField
from flask_wtf import FlaskForm
from flask import render_template,request,flash,abort,url_for,redirect
from flask_login import LoginManager, login_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

class AddForm(FlaskForm):
    todo = StringField('todo', [validators.DataRequired(),validators.Length(min=3, max=25)])

class LoginForm(FlaskForm):
    username = StringField('username', [validators.DataRequired(), validators.Length(min=3, max=25)])
    password = StringField('password', [validators.DataRequired(), validators.Length(min=3, max=25)])
    remember_me = BooleanField('Keep me logged in')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        #user = User(form.username.data, form.password.data)
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, form.remember_me.data)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/')
@app.route('/index')
def index():
    form = AddForm()
    todos = Todo.query.order_by('created desc').all()
    return render_template('index.html',todos=todos, form=form)

@app.route('/done/<int:id>')
def done(id):
    todo = Todo.query.get_or_404(id)
    todo.status = 1
    todo.add()
    return redirect(url_for('index'))

@app.route('/dele/<int:id>')
def dele(id):
    todo = Todo.query.get_or_404(id)
    todo.delete()
    return redirect(url_for('index'))


@app.route('/add',methods=['POST','GET'])
def add():
    form = AddForm(request.form)
    if form.validate():
        data = form.todo.data
        todo = Todo(data)
        todo.add()
    else:
        for error in form.todo.errors:
            flash(error)
    #todos = Todo.query.all()
    return redirect(url_for('index'))
    #return render_template('index.html',todos=todos, form=form)


