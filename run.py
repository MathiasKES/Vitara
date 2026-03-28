import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

from waitress import serve
if __name__ == '__main__':
    is_prod = (os.getenv('FLASK_ENV') == 'production')
    if is_prod:
        serve(app, host='127.0.0.1', port=5002)
    else:
        app.run(debug=True, port=5002)
