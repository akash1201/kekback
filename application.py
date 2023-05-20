from AC import create_app
import os

print(os.environ.get('FLASK_DEBUG'), "env")
application = create_app(os.environ.get('FLASK_DEBUG'))

if __name__ == '__main__':
    application.run(debug=True)