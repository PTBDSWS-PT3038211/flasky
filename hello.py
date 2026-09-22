import os
import requests as http_requests
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def enviar_email(nome_usuario):
    """Envia e-mail via SendGrid API para o professor e para o aluno."""
    try:
        response = http_requests.post(
            'https://api.sendgrid.com/v3/mail/send',
            headers={
                'Authorization': f'Bearer {SENDGRID_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'personalizations': [
                    {
                        'to': [{'email': email} for email in EMAIL_DESTINATARIOS]
                    }
                ],
                'from': {
                    'email': EMAIL_REMETENTE,
                    'name': 'Flasky App'
                },
                'subject': f'Novo usuário cadastrado - {nome_usuario}',
                'content': [
                    {
                        'type': 'text/html',
                        'value': f'''
                            <h2>Novo usuário cadastrado no Flasky</h2>
                            <p><strong>Prontuário:</strong> {PRONTUARIO}</p>
                            <p><strong>Nome do aluno:</strong> {NOME_ALUNO}</p>
                            <hr>
                            <p><strong>Usuário cadastrado:</strong> {nome_usuario}</p>
                        '''
                    }
                ]
            }
        )
        print(f'E-mail enviado! Status: {response.status_code} - {response.text}')
        return response.status_code == 202
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')
        return False


SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', 'COLE_SUA_CHAVE_AQUI')

# E-mail verificado no SendGrid (Single Sender)
EMAIL_REMETENTE = ' joshua.m@aluno.ifsp.edu.br'

EMAIL_DESTINATARIOS = [
    'flaskaulasweb@zohomail.com',
    'joshua.m@aluno.ifsp.edu.br'
]

PRONTUARIO = 'PT3038211'
NOME_ALUNO = 'Joshua Merces'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():


        user = User.query.filter_by(username=form.name.data).first()

        if user is None:


            role = Role.query.filter_by(name='User').first()


            if role is None:
                role = Role(name='User')
                db.session.add(role)
                db.session.commit()


            user = User(
                username=form.name.data,
                role=role
            )

            db.session.add(user)
            db.session.commit()

            session['known'] = False

        else:
            session['known'] = True

        session['name'] = form.name.data

        return redirect(url_for('index'))


    users = User.query.all()

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        users=users
    )