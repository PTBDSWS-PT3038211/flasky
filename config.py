import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.zoho.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'flaskaulas@zohomail.com'
    # E-mail institucional do aluno (recebe a notificação de novo usuário)
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'joshua.m@aluno.ifsp.edu.br'
    # E-mail do professor (sempre recebe a notificação)
    FLASKY_NOTIFY = 'flaskaulasweb@zohomail.com'
    # Dados do aluno que vão no corpo do e-mail
    FLASKY_NAME = os.environ.get('FLASKY_NAME') or 'Joshua Cassemiro Merces'
    FLASKY_PRONTUARIO = os.environ.get('FLASKY_PRONTUARIO') or 'PT3038211'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_KEY = os.environ.get('SENDGRID_API_KEY') or os.environ.get('API_KEY')
    API_URL = os.environ.get('API_URL', 'https://api.sendgrid.com/v3/mail/send')
    API_FROM = os.environ.get('API_FROM', 'joshua.m@aluno.ifsp.edu.br')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}