from urllib import request
from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/users', methods=['GET', 'POST'])
def home():
    if (request.method =='POST'):
        temp = request.form.get('key')
    bodyData = request.form
    print(bodyData)
    return '<h1>Test</h1>'