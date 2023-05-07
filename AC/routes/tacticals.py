

from AC.database.models import Tacticals
from flask import Blueprint
from flask import jsonify

tacticals = Blueprint('tacticals', __name__)

@tacticals.route('/tacticals', methods=['GET'])
def getTacticals():
        items = Tacticals.query.all()
        print(items)
        tacticals = []
        for item in items:
            tacticals.append(item.as_dict())
        return jsonify(tacticals)
