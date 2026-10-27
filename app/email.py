from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

import requests


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


def send_simple_message(to, subject, text):
    """Envia um e-mail via API do SendGrid. Retorna True se aceito."""
    app = current_app._get_current_object()
    subject = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject

    if not (app.config['API_KEY'] and app.config['API_FROM']):
        print('ERRO: SendGrid não configurado: defina SENDGRID_API_KEY no WSGI.',
              flush=True)
        return False

    try:
        resposta = requests.post(
            app.config['API_URL'],
            headers={'Authorization': 'Bearer ' + app.config['API_KEY']},
            json={'personalizations': [{'to': [{'email': to}]}],
                  'from': {'email': app.config['API_FROM'], 'name': 'Flasky App'},
                  'subject': subject,
                  'content': [{'type': 'text/plain', 'value': text}]},
            timeout=10)
    except requests.RequestException as e:
        print('ERRO: falha ao enviar e-mail para %s: %s' % (to, e), flush=True)
        return False

    if resposta.ok:
        print('E-mail enviado para %s (%s)' % (to, resposta.status_code), flush=True)
        return True
    print('ERRO: SendGrid recusou o envio para %s: %s %s'
          % (to, resposta.status_code, resposta.text), flush=True)
    return False


def notify_new_user(username, email=None):
    """Notifica cadastro de novo usuário. Retorna True se ao menos um envio funcionou."""
    config = current_app.config
    text = ('Prontuário: {}\nNome: {}\nNovo usuário cadastrado: {}'
            .format(config['FLASKY_PRONTUARIO'], config['FLASKY_NAME'], username))
    recipients = [config['FLASKY_NOTIFY'], config['FLASKY_ADMIN'], email]
    # um POST por destinatário: a falha de um endereço não deve impedir os demais
    results = [send_simple_message(r, 'Novo usuário', text)
               for r in dict.fromkeys(r for r in recipients if r)]
    return any(results)