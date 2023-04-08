from urllib import request
from flask import Blueprint

from AC.database.models import Users

auth = Blueprint('auth', __name__)


@auth.route('/users', methods=['GET', 'POST'])
def home():
    items = Users.query.all()
    print(items)
    # return {'items': [{'id': item.id, 'name': item.name, 'description': item.description} for item in items]}
    return items