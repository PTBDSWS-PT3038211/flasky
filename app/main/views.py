from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email, send_simple_message
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # Envia sempre para o e-mail institucional (+ professor)
            destinatarios = [current_app.config['EMAIL_INSTITUCIONAL'],
                             current_app.config['EMAIL_PROFESSOR']]
            print('Enviando mensagem para: ' + str(destinatarios), flush=True)
            resposta = send_simple_message(destinatarios, 'Novo usuário',
                                           form.name.data)
            print('Status SendGrid: ' + str(resposta.status_code), flush=True)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))