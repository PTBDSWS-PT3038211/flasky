from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

import requests
from datetime import datetime


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_simple_message(to, subject, newUser):
    """Envia o e-mail de novo usuário via SendGrid.
    'to' pode ser um e-mail (str) ou uma lista de e-mails.
    Retorna a resposta da API (status 202 = aceito)."""
    app = current_app._get_current_object()

    if isinstance(to, str):
        to = [to]

    assunto = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    texto = (
        'Prontuário: ' + app.config['PRONTUARIO'] + '\n'
        'Nome do aluno: ' + app.config['NOME_ALUNO'] + '\n'
        'Novo usuário cadastrado: ' + newUser
    )
    html = (
        '<h2>Novo usuário cadastrado no Flasky</h2>'
        '<p><strong>Prontuário:</strong> ' + app.config['PRONTUARIO'] + '</p>'
        '<p><strong>Nome do aluno:</strong> ' + app.config['NOME_ALUNO'] + '</p>'
        '<hr>'
        '<p><strong>Usuário cadastrado:</strong> ' + newUser + '</p>'
    )

    print('Enviando mensagem (POST)...', flush=True)
    print('URL: ' + str(app.config['API_URL']), flush=True)
    print('from: ' + str(app.config['API_FROM']), flush=True)
    print('to: ' + str(to), flush=True)
    print('subject: ' + assunto, flush=True)
    print('text: ' + texto, flush=True)

    if not app.config['API_KEY']:
        print('ERRO: variável de ambiente SENDGRID_API_KEY não definida.', flush=True)

    resposta = requests.post(
        app.config['API_URL'],
        headers={
            'Authorization': 'Bearer ' + str(app.config['API_KEY']),
            'Content-Type': 'application/json',
        },
        json={
            'personalizations': [{'to': [{'email': e} for e in to]}],
            'from': {'email': app.config['API_FROM'], 'name': 'Flasky App'},
            'subject': assunto,
            'content': [
                {'type': 'text/plain', 'value': texto},
                {'type': 'text/html', 'value': html},
            ],
        },
        timeout=15,
    )

    print('Enviando mensagem (Resposta)...' + str(resposta) + ' ' + resposta.text +
          ' - ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
    return resposta