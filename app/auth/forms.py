from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

OBRIGATORIO = 'Este campo é obrigatório.'
EMAIL_INVALIDO = 'Endereço de e-mail inválido.'
TAMANHO = 'O campo deve ter entre %(min)d e %(max)d caracteres.'
SENHAS_DIFERENTES = 'As senhas não coincidem.'


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(OBRIGATORIO), Length(1, 64, TAMANHO), Email(EMAIL_INVALIDO)])
    password = PasswordField('Senha', validators=[DataRequired(OBRIGATORIO)])
    remember_me = BooleanField('Manter conectado')
    submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(OBRIGATORIO), Length(1, 64, TAMANHO), Email(EMAIL_INVALIDO)])
    username = StringField('Nome de usuário', validators=[
        DataRequired(OBRIGATORIO), Length(1, 64, TAMANHO),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'O nome de usuário deve começar com uma letra e ter apenas '
               'letras, números, pontos ou sublinhados (sem espaços).')])
    password = PasswordField('Senha', validators=[
        DataRequired(OBRIGATORIO), EqualTo('password2', message=SENHAS_DIFERENTES)])
    password2 = PasswordField('Confirme a senha', validators=[DataRequired(OBRIGATORIO)])
    submit = SubmitField('Cadastrar')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Este e-mail já está cadastrado.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Este nome de usuário já está em uso.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Senha atual', validators=[DataRequired(OBRIGATORIO)])
    password = PasswordField('Nova senha', validators=[
        DataRequired(OBRIGATORIO), EqualTo('password2', message=SENHAS_DIFERENTES)])
    password2 = PasswordField('Confirme a nova senha',
                              validators=[DataRequired(OBRIGATORIO)])
    submit = SubmitField('Atualizar senha')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(OBRIGATORIO), Length(1, 64, TAMANHO), Email(EMAIL_INVALIDO)])
    submit = SubmitField('Redefinir senha')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Nova senha', validators=[
        DataRequired(OBRIGATORIO), EqualTo('password2', message=SENHAS_DIFERENTES)])
    password2 = PasswordField('Confirme a senha', validators=[DataRequired(OBRIGATORIO)])
    submit = SubmitField('Redefinir senha')


class ChangeEmailForm(FlaskForm):
    email = StringField('Novo e-mail', validators=[
        DataRequired(OBRIGATORIO), Length(1, 64, TAMANHO), Email(EMAIL_INVALIDO)])
    password = PasswordField('Senha', validators=[DataRequired(OBRIGATORIO)])
    submit = SubmitField('Atualizar e-mail')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Este e-mail já está cadastrado.')
