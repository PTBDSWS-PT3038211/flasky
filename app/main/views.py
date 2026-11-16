from flask import render_template
from flask_login import current_user
from ..models import User
from . import main


@main.route('/')
def index():
    users = User.query.order_by(User.id).all() \
        if current_user.is_authenticated else []
    return render_template('index.html', users=users)
